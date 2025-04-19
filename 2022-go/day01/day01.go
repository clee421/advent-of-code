package day01

import (
	"fmt"
	"strconv"
)

type Runner struct{}

type Elf struct {
	calories []int
}

func (e *Elf) Total() int {
	total := 0
	for i := 0; i < len(e.calories); i++ {
		total += e.calories[i]
	}

	return total
}

func parse(lines []string) []Elf {
	elves := []Elf{}
	calories := []int{}

	// yea it's messy
	for i := 0; i < len(lines); i++ {
		if i == len(lines)-1 || lines[i] == "" {
			if lines[i] != "" {
				c, _ := strconv.Atoi(lines[i])
				calories = append(calories, c)
			}
			elves = append(elves, Elf{calories: calories})
			calories = []int{}
		} else {
			c, _ := strconv.Atoi(lines[i])
			calories = append(calories, c)
		}
	}

	return elves
}

func max(a int, b int) int {
	if a > b {
		return a
	}

	return b
}

func CreateTask() *Runner {
	return &Runner{}
}

func (r *Runner) RunPart1(lines []string) string {
	elves := parse(lines)
	largest := 0

	for i := 0; i < len(elves); i++ {
		largest = max(largest, elves[i].Total())
	}

	return fmt.Sprint("Total calories:", largest)
}

func (r *Runner) RunPart2(lines []string) string {
	elves := parse(lines)
	topN := []int{0, 0, 0}

	for i := 0; i < len(elves); i++ {
		total := elves[i].Total()
		if total > topN[2] {
			topN[2] = total
			if topN[2] > topN[1] {
				topN[2], topN[1] = topN[1], topN[2]

			}
			if topN[1] > topN[0] {
				topN[1], topN[0] = topN[0], topN[1]

			}
		}
	}

	largest := topN[0] + topN[1] + topN[2]

	return fmt.Sprint("Total calories:", largest)
}
