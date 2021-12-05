package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

type Point struct {
	x int
	y int
}

type Grid [1000][1000]int

func main() {
	points := readFile("./input-data")
	overlap := solve(Grid{}, points)
	fmt.Println("overlap", overlap)
}

func solve(grid Grid, points [][]Point) int {
	count := 0

	for i := 0; i < len(points); i++ {
		to, from := points[i][0], points[i][1]

		// going vertical
		if to.x == from.x {
			col := to.x
			start, end := to.y, from.y
			if end < start {
				start, end = end, start
			}

			for s := start; s <= end; s++ {
				grid[s][col]++
				if grid[s][col] == 2 {
					count++
				}
			}
			// going horizontal
		} else if to.y == from.y {
			row := to.y
			start, end := to.x, from.x
			if end < start {
				start, end = end, start
			}

			for s := start; s <= end; s++ {
				grid[row][s]++
				if grid[row][s] == 2 {
					count++
				}
			}
			// diagonal time
		} else {
			// assumption made that it's exactly diagonal
			distance := abs(to.x - from.x)
			directionX := (from.x - to.x) / distance
			directionY := (from.y - to.y) / distance

			for d := 0; d <= distance; d++ {
				nextX := to.x + (directionX * d)
				nextY := to.y + (directionY * d)

				grid[nextY][nextX]++
				if grid[nextY][nextX] == 2 {
					count++
				}
			}
		}
	}

	// for i := 0; i < 10; i++ {
	// 	row := ""
	// 	for j := 0; j < 10; j++ {
	// 		row += strconv.Itoa((grid[i][j])) + " "
	// 	}

	// 	fmt.Println(row)
	// }

	return count
}

func abs(n int) int {
	if n < 0 {
		return -n
	}

	return n
}

func readFile(filename string) [][]Point {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	points := [][]Point{}
	for _, l := range lines {
		ps := strings.Split(l, "->")

		toParts := strings.Split(strings.TrimSpace(ps[0]), ",")
		x, _ := strconv.Atoi(toParts[0])
		y, _ := strconv.Atoi(toParts[1])
		to := Point{x, y}

		fromParts := strings.Split(strings.TrimSpace(ps[1]), ",")
		x, _ = strconv.Atoi(fromParts[0])
		y, _ = strconv.Atoi(fromParts[1])
		from := Point{x, y}

		points = append(points, []Point{to, from})
	}

	return points
}
