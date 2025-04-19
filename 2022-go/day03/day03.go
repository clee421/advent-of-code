package day03

import (
	"fmt"
	"os"
)

const GroupLimit = 3

type Runner struct{}
type Item rune
type Compartment struct {
	items map[Item]bool
}
type Rucksack struct {
	one Compartment
	two Compartment
}
type Group struct {
	rucksacks []Rucksack
}

func CreateTask() *Runner {
	return &Runner{}
}

func CreateCompartment(text string) Compartment {
	c := map[Item]bool{}
	for i := 0; i < len(text); i++ {
		c[Item(text[i])] = true
	}
	return Compartment{c}
}

func (c *Compartment) Difference(other *Compartment) *Compartment {
	m := map[Item]bool{}
	for item, _ := range c.items {
		if _, ok := other.items[item]; ok {
			m[item] = true
		}
	}

	return &Compartment{m}
}

func (c *Item) Value() int {
	if int(*c) >= 97 {
		return int(*c) - 96
	}

	return int(*c) - 64 + 26
}

func (r *Rucksack) Contains(i Item) bool {
	_, ok := r.one.items[i]
	if ok {
		return ok
	}

	_, ok = r.two.items[i]
	return ok
}

func (g *Group) Badge() int {
	// cheating because i know there are 3 items each
	one := g.rucksacks[0]
	two := g.rucksacks[1]
	three := g.rucksacks[2]

	a := 97
	A := 65
	z := 122
	Z := 90
	for ascii := A; ascii <= z; ascii++ {
		if ascii > Z && ascii < a {
			// ignore the symbols
			continue
		}

		item := Item(ascii)
		if one.Contains(item) && two.Contains(item) && three.Contains(item) {
			return item.Value()
		}
	}

	// shouldn't happen but ya
	fmt.Println("no no no")
	return 0
}

func parse(lines []string) []Rucksack {
	rucksacks := []Rucksack{}
	for i := 0; i < len(lines); i++ {
		mid := (len(lines[i]) / 2)
		first := lines[i][0:mid]
		last := lines[i][mid:]

		rucksacks = append(rucksacks, Rucksack{
			one: CreateCompartment(first),
			two: CreateCompartment(last),
		})
	}

	return rucksacks
}

func parseGroups(rucksacks []Rucksack) []Group {
	groups := []Group{}
	for i := 0; i < len(rucksacks); i += GroupLimit {
		r := []Rucksack{}
		for j := 0; j < GroupLimit; j++ {
			r = append(r, rucksacks[i+j])
		}

		groups = append(groups, Group{rucksacks: r})
	}

	return groups
}

func (r *Runner) RunPart1(lines []string) string {
	rucksacks := parse(lines)
	priority := 0
	for i := 0; i < len(rucksacks); i++ {
		diff := rucksacks[i].one.Difference(&rucksacks[i].two)
		if len(diff.items) > 1 {
			os.Exit(1)
		}

		for item, _ := range diff.items {
			// should only be one item
			// 'a' starts at 97 and we need it to be 1
			// fmt.Println(string(item), item.Value())
			priority += item.Value()
		}
	}

	return fmt.Sprint("Priority: ", priority)
}

func (r *Runner) RunPart2(lines []string) string {
	rucksacks := parse(lines)
	groups := parseGroups(rucksacks)

	priority := 0
	for i := 0; i < len(groups); i++ {
		priority += groups[i].Badge()
	}

	return fmt.Sprint("Priority: ", priority)
}
