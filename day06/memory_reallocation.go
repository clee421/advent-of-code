package main

import (
	"bufio"
	"bytes"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func main() {
	file := "input.txt"
	f, err := os.Open(fmt.Sprintf("./%v", file))
	if err != nil {
		panic(err)
	}

	var sa []string
	scanner := bufio.NewScanner(f)
	if scanner.Scan() {
		line := scanner.Text()
		sa = strings.Split(line, " ")
	}

	mem := make([]int, 0)
	for _, v := range sa {
		i, err := strconv.Atoi(v)
		if err != nil {
			log.Fatal(err)
		}

		mem = append(mem, i)
	}

	dupe := make([]int, len(mem))
	copy(dupe, mem)

	res, state := findCycles(mem)

	fmt.Println(res, " ", state)

	cycle := findState(dupe, state)

	fmt.Println(res - cycle)
}

// 658 is too low
// 6681 is correct, issue with findMax... I'm an idiot
func findCycles(mem []int) (int, string) {
	cycles := 0

	// create a set
	set := make(map[string]struct{})

	// variable for set to check exists
	var exists = struct{}{}

	var state string
	for {
		// getting current state
		state = intArrayToString(mem)

		// if ok then state already exists then we're done
		_, ok := set[state]
		if ok {
			break
		}

		// add the current state to set since it does not exist
		set[state] = exists

		// find where max block is
		i := findMax(mem)

		// redistribute the max block
		redistributeBlock(&mem, i)

		// one cycle completed
		cycles++
	}

	return cycles, state
}

func intArrayToString(a []int) string {
	var buffer bytes.Buffer

	for i, v := range a {
		if i < len(a)-1 {
			s := strconv.FormatInt(int64(v), 10)
			buffer.WriteString(s)
			buffer.WriteString(" ")
		}
	}

	s := strconv.FormatInt(int64(a[len(a)-1]), 10)
	buffer.WriteString(s)

	return buffer.String()
}

func findMax(a []int) int {
	index := 0
	max := a[index]

	for i, v := range a {
		if v > max {
			index = i
			max = v
		}
	}

	return index
}

func redistributeBlock(mem *[]int, i int) {
	state := *mem

	// store block to be redistributed
	block := state[i]

	// remove block from location
	state[i] = 0

	// distribution amount is the amount divided by length
	dist := block / len(state)

	// if it did not divide evenly then round up
	if block%len(state) > 0 {
		dist++
	}

	// keep distributing until there is none remaining
	for block > 0 {
		// distribute to the next block
		i++

		// check if out of boundry
		if i > len(state)-1 {
			i = 0
		}

		// if there are not enough then just distribute the rest
		// otherwise there is more then enough to keep going
		if block < dist {
			state[i] += block
			block = 0
		} else {
			state[i] += dist
			block -= dist
		}
	}
}

func findState(mem []int, target string) int {
	cycles := 0

	// create a set
	set := make(map[string]struct{})

	// variable for set to check exists
	var exists = struct{}{}

	for {
		// getting current state
		state := intArrayToString(mem)

		if state == target {
			break
		}

		// add the current state to set since it does not exist
		set[state] = exists

		// find where max block is
		i := findMax(mem)

		// redistribute the max block
		redistributeBlock(&mem, i)

		// one cycle completed
		cycles++
	}

	return cycles
}
