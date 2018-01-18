package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

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

	// Process the input
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()

		// parse each line as your read it
		support, stand := parseLine(line)

		// only lines that are supporting people are recorded
		if support != "" {
			setSupport[support] = true

			for _, s := range stand {
				setStand[s] = true
			}
		}
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
func parseLine(line string) (string, []string) {
	sa := strings.Split(line, " -> ")
	if len(sa) < 2 {
		return "", []string{}
	}

	// sa looks like this now
	// [fwft (72), ktlj, cntj, xhth]
	support := strings.Split(sa[0], " ")[0]
	stand := strings.Split(sa[1], ", ")

	return support, stand
}
