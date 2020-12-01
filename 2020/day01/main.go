package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func main() {
	nums := readFile("./input.data")
	result := twoSum(nums, 2020)
	fmt.Println("Two sum result is:", result)

	result = threeSum(nums, 2020)
	fmt.Println("Three sum result is:", result)
}

func threeSum(nums []int, target int) int {
	for i, n := range nums {
		newTarget := target - n
		newNums := append(nums[:i], nums[i+1:]...)

		res := twoSum(newNums, newTarget)
		if res > 0 {
			fmt.Printf("%d + %d = %d\n", n, target-n, target)
			return res * n
		}
	}

	return 0
}

func twoSum(nums []int, target int) int {
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
