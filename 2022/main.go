package main

import (
	"aoc/2022/day01"
	"aoc/2022/day02"
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

type Task interface {
	RunPart1(input []string) string
	RunPart2(input []string) string
}
type Daily struct {
	task Task
}

func main() {
	useSample := flag.Bool("sample", false, "Use sample input")
	flag.Parse()

	if flag.NArg() != 2 {
		fmt.Println("Correct usage is: go run main <day> <part>")
	}
	day := flag.Arg(0)
	part := flag.Arg(1)

	packages := map[string]Daily{
		"day01": {task: day01.CreateTask()},
		"day02": {task: day02.CreateTask()},
	}

	daily, ok := packages[day]
	if !ok {
		fmt.Printf("Unrecognized day: %s", day)
		os.Exit(1)
	}

	if part != "part1" && part != "part2" {
		fmt.Printf("Unrecognized part: %s", part)
		os.Exit(1)
	}

	inputFilepath := fmt.Sprintf("./%s/input.txt", day)
	if *useSample {
		inputFilepath = fmt.Sprintf("./%s/sample.txt", day)
	}

	lines := readFile(inputFilepath)
	output := ""
	if part == "part1" {
		output = daily.task.RunPart1(lines)
	} else {
		output = daily.task.RunPart2(lines)
	}

	fmt.Println(output)
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	return strings.Split(string(data), "\n")
}
