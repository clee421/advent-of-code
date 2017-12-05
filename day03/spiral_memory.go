package main

import "fmt"

func main() {
	// test := 1
	// test := 12
	// test := 23
	// test := 75
	// test := 1024
	// test := 361527
	// tar := 747
	tar := 361527
	fmt.Println(getSteps(tar))
	fmt.Println(findGridTarget(tar))
}

func getLayers(n int) int {
	layers := 0
	for n > (8 * layers) {
		n -= (8 * layers)
		layers++
	}

	return layers
}

func getSteps(target int) int {
	layers := getLayers(target)
	limit := 1
	for i := 0; i <= layers; i++ {
		limit += (8 * i)
	}

	side := layers * 2

	upper := limit
	lower := limit - side

	for target < lower {
		upper, lower = lower, lower-side
	}

	mid := (upper + lower) / 2

	dist := target - mid
	if dist < 0 {
		dist *= -1
	}

	steps := dist + layers

	return steps
}

func findGridTarget(target int) int {
	layers := getLayers(target)
	size := (layers * 2) + 1
	grid := make([][]int, 0)

	for i := 0; i < size; i++ {
		grid = append(grid, make([]int, size))
	}

	i := layers
	j := layers
	grid[i][j] = 1

	// went right once
	j++
	grid[i][j] = 1

	for {
		// go up until can't
		for grid[i][j-1] != 0 {
			i--
			addAllDirections(&grid, i, j)
			if grid[i][j] > target {
				return grid[i][j]
			}
		}

		// go left until can't
		for grid[i+1][j] != 0 {
			j--
			addAllDirections(&grid, i, j)
			if grid[i][j] > target {
				return grid[i][j]
			}
		}

		// go down until can't
		for grid[i][j+1] != 0 {
			i++
			addAllDirections(&grid, i, j)
			if grid[i][j] > target {
				return grid[i][j]
			}
		}

		// go right until can't
		for grid[i-1][j] != 0 {
			j++
			addAllDirections(&grid, i, j)
			if grid[i][j] > target {
				return grid[i][j]
			}
		}
	}
}

func addAllDirections(g *[][]int, x, y int) {
	// printGrid(g)

	direct := make([][]int, 0)
	direct = append(direct, []int{-1, 1})
	direct = append(direct, []int{0, 1})
	direct = append(direct, []int{1, 1})
	direct = append(direct, []int{-1, 0})
	direct = append(direct, []int{1, 0})
	direct = append(direct, []int{-1, -1})
	direct = append(direct, []int{0, -1})
	direct = append(direct, []int{1, -1})

	grid := *g

	for _, v := range direct {
		a, b := v[0], v[1]
		grid[x][y] += grid[x+a][y+b]
	}
}

func printGrid(g *[][]int) {
	grid := *g
	for _, v := range grid {
		fmt.Println(v)
	}
}
