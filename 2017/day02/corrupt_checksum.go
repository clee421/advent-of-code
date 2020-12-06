package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	f, err := os.Open("./data.txt")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	sum := 0

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), "\t")
		// sum += getMinMaxDifference(line)
		sum += evenDivision(line)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	// fmt.Printf("Checksum: %v\n", sum)
	fmt.Printf("Checksum (part 2): %v\n", sum)
}

func getMinMaxDifference(sa []string) int {
	max, err := strconv.Atoi(sa[0])
	if err != nil {
		panic(err)
	}
	min, err := strconv.Atoi(sa[0])
	if err != nil {
		panic(err)
	}

	for _, v := range sa {
		num, err := strconv.Atoi(v)
		if err != nil {
			panic(err)
		}

		if num > max {
			max = num
		}

		if num < min {
			min = num
		}
	}

	return max - min
}

func evenDivision(sa []string) int {
	na := make([]int, 0, len(sa))
	for _, v := range sa {
		num, err := strconv.Atoi(v)
		if err != nil {
			panic(err)
		}

		na = append(na, num)
	}

	sort.Ints(na)
	for i := len(na) - 1; i >= 0; i-- {
		for j := 0; j < i; j++ {
			if na[i]%na[j] == 0 {
				return na[i] / na[j]
			}
		}
	}

	return 0
}
