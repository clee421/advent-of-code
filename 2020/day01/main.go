package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func main() {
	nums := readFile("./input.data")
	result := solve(nums, 2020)
	fmt.Println("Result is:", result)
}

func solve(nums []int, target int) int {
	seen := map[int]bool{}
	for _, n := range nums {
		diff := target - n
		if seen[diff] {
			fmt.Printf("%d + %d = %d\n", n, diff, target)
			return n * diff
		}

		seen[n] = true
	}

	return 0
}

func readFile(filename string) []int {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	n := []int{}
	for _, l := range lines {
		i, err := strconv.Atoi(l)
		if err != nil {
			continue
		}

		n = append(n, i)
	}

	return n
}
