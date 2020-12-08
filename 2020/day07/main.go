package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

// BagRule is the rule for a bag
type BagRule struct {
	Color    string
	Contains []struct {
		Color string
		Count int
	}
}

func main() {
	r := readFile("./test.data")
	rules := parseData(r)

	fmt.Println(rules)
}

func parseData(d []string) []BagRule {
	rules := []BagRule{}

	for _, l := range d {
		rule := BagRule{}

		s := strings.Split(l, " bags contain ")
		rule.Color = s[0]

		// fmt.Println("Color:", rule.Color)

		if s[1] == "no other bags." {
			rules = append(rules, rule)
			continue
		}

		// 1 bright white bag, 2 muted yellow bags.
		// strips the .
		s[1] = s[1][:len(s[1])-1]
		contains := strings.Split(s[1], ", ")
		for _, r := range contains {
			// 1 bright white bag
			text := strings.Split(r, " ")
			n, err := strconv.Atoi(text[0])
			if err != nil {
				panic(fmt.Sprintf("%s; failed to parse", r))
			}

			color := strings.Join(text[1:len(text)-1], " ")
			rule.Contains = append(rule.Contains, struct {
				Color string
				Count int
			}{color, n})

			rules = append(rules, rule)
			// fmt.Println("  Contains:", n, color)
		}
	}

	return rules
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	return lines
}
