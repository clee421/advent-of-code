package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func main() {
	lines := readFile("./input.data")
	fuels := parseData(lines)

	result := sum(fuels)
	fmt.Println("Total fuel:", result)

	result = sum2(fuels)
	fmt.Println("Total recurse fuel:", result)
}

func calculateUsage(f int) int {
	sum := 0
	for f > 0 {
		f = (f/3 - 2)
		if f < 0 {
			f = 0
		}

		sum += f
	}

	return sum
}

func sum2(d []int) int {
	sum := 0
	for _, n := range d {
		sum += calculateUsage(n)
	}

	return sum
}

func sum(d []int) int {
	sum := 0
	for _, n := range d {
		sum += (n/3 - 2)
	}

	return sum
}

func parseData(lines []string) []int {
	fuels := []int{}
	for _, l := range lines {
		n, err := strconv.Atoi(l)
		if err != nil {
			panic("Cannot convert number")
		}

		fuels = append(fuels, n)
	}

	return fuels
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	return strings.Split(string(data), "\n")
}
