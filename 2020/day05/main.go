package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

// SeatingInfo seating ifo
type SeatingInfo struct {
	id  int
	row int
	col int
}

// ID of seating info
func (si SeatingInfo) ID() int {
	return si.id
}

// Seats array of seating info
type Seats []SeatingInfo

func main() {
	r := readFile("./input.data")
	seats := parseRawData(r)

	fmt.Println("Max ID found:", seats.MaxID())
	fmt.Println("My seat:", seats.MissingID())
}

// MaxID is the highest int of id
func (s Seats) MaxID() int {
	max := 0
	for _, seat := range s {
		if seat.ID() > max {
			max = seat.ID()
		}
	}

	return max
}

// MissingID is missing id in the list
func (s Seats) MissingID() int {
	// 864 was the max id found
	min, max := 864, 0
	seen := map[int]bool{}
	for _, seat := range s {
		if seat.ID() > max {
			max = seat.ID()
		}

		if seat.ID() < min {
			min = seat.ID()
		}

		seen[seat.ID()] = true
	}

	for n := min; n <= max; n++ {
		if seen[n-1] && seen[n+1] && !seen[n] {
			return n
		}
	}

	return -1
}

func parseRawData(d []string) Seats {
	seatings := []SeatingInfo{}
	for _, rd := range d {
		si := parseEncodedSeat(rd)
		seatings = append(seatings, si)
	}

	return seatings
}

func parseEncodedSeat(es string) SeatingInfo {
	row := parseRow(es[:7])
	col := parseColumn(es[7:])
	id := row*8 + col

	return SeatingInfo{id, row, col}
}

func bSearch(rd string, start int, end int, t1 byte, t2 byte) int {
	var m int
	s, e := start, end
	for i := 0; i < len(rd); i++ {
		m = (s + e) / 2

		switch rd[i] {
		case t1:
			e = m
		case t2:
			s = m + 1
		default:
			panic(fmt.Sprintf("Unrecognized row type %s", string(rd[i])))
		}
	}

	return (s + e) / 2
}

func parseRow(rd string) int {
	return bSearch(rd, 0, 127, 'F', 'B')
}

func parseColumn(cd string) int {
	return bSearch(cd, 0, 7, 'L', 'R')
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	return lines
}
