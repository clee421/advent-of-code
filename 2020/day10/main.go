package main

import (
	"fmt"
	"io/ioutil"
	"sort"
	"strconv"
	"strings"
)

func main() {
	r := readFile("./input.data")
	nums := sortedList(r)

	joltDiff := calculateJoltDiff(nums)
	fmt.Println("Jolt diff:", joltDiff)

	tree := buildTree(nums)
	result := calculateCombinations(tree, nums[len(nums)-1])
	fmt.Println("Jolt combos:", result)
}

func buildTree(sortedNums []int) map[int][]int {
	l := len(sortedNums)

	tree := map[int][]int{}
	curr := 0

	for i, n := range sortedNums {
		check := []int{}
		for s := i; s < l; s++ {
			if sortedNums[s] <= curr+3 {
				check = append(check, sortedNums[s])
			}

			if sortedNums[s] > curr+3 {
				break
			}
		}

		tree[curr] = check
		curr = n
	}

	return tree
}

func calculateCombinations(tree map[int][]int, last int) int {
	memo := map[int]*int{}
	return dfs(tree, 0, last, memo)
}

// I attempted to implement my own stack to use for the DFS. It turned out to be terrible and
// you should never do that. There's much more to handle than just the value.
func dfs(tree map[int][]int, start int, last int, memo map[int]*int) int {
	if memo[start] != nil {
		return *memo[start]
	}

	if start == last {
		return 1
	}

	sum := 0
	for _, n := range tree[start] {
		sum += dfs(tree, n, last, memo)
	}

	memo[start] = &sum

	return sum
}

func calculateJoltDiff(sortedNums []int) int {
	joltMap := map[int]int{}
	nums := append([]int{0}, sortedNums...)
	for i := 1; i < len(nums); i++ {
		diff := nums[i] - nums[i-1]
		joltMap[diff]++
	}

	// some weird requirment
	joltMap[3]++

	// fmt.Println(joltMap)

	return joltMap[1] * joltMap[3]
}

func sortedList(lines []string) []int {
	nums := []int{}
	for _, l := range lines {
		n, _ := strconv.Atoi(l)
		nums = append(nums, n)
	}

	sort.Ints(nums)
	return nums
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	return lines
}
