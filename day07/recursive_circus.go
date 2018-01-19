package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type program struct {
	name   string
	weight int
}

// Part 1 Solution: gmcrj // OK
func main() {
	file := "input.txt"
	f, err := os.Open(fmt.Sprintf("./%v", file))
	if err != nil {
		panic(err)
	}

	// A set of supports
	setSupport := make(map[string][]string)

	// A set of peaple that stand on supports
	setStand := make(map[string]bool)

	// A set of program's and weight
	setProgram := make(map[string]int)

	// Process the input
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()

		// parse each line as your read it
		support, stand, p := parseLine(line)

		// only lines that are supporting people are recorded
		if support != "" {
			setSupport[support] = stand

			for _, s := range stand {
				setStand[s] = true
			}
		}

		// store each program's name and weight
		setProgram[p.name] = p.weight
	}

	root := "nobody"
	// The support at the root of this tree is the
	// supporter that is not a stander
	for k := range setSupport {
		if !setStand[k] {
			root = k
			break
		}
	}

	fmt.Println("This root supporter is", root)

	name, weight, _ := findOffWeightProgram(root, &setSupport, &setProgram)
	fmt.Println("Program", name, "needs to be", weight)
}

// Either one of these formats are accepted as part of the line
// ktlj (57)
// fwft (72) -> ktlj, cntj, xhth
// do not clean input here
func parseLine(line string) (string, []string, program) {
	sa := strings.Split(line, " -> ")

	// sa looks like this now
	// [fwft (72), ktlj, cntj, xhth]
	pa := strings.Split(sa[0], " ")
	re := regexp.MustCompile("([0-9]+)")
	ws := re.FindString(pa[1])
	wi, _ := strconv.Atoi(ws)
	if len(sa) < 2 {
		return "", []string{}, program{pa[0], wi}
	}

	support := pa[0]
	stand := strings.Split(sa[1], ", ")

	return support, stand, program{pa[0], wi}
}

func findOffWeightProgram(name string, support *map[string][]string, program *map[string]int) (string, int, bool) {
	// dereference to index in
	supp := *support
	prog := *program

	// get children
	children, exist := supp[name]

	// If the name does not exist then this program is a standee only
	// and thus this is the base case. Return true to tell parent
	// that everything is ok and the weight is valid
	if !exist {
		return "", prog[name], true
	}

	// store children and their total weight supported
	mapChildren := make(map[string]int)

	for _, child := range children {
		n, w, ok := findOffWeightProgram(child, support, program)

		// If not ok then that means the off weight program was found
		if !ok {
			return n, w, ok
		}

		// Otherwise we store all the children and their weights
		// and check if any child is the off weight one
		mapChildren[child] = w
	}

	// fmt.Println("______________________________")
	// fmt.Println("Parent:", name)
	// fmt.Println("Children:", mapChildren)

	n, w, ok := checkOffWeight(&mapChildren, program)

	// If one of the children is off weight then the
	// weight it should be and the name will be returned
	// and it will not be ok
	if !ok {
		return n, w, ok
	}

	// Otherwise every thing is good and we'll sum the children's
	// weight and add this programs weight
	sum := 0
	for _, w := range mapChildren {
		sum += w
	}

	return name, sum + prog[name], true
}

func checkOffWeight(mc *map[string]int, p *map[string]int) (string, int, bool) {
	mapChildren := *mc
	mapProgram := *p

	count := make(map[int]int)
	for _, w := range mapChildren {
		count[w]++
	}

	// Means everybody is equal and it's all ok
	if len(count) == 1 {
		return "", 0, true
	}

	// Otherwise it's not all ok and it's time to find the off weight
	var offWeight, correctWeight int
	for weight, c := range count {
		// one of the weights is will be off
		if c == 1 {
			offWeight = weight
		}

		// need to know correct weight
		if c > 1 {
			correctWeight = weight
		}
	}

	// fmt.Println("************************")
	// fmt.Println("Count:", count)
	// fmt.Println("Correct weight:", correctWeight)
	// fmt.Println("Off weight:", offWeight)

	// get the program that has the off weight
	var name string
	for n, w := range mapChildren {
		if w == offWeight {
			name = n
			break
		}
	}

	// Calculate the new weight the program needs to be
	diff := correctWeight - offWeight
	newWeight := mapProgram[name] + diff

	// fmt.Println("Difference:", diff)
	// fmt.Println("New weight:", newWeight)

	return name, newWeight, false
}
