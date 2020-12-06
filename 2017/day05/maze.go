package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	f, err := os.Open("./input.txt")
	if err != nil {
		panic(err)
	}

	ma := make([]int, 0)

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()

		i, err := strconv.Atoi(line)
		if err != nil {
			log.Fatal(err)
		}
		ma = append(ma, i)
	}

	// steps := findSteps(ma)
	steps := findStepsVariant(ma)

	// fmt.Println("Number of steps (part 1): ", steps)
	fmt.Println("Number of steps (part 2): ", steps)
}

// This runs quite slowly
func findSteps(maze []int) int {
	steps := 0
	pos := 0

	for {
		// get next position
		next := pos + maze[pos]

		// increment step for this current step
		steps++

		// we're still in the loop so increment current position
		maze[pos]++

		// if next position is out of array then you've escaped
		if next >= len(maze) || next < 0 {
			fmt.Println(maze)
			return steps
		}

		// get the next position and start again
		pos = next
	}
}

// 29875842 is wrong
// 24315397 is right // had to swap code lines
func findStepsVariant(maze []int) int {
	steps := 0
	pos := 0

	for {
		// get next position
		next := pos + maze[pos]

		// increment step for this current step
		steps++

		// weirdness variation if offset is 3 or more
		if maze[pos] >= 3 {
			maze[pos]--
		} else {
			maze[pos]++
		}

		// if next position is out of array then you've escaped
		if next >= len(maze) || next < 0 {
			// fmt.Println(maze)
			return steps
		}

		// get the next position and start again
		pos = next
	}
}
