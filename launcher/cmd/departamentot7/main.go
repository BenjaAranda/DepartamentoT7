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
	"runtime"
	"strings"
	"time"
)

//go:embed site
var embedded embed.FS

func openBrowser(url string) error {
	var name string
	var args []string
	switch runtime.GOOS {
	case "windows":
		name, args = "rundll32", []string{"url.dll,FileProtocolHandler", url}
	case "darwin":
		name, args = "open", []string{url}
	default:
		name, args = "xdg-open", []string{url}
	}
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
		if err := openBrowser(url); err != nil {
			fmt.Println("Abre manualmente", url)
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
