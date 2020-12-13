package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

const part = 2

// Instruction single instruction for console
type Instruction struct {
	Command string
	Value   int
}

// History is the slice of state for the instruction
type History struct {
	Index int
	Value int
}

func main() {
	r := readFile("./input.data")
	is := parseInstructions(r)
	result, ok := runInstructions(is)

	fmt.Println("Accumulator value:", result, ok)
}

func runInstructions(is []Instruction) (int, bool) {
	acc, ok, history := runInstructionsFromState(0, 0, is)
	if part == 2 {
		for i := len(history) - 1; i >= 0; i-- {
			last := history[i]
			// fmt.Println("Retrying from:", last.Value, "at", last.Index)
			is[last.Index].Command = flipCommand(is[last.Index].Command)
			retryAcc, retryOk, _ := runInstructionsFromState(last.Value, last.Index, is)
			if retryOk {
				return retryAcc, retryOk
			}
		}
	}

	return acc, ok
}

func runInstructionsFromState(start int, index int, is []Instruction) (int, bool, []History) {
	h := []History{}

	acc := start
	seen := map[int]bool{}

	i := index
	for i < len(is) {
		// fmt.Println("Looking at index:", i)
		if _, ok := seen[i]; ok {
			// seen before so infinite loop
			return acc, false, h
		}

		jump := 0

		in := is[i]
		// fmt.Println("Running", in.Command, in.Value)

		switch in.Command {
		case "acc":
			acc += in.Value
			jump++
		case "jmp":
			jump += in.Value
		case "nop":
			jump = 1
		}

		seen[i] = true

		i += jump

		h = append(h, History{i, acc})
	}

	return acc, true, h
}

func parseInstructions(lines []string) []Instruction {
	is := []Instruction{}
	for _, l := range lines {
		s := strings.Split(l, " ")
		cmd := s[0]
		val, err := strconv.Atoi(s[1])
		if err != nil {
			panic(fmt.Sprintf("could not parse %s", s[1]))
		}

		is = append(is, Instruction{cmd, val})
	}

	return is
}

func flipCommand(cmd string) string {
	if cmd == "nop" {
		return "jmp"
	}

	return "nop"
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	return lines
}
