package main

import (
	"context"
	"embed"
	"errors"
	"flag"
	"fmt"
	"io/fs"
	"log"
	"net"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"path"
	"path/filepath"
	"runtime"
	"strings"
	"time"
)

//go:embed site
var embedded embed.FS

func findWindowsBrowser(name string) string {
	executable, folders := "", []string{}
	switch name {
	case "chrome":
		executable = "chrome.exe"
		folders = []string{"Google/Chrome/Application"}
	case "edge":
		executable = "msedge.exe"
		folders = []string{"Microsoft/Edge/Application"}
	default:
		return ""
	}
	for _, root := range []string{os.Getenv("PROGRAMFILES"), os.Getenv("PROGRAMFILES(X86)"), os.Getenv("LOCALAPPDATA")} {
		if root == "" {
			continue
		}
		for _, folder := range folders {
			candidate := filepath.Join(root, filepath.FromSlash(folder), executable)
			if info, err := os.Stat(candidate); err == nil && !info.IsDir() {
				return candidate
			}
		}
	}
	return ""
}

func browserCommand(platform, preference, url string, find func(string) string) (string, []string, error) {
	if preference != "auto" && preference != "default" && preference != "chrome" && preference != "edge" {
		return "", nil, fmt.Errorf("navegador no reconocido: %s", preference)
	}
	if platform == "windows" {
		if preference == "auto" {
			for _, candidate := range []string{"chrome", "edge"} {
				if executable := find(candidate); executable != "" {
					return executable, []string{"--new-window", url}, nil
				}
			}
		} else if preference != "default" {
			if executable := find(preference); executable != "" {
				return executable, []string{"--new-window", url}, nil
			}
			return "", nil, fmt.Errorf("%s no se encuentra instalado", preference)
		}
		return "rundll32", []string{"url.dll,FileProtocolHandler", url}, nil
	}
	if preference == "chrome" || preference == "edge" {
		return "", nil, fmt.Errorf("la elección %s solo está disponible en Windows", preference)
	}
	if platform == "darwin" {
		return "open", []string{url}, nil
	}
	return "xdg-open", []string{url}, nil
}

func openBrowser(url, preference string) error {
	name, args, err := browserCommand(runtime.GOOS, preference, url, findWindowsBrowser)
	if err != nil {
		return err
	}
	fmt.Println("Navegador:", filepath.Base(name))
	return exec.Command(name, args...).Start()
}

func siteHandler(files fs.FS, host string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Host != host {
			http.Error(w, "Acceso local solamente", http.StatusForbidden)
			return
		}
		if r.Method != http.MethodGet && r.Method != http.MethodHead {
			w.Header().Set("Allow", "GET, HEAD")
			http.Error(w, "Metodo no permitido", http.StatusMethodNotAllowed)
			return
		}
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.Header().Set("Referrer-Policy", "no-referrer")
		w.Header().Set("Cross-Origin-Resource-Policy", "same-origin")
		w.Header().Set("Cache-Control", "no-store")
		w.Header().Set("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
		for _, part := range strings.Split(r.URL.Path, "/") {
			if part == ".." {
				http.NotFound(w, r)
				return
			}
		}
		name := strings.TrimPrefix(path.Clean("/"+r.URL.Path), "/")
		if name == "" || name == "." {
			name = "index.html"
		}
		if name != "index.html" && name != "favicon.svg" && name != "reference/planta-t7.png" && name != "models/manifest.json" && name != "models/departamento-t7-web.glb" && name != "models/departamento-t7.json" && !strings.HasPrefix(name, "assets/") {
			http.NotFound(w, r)
			return
		}
		if strings.HasPrefix(name, "assets/") && (strings.Count(name, "/") != 1 || !(strings.HasSuffix(name, ".js") || strings.HasSuffix(name, ".css") || strings.HasSuffix(name, ".wasm") || strings.HasSuffix(name, ".woff2"))) {
			http.NotFound(w, r)
			return
		}
		data, err := fs.ReadFile(files, name)
		if err != nil {
			http.NotFound(w, r)
			return
		}
		switch path.Ext(name) {
		case ".html":
			w.Header().Set("Content-Type", "text/html; charset=utf-8")
		case ".js":
			w.Header().Set("Content-Type", "text/javascript; charset=utf-8")
		case ".css":
			w.Header().Set("Content-Type", "text/css; charset=utf-8")
		case ".json":
			w.Header().Set("Content-Type", "application/json")
		case ".glb":
			w.Header().Set("Content-Type", "model/gltf-binary")
		case ".png":
			w.Header().Set("Content-Type", "image/png")
		case ".svg":
			w.Header().Set("Content-Type", "image/svg+xml")
		case ".wasm":
			w.Header().Set("Content-Type", "application/wasm")
		case ".woff2":
			w.Header().Set("Content-Type", "font/woff2")
		}
		w.Header().Set("Content-Length", fmt.Sprint(len(data)))
		if r.Method == http.MethodGet {
			_, _ = w.Write(data)
		}
	})
}

func main() {
	noBrowser := flag.Bool("no-browser", false, "do not open a browser (diagnostics)")
	browser := flag.String("browser", "auto", "auto, default, chrome or edge (Windows)")
	flag.Parse()
	site, err := fs.Sub(embedded, "site")
	if err != nil {
		log.Fatal(err)
	}
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		log.Fatal("No se pudo iniciar el servidor local: ", err)
	}
	address := listener.Addr().String()
	server := &http.Server{Handler: siteHandler(site, address), ReadHeaderTimeout: 5 * time.Second, IdleTimeout: 30 * time.Second}
	url := "http://" + address + "/"
	fmt.Println("DepartamentoT7 abierto en", url)
	fmt.Println("Cierra esta ventana para detener el simulador.")
	if !*noBrowser {
		if err := openBrowser(url, *browser); err != nil {
			fmt.Println(err, "· Abre manualmente", url)
		}
	}
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()
	go func() {
		<-ctx.Done()
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
		defer cancel()
		_ = server.Shutdown(shutdownCtx)
	}()
	if err := server.Serve(listener); err != nil && !errors.Is(err, http.ErrServerClosed) {
		log.Fatal(err)
	}
}
