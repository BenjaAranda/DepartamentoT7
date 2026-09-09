"""Extract the unchanged T7 PDF references and record their provenance."""

import argparse
import hashlib
import io
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pdfplumber
import pypdf
from PIL import Image, __version__ as pillow_version


ROOT = Path(__file__).resolve().parents[1]
SOURCE_NAME = "Presentación Aprobación Proyecto Técnico 2.pdf"
EXPECTED_SHA256 = "ad8e0871ed6afb7117e2dafa80bc28ad90b3c845709dc268ba01fcd12259aeec"
PAGE_NUMBER = 20
DPI = 216
PLAN_CROP_PT = [8, 174, 625, 485]  # x0, top, x1, bottom; PDF points, not meters.


def digest(data):
    return hashlib.sha256(data).hexdigest()


def image_record(path, role):
    data = path.read_bytes()
    with Image.open(io.BytesIO(data)) as image:
        image.load()
        return {
            "file": path.name,
            "role": role,
            "bytes": len(data),
            "sha256": digest(data),
            "format": image.format,
            "size_px": list(image.size),
            "mode": image.mode,
            "decoded_rgb_sha256": digest(image.convert("RGB").tobytes()),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT.parent / SOURCE_NAME)
    parser.add_argument("--output", type=Path, default=ROOT / "references/derived/p20-t7")
    parser.add_argument("--pdftoppm", default=shutil.which("pdftoppm"))
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    source_bytes = source.read_bytes()
    before = digest(source_bytes)
    if before != EXPECTED_SHA256:
        raise ValueError("El PDF no coincide con la referencia aprobada; revisar su procedencia antes de extraer.")
    if not args.pdftoppm:
        raise RuntimeError("No se encontró pdftoppm; indicar --pdftoppm con su ruta.")
    reader = pypdf.PdfReader(io.BytesIO(source_bytes))
    page = reader.pages[PAGE_NUMBER - 1]
    if len(reader.pages) != 42 or list(page.mediabox) != [0, 0, 960, 540] or page.rotation != 0:
        raise ValueError("La estructura de la lámina no coincide con la referencia registrada.")

    with pdfplumber.open(io.BytesIO(source_bytes)) as pdf:
        sheet = pdf.pages[PAGE_NUMBER - 1]
        placements = [
            {"resource_name": item["name"], "bbox_pt_top_left": [item["x0"], item["top"], item["x1"], item["bottom"]],
             "source_size_px": list(item["srcsize"])}
            for item in sheet.images
        ]
        access_words = [word for word in sheet.extract_words() if word["text"] == "ACCESO"]
        if len(access_words) != 1:
            raise ValueError("No se identificó el rótulo de acceso de forma unívoca.")
        access = access_words[0]
        if not (PLAN_CROP_PT[0] <= access["x0"] < access["x1"] <= PLAN_CROP_PT[2]
                and PLAN_CROP_PT[1] <= access["top"] < access["bottom"] <= PLAN_CROP_PT[3]):
            raise ValueError("El recorte propuesto cortaría el rótulo de acceso.")

    output.mkdir(parents=True, exist_ok=True)
    artifacts = []
    for key, filename, size, role in [
        ("/Image196", "planta-nativa.png", (1536, 813), "native_plan_without_page_overlays"),
        ("/Image195", "isometrica-nativa.jpg", (915, 826), "native_isometric"),
    ]:
        image = page.images[key]
        if image.image.size != size:
            raise ValueError("Resolución inesperada en " + key)
        obj = image.indirect_reference.get_object()
        decoded_pdf_stream = obj.get_data()
        artifact_path = output / filename
        # pypdf's ImageFile may re-encode JPEG; copy the original DCT stream instead.
        artifact_path.write_bytes(decoded_pdf_stream if filename.endswith(".jpg") else image.data)
        record = image_record(artifact_path, role)
        record.update({
            "pdf_resource": key,
            "pdf_object_id": image.indirect_reference.idnum,
            "pdf_generation": image.indirect_reference.generation,
            "pdf_filter": str(obj.get("/Filter")),
            "pdf_color_space": str(obj.get("/ColorSpace")),
            "bits_per_component": obj.get("/BitsPerComponent"),
            "resampled": False,
        })
        if filename.endswith(".png"):
            record["pdf_decoded_pixels_sha256"] = digest(decoded_pdf_stream)
            record["native_pixels_match"] = record["decoded_rgb_sha256"] == digest(decoded_pdf_stream)
            if len(decoded_pdf_stream) != size[0] * size[1] * 3 or not record["native_pixels_match"]:
                raise ValueError("La planta exportada no conserva los píxeles RGB del PDF.")
        else:
            record["pdf_jpeg_stream_sha256"] = digest(decoded_pdf_stream)
            record["original_jpeg_bytes_match"] = artifact_path.read_bytes() == decoded_pdf_stream
            if not record["original_jpeg_bytes_match"]:
                raise ValueError("La isométrica no conserva los bytes JPEG del PDF.")
        placement = next(item for item in placements if item["resource_name"] == key[1:])
        bounds = placement["bbox_pt_top_left"]
        record["page_bbox_pt_top_left"] = bounds
        record["effective_pdf_dpi"] = [round(size[0] * 72 / (bounds[2] - bounds[0]), 6),
                                       round(size[1] * 72 / (bounds[3] - bounds[1]), 6)]
        artifacts.append(record)

    base = [str(args.pdftoppm), "-f", str(PAGE_NUMBER), "-l", str(PAGE_NUMBER), "-r", str(DPI), "-png", "-singlefile"]
    subprocess.run(base + [str(source), str(output / "pagina-20-contexto")], check=True, capture_output=True)
    scale = DPI / 72
    left, top, right, bottom = [int(value * scale) for value in PLAN_CROP_PT]
    subprocess.run(base + ["-x", str(left), "-y", str(top), "-W", str(right-left), "-H", str(bottom-top),
                          str(source), str(output / "planta-compuesta")], check=True, capture_output=True)
    context = image_record(output / "pagina-20-contexto.png", "full_page_context_with_header_and_annotations")
    context["render_dpi"] = DPI
    crop = image_record(output / "planta-compuesta.png", "plan_with_original_page_overlays_and_access_label")
    crop.update({"render_dpi": DPI, "crop_bbox_pt_top_left": PLAN_CROP_PT,
                 "crop_bbox_render_pixels": [left, top, right, bottom]})
    with Image.open(output / "pagina-20-contexto.png") as full, Image.open(output / "planta-compuesta.png") as cropped:
        if full.size != (2880, 1620) or cropped.size != (1851, 933):
            raise ValueError("El render no tiene las dimensiones previstas.")
        crop["pixels_match_full_page_region"] = full.crop((left, top, right, bottom)).tobytes() == cropped.tobytes()
        if not crop["pixels_match_full_page_region"]:
            raise ValueError("El recorte no coincide píxel a píxel con el render completo.")
    artifacts.extend([context, crop])

    text = "\n".join(line.rstrip() for line in page.extract_text().splitlines()).rstrip() + "\n"
    text_path = output / "pagina-20-texto.txt"
    text_path.write_text(text, encoding="utf-8", newline="\n")
    after = digest(source.read_bytes())
    if after != before:
        raise ValueError("La huella del PDF cambió durante la extracción.")
    version_result = subprocess.run([str(args.pdftoppm), "-v"], check=True, capture_output=True, text=True)
    manifest = {
        "reference_id": "T7-P20",
        "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {"filename": source.name, "path_from_project_root": "../" + SOURCE_NAME,
                   "bytes": len(source_bytes), "page_count": len(reader.pages), "page_number": PAGE_NUMBER,
                   "page_index": PAGE_NUMBER - 1, "sha256_before": before, "sha256_after": after, "unchanged": True},
        "page": {"media_box_pt": list(page.mediabox), "crop_box_pt": list(page.cropbox), "rotation_degrees": page.rotation,
                 "coordinate_system": "PDF points; image and crop bounds use x right, y down from upper-left; 72 pt per inch",
                 "image_placements": placements},
        "tools": {"pypdf": pypdf.__version__, "pdfplumber": pdfplumber.__version__, "Pillow": pillow_version,
                  "poppler": (version_result.stderr or version_result.stdout).splitlines()[0]},
        "artifacts": artifacts,
        "text_extraction": {"file": text_path.name, "bytes": text_path.stat().st_size, "sha256": digest(text_path.read_bytes()),
                            "scope": "PDF text objects only; no OCR of dimensions inside the raster plan"},
        "calibration": {"status": "not_calibrated", "meters_per_pixel": None, "area_verified": False,
                        "note": "PDF points and render DPI do not establish architectural scale. T09-T13 remain pending."},
        "provenance_notes": [
            "Native image extraction does not include separate PDF text or drawing overlays.",
            "The plan composite retains original page labels, access arrow and two placements of Image190.",
            "Native images were not resized, rotated, mirrored or retouched. Composite images are PDF renders at 216 DPI.",
            "Rendering at 216 DPI does not add architectural information to the native raster images.",
        ],
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({"source_unchanged": True, "page_number": PAGE_NUMBER,
                      "images": [{"file": a["file"], "size_px": a["size_px"], "bytes": a["bytes"]} for a in artifacts],
                      "native_plan_pixels_match": artifacts[0]["native_pixels_match"],
                      "original_isometric_jpeg_bytes_match": artifacts[1]["original_jpeg_bytes_match"],
                      "composite_matches_full_page": crop["pixels_match_full_page_region"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
