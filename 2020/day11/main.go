package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

func main() {
	r := readFile("./input.data")

	grid := parseData(r)
	result1 := solve1(grid)
	fmt.Println("Total seats", result1)
}

func solve1(data [][]byte) int {
	newData := simulate(data)

	rounds := 0
	for !isEqual(newData, data) {
		rounds++
		data = newData
		newData = simulate(newData)
	}

	fmt.Println("solve 1 took", rounds, "rounds")
	return countSeats(newData)
}

func logGrid(grid [][]byte) {
	fmt.Println("")
	for _, row := range grid {
		fmt.Println(string(row))
	}
	fmt.Println("")
}

func simulate(data [][]byte) [][]byte {
	nd := [][]byte{}
	for i := range data {
		row := []byte{}
		for j := range data[i] {
			state := calculateNewState(data, i, j)
			row = append(row, state)
		}

		nd = append(nd, row)
	}

	return nd
}

func calculateNewState(grid [][]byte, x int, y int) byte {
	moves := [][]int{
		[]int{-1, -1},
		[]int{-1, 0},
		[]int{-1, 1},
		[]int{0, -1},
		[]int{0, 1},
		[]int{1, 1},
		[]int{1, 0},
		[]int{1, -1},
	}

	empty := 0
	occupied := 0
	for _, m := range moves {
		nx, ny := m[0]+x, m[1]+y

		validXMove := 0 <= nx && nx < len(grid)
		validYMove := validXMove && 0 <= ny && ny < len(grid[nx])
		validMove := validXMove && validYMove
		if !validMove {
			continue
		}

		switch grid[nx][ny] {
		case 'L':
			empty++
		case '#':
			occupied++
		}
	}

	if grid[x][y] == 'L' && occupied == 0 {
		return '#'
	}

	if grid[x][y] == '#' && occupied >= 4 {
		return 'L'
	}

	return grid[x][y]
}

func isEqual(a [][]byte, b [][]byte) bool {
	if len(a) != len(b) {
		fmt.Println("this... should not happen")
		panic(1)
	}

	for i := range a {
		if len(a[i]) != len(b[i]) {
			fmt.Println("well then")
			panic(1)
		}

		for j := range a[i] {
			if a[i][j] != b[i][j] {
				return false
			}
		}
	}

	return true
}

func countSeats(data [][]byte) int {
	count := 0
	for _, r := range data {
		for _, d := range r {
			if d == '#' {
				count++
			}
		}
	}

	return count
}

func parseData(lines []string) [][]byte {
	data := [][]byte{}
	for _, l := range lines {
		row := []byte{}
		for i := 0; i < len(l); i++ {
			row = append(row, l[i])
		}

		data = append(data, row)
	}

	return data
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	return lines
}
