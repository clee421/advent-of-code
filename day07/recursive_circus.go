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
	setSupport := make(map[string]bool)

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
			setSupport[support] = true

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
