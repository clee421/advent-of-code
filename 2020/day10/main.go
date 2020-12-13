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
