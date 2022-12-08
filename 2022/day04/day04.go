package day04

import (
	"fmt"
	"strconv"
	"strings"
)

type Runner struct{}
type Range struct {
	from int
	to   int
}
type Pair struct {
	one *Range
	two *Range
}

func CreateTask() *Runner {
	return &Runner{}
}

func parse(lines []string) []Pair {
	pairs := []Pair{}
	for _, line := range lines {
		pair := strings.Split(line, ",")
		firstPair := strings.Split(pair[0], "-")
		secondPair := strings.Split(pair[1], "-")

		a, _ := strconv.Atoi(firstPair[0])
		b, _ := strconv.Atoi(firstPair[1])
		c, _ := strconv.Atoi(secondPair[0])
		d, _ := strconv.Atoi(secondPair[1])
		pairs = append(pairs, Pair{
			one: &Range{from: a, to: b},
			two: &Range{from: c, to: d},
		})
	}

	return pairs
}

func (r *Range) Contains(other *Range) bool {
	return r.from <= other.from && other.to <= r.to
}

func (r *Range) Overlap(other *Range) bool {
	return other.from <= r.to && other.to >= r.from
}

func (r *Runner) RunPart1(lines []string) string {
	pairs := parse(lines)
	count := 0
	for _, pair := range pairs {
		if pair.one.Contains(pair.two) || pair.two.Contains(pair.one) {
			count++
		}
	}

	return fmt.Sprint("Containing pairs: ", count)
}

func (r *Runner) RunPart2(lines []string) string {
	pairs := parse(lines)
	count := 0
	for _, pair := range pairs {
		if pair.one.Overlap(pair.two) || pair.two.Overlap(pair.one) {
			count++
		}
	}

	return fmt.Sprint("Overlapping pairs: ", count)
}
