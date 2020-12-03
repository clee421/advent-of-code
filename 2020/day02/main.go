package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

// PassWordPolicy struct
type PassWordPolicy struct {
	min  int
	max  int
	chr  byte
	text string
}

func main() {
	pws := readFile("./input.data")

	result1 := validPasswords1(pws)
	fmt.Println("Valid password:", result1)

	result2 := validPasswords2(pws)
	fmt.Println("Valid password:", result2)
}

func validPasswords1(pws []PassWordPolicy) int {
	valid := 0
	for _, p := range pws {
		c := 0
		for i := 0; i < len(p.text); i++ {
			if p.chr == p.text[i] {
				c++
			}
		}

		if p.min <= c && c <= p.max {
			valid++
		}
	}

	return valid
}

func validPasswords2(pws []PassWordPolicy) int {
	valid := 0
	for _, p := range pws {
		idx1 := p.min - 1
		idx2 := p.max - 1

		c1 := p.text[idx1] == p.chr
		c2 := p.text[idx2] == p.chr

		if c1 != c2 {
			valid++
		}
	}

	return valid
}

func readFile(filename string) []PassWordPolicy {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	pws := []PassWordPolicy{}
	for _, l := range lines {

		// [1-3,  a:, abcde]
		p := strings.Split(l, " ")

		// [1, 3]
		limits := strings.Split(p[0], "-")

		// a
		char := p[1][0]

		min, err := strconv.Atoi(limits[0])
		if err != nil {
			continue
		}

		max, err := strconv.Atoi(limits[1])
		if err != nil {
			continue
		}

		pws = append(pws, PassWordPolicy{
			min:  min,
			max:  max,
			chr:  char,
			text: p[2],
		})
	}

	return pws
}
