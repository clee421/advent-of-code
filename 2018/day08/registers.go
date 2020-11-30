package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Instruction type for each line parsed
type Instruction struct {
	Register     string
	Modification string
	Value        int
	// Conditional
	Left      string
	Condition string
	Right     int
}

func main() {
	file := "input.txt"
	f, err := os.Open(fmt.Sprintf("./%v", file))
	if err != nil {
		panic(err)
	}

	// map of registers and value
	mapRegisters := make(map[string]int)

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()

		// parse the line
		i := parseLine(line)

		updateRegister(&mapRegisters, i)

		// fmt.Println(i)
		// fmt.Println(mapRegisters)
	}

	r, v := findLargestValue(&mapRegisters)

	fmt.Printf("Largest value is: %s-%v\n", r, v)
}

func findLargestValue(rm *map[string]int) (string, int) {
	regMap := *rm

	started := false
	var reg string
	var val int

	for r, v := range regMap {
		if !started || v > val {
			reg = r
			val = v
		}

		if !started {
			started = true
		}
	}

	return reg, val
}

func parseLine(s string) Instruction {
	// format: c dec -10 if a >= 1
	split := strings.Split(s, " ")
	v, _ := strconv.Atoi(split[2])
	l, _ := strconv.Atoi(split[6])

	return Instruction{
		Register:     split[0],
		Modification: split[1],
		Value:        v,
		Left:         split[4],
		Condition:    split[5],
		Right:        l,
	}
}

func updateRegister(r *map[string]int, i Instruction) {
	if i.validCondition(r) {
		i.update(r)
	}
}

func (i Instruction) validCondition(reg *map[string]int) bool {
	r := *reg

	switch i.Condition {
	case "==":
		return r[i.Left] == i.Right
	case "!=":
		return r[i.Left] != i.Right
	case ">":
		return r[i.Left] > i.Right
	case "<":
		return r[i.Left] < i.Right
	case "<=":
		return r[i.Left] <= i.Right
	case ">=":
		return r[i.Left] >= i.Right
	default:
		return false
	}
}

func (i Instruction) update(reg *map[string]int) {
	r := *reg
	if i.Modification == "dec" {
		r[i.Register] -= i.Value
	}

	if i.Modification == "inc" {
		r[i.Register] += i.Value
	}
}
