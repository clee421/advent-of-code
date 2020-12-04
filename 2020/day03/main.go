package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

func main() {
	grid := readFile("./input.data")

	slopes := [][]int{
		{1, 1},
		{3, 1},
		{5, 1},
		{7, 1},
		{1, 2},
	}

	total := 1
	for _, slope := range slopes {
		count := countTrees(grid, slope[0], slope[1])
		fmt.Printf("On slope %d-%d found %d trees\n", slope[0], slope[1], count)

		if count > 0 {
			total *= count
		}
	}

	fmt.Println("Multiplied trees:", total)
}

func countTrees(grid [][]byte, dx int, dy int) int {
	count := 0

	width := len(grid[0])

	coordX := (dx % width)
	coordY := dy
	for coordY < len(grid) {
		if grid[coordY][coordX] == '#' {
			count++

		}

		coordX = (coordX + dx) % width
		coordY += dy
	}

	return count
}

func readFile(filename string) [][]byte {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	grid := [][]byte{}
	for _, l := range lines {
		row := []byte{}

		for i := 0; i < len(l); i++ {
			row = append(row, l[i])
		}

		grid = append(grid, row)
	}

	return grid
}
