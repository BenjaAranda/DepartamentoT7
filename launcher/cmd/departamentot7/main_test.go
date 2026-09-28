package main

import (
	"io/fs"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestOfflinePackageAndLocalAccess(t *testing.T) {
	site, err := fs.Sub(embedded, "site")
	if err != nil {
		t.Fatal(err)
	}
	host := "127.0.0.1:45123"
	handler := siteHandler(site, host)
	for _, tc := range []struct {
		method, url, host string
		want              int
		fragment          string
	}{
		{"GET", "/", host, 200, "DepartamentoT7"},
		{"GET", "/models/manifest.json", host, 200, "revision"},
		{"HEAD", "/models/departamento-t7-web.glb", host, 200, ""},
		{"GET", "/", "untrusted.example", 403, ""},
		{"POST", "/", host, 405, ""},
		{"GET", "/private.env", host, 404, ""},
		{"GET", "/assets/../models/manifest.json", host, 404, ""},
	} {
		req := httptest.NewRequest(tc.method, tc.url, nil)
		req.Host = tc.host
		resp := httptest.NewRecorder()
		handler.ServeHTTP(resp, req)
		if resp.Code != tc.want || !strings.Contains(resp.Body.String(), tc.fragment) {
			t.Errorf("%s %s (%s): got %d, want %d", tc.method, tc.url, tc.host, resp.Code, tc.want)
		}
		if tc.method == "HEAD" && resp.Body.Len() != 0 {
			t.Error("HEAD returned a body")
		}
	}
}

func TestBrowserChoice(t *testing.T) {
	url := "http://127.0.0.1:45123/"
	find := func(name string) string {
		return map[string]string{"chrome": "C:/Chrome/chrome.exe", "edge": "C:/Edge/msedge.exe"}[name]
	}
	for _, tc := range []struct {
		platform, preference, want string
	}{
		{"windows", "auto", "C:/Chrome/chrome.exe"},
		{"windows", "default", "rundll32"},
		{"windows", "edge", "C:/Edge/msedge.exe"},
		{"darwin", "auto", "open"},
		{"linux", "auto", "xdg-open"},
	} {
		name, args, err := browserCommand(tc.platform, tc.preference, url, find)
		if err != nil || name != tc.want || args[len(args)-1] != url {
			t.Errorf("%s %s: got %q %v %v", tc.platform, tc.preference, name, args, err)
		}
	}
	name, _, err := browserCommand("windows", "auto", url, func(name string) string {
		if name == "edge" {
			return "C:/Edge/msedge.exe"
		}
		return ""
	})
	if err != nil || name != "C:/Edge/msedge.exe" {
		t.Error("auto did not fall back to Edge")
	}
	_, _, err = browserCommand("windows", "chrome", url, func(string) string { return "" })
	if err == nil {
		t.Error("missing requested browser was silently ignored")
	}
}
