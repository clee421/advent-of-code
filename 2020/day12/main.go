package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

// Instruction instruction
type Instruction struct {
	action byte
	value  int
}

// Ship ship
type Ship struct {
	direction byte
	east      int
	north     int
}

func (s *Ship) distance() int {
	return abs(s.east) + abs(s.north)
}

func (s *Ship) move(in Instruction) bool {
	switch in.action {
	case 'N':
		// fmt.Println("north instructions", in.value)
		s.north += in.value
	case 'S':
		// fmt.Println("south instructions", in.value)
		s.north -= in.value
	case 'E':
		// fmt.Println("east instructions", in.value)
		s.east += in.value
	case 'W':
		// fmt.Println("west instructions", in.value)
		s.east -= in.value
	case 'F':
		// fmt.Println("forward instructions", in.value)
		s.move(Instruction{s.direction, in.value})
	case 'L':
		s.update(in.action, in.value)
	case 'R':
		s.update(in.action, in.value)
	default:
		// fmt.Println("holy crap a wrong instruction")
		panic(1)
	}

	return true
}

func (s *Ship) update(direction byte, degrees int) {
	order := []byte{'N', 'E', 'S', 'W'}
	dirs := map[byte]int{'N': 0, 'E': 1, 'S': 2, 'W': 3}

	offset := degrees / 90
	cd := dirs[s.direction]

	var nd int
	switch direction {
	case 'R':
		// fmt.Println("right instructions", degrees)
		nd = (cd + offset)
	case 'L':
		// fmt.Println("left instructions", degrees)
		nd = ((cd - offset) % 4) + 4
	}

	nd = nd % 4

	// fmt.Println("Old direction", string(s.direction), "rotating", degrees, "degrees", string(direction), "to get", string(order[nd]))
	s.direction = order[nd]
}

func main() {
	r := readFile("./input.data")
	ins := parseInstructions(r)

	result1 := solve1(ins)
	fmt.Println("Total distance:", result1)
}

func solve1(instructions []Instruction) int {
	ship := Ship{direction: 'E'}
	for _, in := range instructions {
		ok := ship.move(in)
		if !ok {
			fmt.Println("some intruction blew up")
		}

		// fmt.Println(i, "current value", ship.distance())
	}

	// fmt.Println(ship.north, ship.east)

	return ship.distance()
}

func parseInstructions(lines []string) []Instruction {
	instructions := []Instruction{}
	for _, l := range lines {
		in := Instruction{
			action: l[0],
		}

		v, _ := strconv.Atoi(l[1:])
		if (in.action == 'L' || in.action == 'R') && v%90 != 0 {
			fmt.Println("this is not a right angle turn")
			panic(1)
		}

		in.value = v
		instructions = append(instructions, in)
	}

	return instructions
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	return lines
}

func abs(n int) int {
	if n < 0 {
		return -n
	}

	return n
}
