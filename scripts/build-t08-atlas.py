"""Build a source-bound, non-metric atlas from the T08 trace catalogue."""
import base64
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "references/derived/p20-t7"
CATALOGUE = ROOT / "architecture/classification/t08-trazos.tsv"
OUTPUT = ROOT / "references/derived/t08-clasificacion"
FAMILIES = [
    ("muros", "Muros y tabiques", "Candidatos a cerramiento: registrar caras, quiebres y huecos en T11 antes de extruir."),
    ("vanos", "Vanos y pasos", "Conservar las discontinuidades; confirmar tipo de carpintería y límites en T11."),
    ("hojas", "Hojas y barridos", "La hoja es móvil; el arco solo representa su apertura y nunca forma una pared."),
    ("mobiliario", "Mobiliario", "Modelar como muebles independientes según el programa del usuario, no como arquitectura."),
    ("equipamiento", "Equipamiento", "Representar equipos y apoyos por separado; confirmar los símbolos provisionales."),
    ("cotas", "Cotas y rótulos técnicos", "Son mediciones y notas del dibujo; inventariar en T09, sin convertirlas en sólidos."),
    ("tramas", "Tramas y líneas simbólicas", "No asignar altura ni volumen a achurados, retícula o diagonales por su grafismo."),
    ("libres", "Espacios libres", "Conservar maniobra, transferencia y circulación; no añadir colliders a las reservas gráficas."),
    ("anotaciones", "Anotaciones de la lámina", "Texto, flechas y figuras humanas son evidencia, no órdenes ni geometría del modelo."),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main():
    manifest = json.loads((SOURCE_DIR / "manifest.json").read_text(encoding="utf-8"))
    source_hashes = {}
    for artifact in manifest["artifacts"]:
        content = (SOURCE_DIR / artifact["file"]).read_bytes()
        if sha(content) != artifact["sha256"]:
            raise ValueError("Referencia modificada: " + artifact["file"])
        source_hashes[artifact["file"]] = artifact["sha256"]
    pdf = ROOT.parent / manifest["source"]["filename"]
    if sha(pdf.read_bytes()) != manifest["source"]["sha256_before"]:
        raise ValueError("El PDF original no coincide con la referencia registrada.")
    families = {key for key, _, _ in FAMILIES}
    sizes = {"nativa": (1536, 813), "compuesta": (1851, 933)}
    items, ids = [], set()
    with CATALOGUE.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            if row["id"] in ids or row["familia"] not in families or row["confianza"] not in {"alta", "media"}:
                raise ValueError("Identificador, familia o confianza inválidos: " + row["id"])
            ids.add(row["id"])
            box = [int(row[key]) for key in ["x0", "y0", "x1", "y1"]]
            width, height = sizes[row["vista"]]
            if not (0 <= box[0] < box[2] <= width and 0 <= box[1] < box[3] <= height):
                raise ValueError("Localizador fuera de la imagen: " + row["id"])
            items.append({"id": row["id"], "family": row["familia"], "label": row["nombre"],
                          "confidence": row["confianza"], "frame": row["vista"], "bbox_px": box,
                          "criterion": row["criterio"], "model_geometry_allowed": False})
    counts = dict(Counter(item["family"] for item in items))
    if set(counts) != families:
        raise ValueError("Falta al menos una familia de trazos.")
    plan = next(a for a in manifest["artifacts"] if a["file"] == "planta-nativa.png")
    crop = next(a for a in manifest["artifacts"] if a["file"] == "planta-compuesta.png")
    box, crop_box = plan["page_bbox_pt_top_left"], crop["crop_bbox_pt_top_left"]
    factor = crop["render_dpi"] / 72
    transform = {"offset_x": (box[0] - crop_box[0]) * factor, "offset_y": (box[1] - crop_box[1]) * factor,
                 "scale_x": (box[2] - box[0]) * factor / 1536, "scale_y": (box[3] - box[1]) * factor / 813}
    catalogue = {
        "task": "T08", "revision": 1, "authored_source": "architecture/classification/t08-trazos.tsv",
        "authored_source_sha256": sha(CATALOGUE.read_bytes()), "source_pdf_sha256": manifest["source"]["sha256_before"],
        "source_image_sha256": source_hashes,
        "coordinate_policy": {"unit": "px", "origin": "upper_left", "x_direction": "right", "y_direction": "down",
                              "purpose": "approximate_locators_not_contours", "metric_scale": None,
                              "bounds_are_wall_faces": False, "model_geometry_allowed": False},
        "native_to_composite": transform,
        "families": [{"id": key, "label": label, "rule": rule} for key, label, rule in FAMILIES],
        "items": items,
    }
    write_json(ROOT / "architecture/classification/t08-clasificacion.json", catalogue)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    render_data = {"families": catalogue["families"], "items": items, "transform": transform,
                   "native": "data:image/png;base64," + base64.b64encode((SOURCE_DIR / "planta-nativa.png").read_bytes()).decode(),
                   "composite": "data:image/png;base64," + base64.b64encode((SOURCE_DIR / "planta-compuesta.png").read_bytes()).decode()}
    template = (ROOT / "scripts/templates/t08-atlas.html").read_text(encoding="utf-8")
    if template.count("__T08_DATA__") != 1:
        raise ValueError("La plantilla no tiene un único punto de inserción.")
    page = template.replace("__T08_DATA__", json.dumps(render_data, ensure_ascii=False).replace("</", "<\\/"))
    (OUTPUT / "atlas.html").write_text(page, encoding="utf-8", newline="\n")
    checks = {"task": "T08", "source_pdf_unchanged": True, "source_images_unchanged": True,
              "records": len(items), "unique_ids": len(ids), "families": counts,
              "locators_within_source_frames": True, "metric_geometry_export_enabled": False,
              "medium_confidence_ids": [item["id"] for item in items if item["confidence"] == "media"],
              "atlas_sha256": sha((OUTPUT / "atlas.html").read_bytes()),
              "catalogue_sha256": sha((ROOT / "architecture/classification/t08-clasificacion.json").read_bytes())}
    write_json(OUTPUT / "comprobacion.json", checks)
    print(json.dumps(checks, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
