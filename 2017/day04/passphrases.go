package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
)

func main() {
	f, err := os.Open("./input.txt")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	count := 0

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()
		if validPassphraseAnagram(line) {
			count++
		}
	}

	// fmt.Println("Valid passphrases (part 1): ", count)
	fmt.Println("Valid passphrases (part 2): ", count)
}

func validPassphrase(s string) bool {
	// create array of strings
	sa := strings.Split(s, " ")

	// create a set
	set := make(map[string]struct{})

	// variable for set to check exists
	var exists = struct{}{}

	for _, pass := range sa {
		if _, ok := set[pass]; ok {
			return false
		}

		set[pass] = exists
	}

	return true
}

func validPassphraseAnagram(s string) bool {
	// create array of strings
	sa := strings.Split(s, " ")

	// create a set
	set := make(map[string]struct{})

	// variable for set to check exists
	var exists = struct{}{}

	for _, pass := range sa {
		sortedPass := sortString(pass)
		if _, ok := set[sortedPass]; ok {
			return false
		}

		set[sortedPass] = exists
	}

	return true
}

func sortString(s string) string {
	r := []rune(s)
	sort.Slice(r, func(i, j int) bool {
		return r[i] < r[j]
	})
	return string(r)
}
