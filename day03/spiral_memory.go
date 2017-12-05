package main

import "fmt"

func main() {
	// test := 1
	// test := 12
	// test := 23
	// test := 75
	// test := 1024
	test := 361527
	layers := findLayers(test)
	fmt.Println(getSteps(layers, test))
}

func findLayers(n int) int {
	layers := 0
	for n > (8 * layers) {
		n -= (8 * layers)
		layers++
	}

	return layers
}

func getSteps(layers int, target int) int {
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
