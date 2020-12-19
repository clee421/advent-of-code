package main

import (
	"flag"
	"fmt"
	"os"
)

const mainFile string = `package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

func main() {
	r := readFile("./input.data")

	fmt.Println("Lines:", r)
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	return lines
}
`

func main() {
	pathPointer := flag.String("path", "", "creates basic files for AoC")
	flag.Parse()

	if *pathPointer == "" {
		fmt.Println("--path must be set")
		panic(1)
	}

	path := fmt.Sprintf("./%s", *pathPointer)

	if _, err := os.Stat(path); os.IsNotExist(err) {
		os.Mkdir(path, os.ModePerm)
	}

	createFile(path+"/test.data", "")
	createFile(path+"/input.data", "")
	createFile(path+"/main.go", mainFile)
}

func createFile(path string, data string) {
	f, err := os.Create(path)
	if err != nil {
		fmt.Printf("Error creating %s\n", path)
		panic(1)
	}
	defer f.Close()

	f.Write([]byte(data))
}
