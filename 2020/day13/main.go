package main

import (
	"fmt"
	"io/ioutil"
	"sort"
	"strconv"
	"strings"
)

// Notes notes
type Notes struct {
	DepartTime int
	BusIDs     []int
}

// Notes2 notes
type Notes2 struct {
	DepartTime int
	BusIDs     []struct {
		id     int
		offset int
	}
}

func main() {
	r := readFile("./input.data")

	notes := parseData(r)
	result1 := solve1(notes)
	fmt.Println("Solve 1:", result1)

	notes2 := parseData2(r)
	result2 := solve2(notes2)
	// fmt.Println(notes2)
	fmt.Println("Solve 2:", result2)
}

func solve2(notes Notes2) int {
	inc := notes.BusIDs[0].id
	// the hint is from aoc so i don't just run this forever lol
	time := 102002790014590
	// time := 0

	time = (time / inc) * inc
	for !validOffset(time, notes) {
		fmt.Println("bad time", time)
		time += inc

	}

	return time
}

func crt(notes Notes2) int {
	// figure out how crt works
	// https://en.wikipedia.org/wiki/Chinese_remainder_theorem
	return 0
}

func validOffset(time int, notes Notes2) bool {
	for _, b := range notes.BusIDs {
		if (time+b.offset)%b.id != 0 {
			return false
		}
	}

	return true
}

func solve1(notes Notes) int {
	busID, minWait := 0, notes.DepartTime
	for _, id := range notes.BusIDs {
		lastStopNumber := notes.DepartTime / id
		departTime := lastStopNumber * id
		for departTime < notes.DepartTime {
			departTime += id
		}

		waitTime := departTime - notes.DepartTime
		if waitTime < minWait {
			minWait = waitTime
			busID = id
		}
	}

	return minWait * busID
}

func parseData2(lines []string) Notes2 {
	ids := []struct {
		id     int
		offset int
	}{}
	time, _ := strconv.Atoi(lines[0])

	list := strings.Split(lines[1], ",")
	for i, b := range list {
		if b == "x" {
			continue
		}

		id, _ := strconv.Atoi(b)
		ids = append(ids, struct {
			id     int
			offset int
		}{id, i})
	}

	return Notes2{time, ids}
}

func parseData(lines []string) Notes {
	ids := []int{}
	time, _ := strconv.Atoi(lines[0])

	list := strings.Split(lines[1], ",")
	for _, b := range list {
		if b == "x" {
			continue
		}

		id, _ := strconv.Atoi(b)
		ids = append(ids, id)
	}

	sort.Ints(ids)

	return Notes{time, ids}
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	return lines
}
