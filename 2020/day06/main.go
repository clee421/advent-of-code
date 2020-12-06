package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

// Group group
type Group []Person

// Person person
type Person struct {
	Answers []byte
}

func main() {
	r := readFile("./input.data")
	groups := parseData(r)
	result1 := solve1(groups)
	fmt.Println("Sum of counts:", result1)

	result2 := solve2(groups)
	fmt.Println("Sum of counts(correct):", result2)
}

func solve1(groups []Group) int {
	sum := 0
	for _, g := range groups {
		seen := map[byte]bool{}

		for _, p := range g {
			for _, c := range p.Answers {
				seen[c] = true
			}
		}
		sum += len(seen)
	}

	return sum
}

func solve2(groups []Group) int {
	sum := 0
	for _, g := range groups {
		seen := map[byte]int{}

		for _, p := range g {
			for _, c := range p.Answers {
				seen[c]++

				if seen[c] == len(g) {
					sum++
				}
			}
		}
	}

	return sum
}

func parseData(d []string) []Group {
	groups := []Group{}

	g := []string{}
	for _, l := range d {
		if l == "" {
			groups = append(groups, parseGroup(g))
			g = []string{}
			continue
		}

		g = append(g, l)
	}

	groups = append(groups, parseGroup(g))

	return groups
}

func parseGroup(d []string) Group {
	g := Group{}
	for _, l := range d {
		g = append(g, parsePerson(l))
	}

	return g
}

func parsePerson(d string) Person {
	p := Person{}
	for i := 0; i < len(d); i++ {
		p.Answers = append(p.Answers, d[i])
	}

	return p
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	return lines
}
