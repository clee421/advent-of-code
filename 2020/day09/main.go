package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func main() {
	r := readFile("./input.data")
	nums := parseNumbers(r)
	result := findEncodeError(nums, 25)

	fmt.Println("Encoding error:", result)

	cs := findContiguousSet(nums, result)
	w := findEncryptionWeakness(cs)
	fmt.Println("Encryption weakness:", w)
}

func findEncryptionWeakness(nums []int) int {
	min, max := nums[0], nums[0]
	for _, n := range nums {
		if n < min {
			min = n
		}

		if n > max {
			max = n
		}
	}

	return min + max
}

func findContiguousSet(nums []int, target int) []int {
	s, e := 0, 1
	sum := nums[s] + nums[e]
	for s <= e && e < len(nums) {
		// fmt.Println("start:", s, "end:", e)
		// fmt.Println("sum:", sum, "target:", target)

		if sum == target {
			return nums[s : e+1]
		}

		if sum > target {
			sum -= nums[s]
			s++
		} else if sum < target {
			e++
			sum += nums[e]
		}
	}

	return []int{}
}

func findEncodeError(list []int, preamble int) int {
	seen := map[int]bool{}
	for i := 0; i < preamble; i++ {
		seen[list[i]] = true
	}

	for i := preamble; i < len(list); i++ {
		curr := list[i]
		ok := findNumberPair(seen, curr)
		if !ok {
			return curr
		}

		drop := list[i-preamble]
		// fmt.Println("dropped:", drop, i-preamble)
		seen[drop] = false
		seen[curr] = true
	}

	return -1
}

func findNumberPair(dict map[int]bool, target int) bool {
	for k, v := range dict {
		if v {
			pair := target - k
			if dict[pair] {
				return true
			}
		}
	}

	return false
}

func parseNumbers(lines []string) []int {
	nums := []int{}
	for _, l := range lines {
		n, err := strconv.Atoi(l)
		if err != nil {
			panic(err)
		}

		nums = append(nums, n)
	}

	return nums
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	return lines
}
