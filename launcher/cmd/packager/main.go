package main

import (
	"archive/zip"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

func add(writer *zip.Writer, source, name string, mode os.FileMode) error {
	file, err := os.Open(source)
	if err != nil {
		return err
	}
	defer file.Close()
	header := &zip.FileHeader{Name: name, Method: zip.Deflate}
	header.SetMode(mode)
	entry, err := writer.CreateHeader(header)
	if err != nil {
		return err
	}
	_, err = io.Copy(entry, file)
	return err
}

func main() {
	binary := flag.String("binary", "", "compiled simulator")
	readme := flag.String("readme", "", "Spanish quick-start guide")
	output := flag.String("output", "", "output ZIP")
	flag.Parse()
	if *binary == "" || *readme == "" || *output == "" {
		fmt.Fprintln(os.Stderr, "binary, readme and output are required")
		os.Exit(2)
	}
	if err := os.MkdirAll(filepath.Dir(*output), 0755); err != nil {
		panic(err)
	}
	file, err := os.Create(*output)
	if err != nil {
		panic(err)
	}
	writer := zip.NewWriter(file)
	if err := add(writer, *binary, filepath.Base(*binary), 0755); err != nil {
		panic(err)
	}
	if err := add(writer, *readme, "LEEME.txt", 0644); err != nil {
		panic(err)
	}
	if err := writer.Close(); err != nil {
		panic(err)
	}
	if err := file.Close(); err != nil {
		panic(err)
	}
	fmt.Println(*output)
}
