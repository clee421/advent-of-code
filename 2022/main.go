package main

import (
	"aoc/2022/day01"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Println("Correct usage is: go run main <day> <part>")
	}
	day := os.Args[1]
	part := os.Args[2]

	switch day {
	case "day01":
		Day01(part)
	default:
		fmt.Printf("Unrecognized day: %s", day)
	}
}

func Day01(part string) {
	lines := readFile("./day01/input.txt")
	if part == "part1" {
		day01.RunPart1(lines)
	} else {
		day01.RunPart2(lines)
	}
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	return strings.Split(string(data), "\n")
}
