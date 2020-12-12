package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

// BagRule is the rule for a bag
type BagRule struct {
	Color    string
	Contains []struct {
		Color string
		Count int
	}
}

// BagNode keeps track of the child to parent relationship
type BagNode struct {
	Color   string
	Parents []string
}

func main() {
	r := readFile("./input.data")
	rules := parseData(r)
	parents := buildParentGraph(rules)
	count := countParentsHierachy(parents, "shiny gold")

	fmt.Println("Parent count for shiny gold bag is:", count)

	count = countChildrenHierachy(rules, "shiny gold")
	fmt.Println("Child count for shiny gold bag is:", count)
}

func countChildrenHierachy(g map[string]*BagRule, start string) int {
	type Rule struct {
		Color string
		Count int
	}

	sum := 0
	queue := []Rule{Rule{start, 1}}

	for len(queue) > 0 {
		rule := queue[0]
		queue = queue[1:]

		if node, ok := g[rule.Color]; ok {
			// fmt.Println("Current color", rule.Color)
			for _, c := range node.Contains {
				// fmt.Printf("Has %d x %d %s bag(s)\n", rule.Count, c.Count, c.Color)
				count := rule.Count * c.Count
				sum += count

				// fmt.Println("Sum:", sum)
				queue = append(queue, Rule{c.Color, (rule.Count * c.Count)})
			}
		}
	}

	return sum
}

func countParentsHierachy(g map[string]*BagNode, target string) int {
	seen := map[string]bool{}
	queue := []string{target}

	for len(queue) > 0 {
		color := queue[0]
		queue = queue[1:]

		// fmt.Println("My target is:", color)
		if node, ok := g[color]; ok {
			// fmt.Println("Has parents:", node.Parents)

			for _, p := range node.Parents {
				seen[p] = true
				queue = append(queue, p)
			}
		}
	}

	return len(seen)
}

func buildParentGraph(rules map[string]*BagRule) map[string]*BagNode {
	graph := map[string]*BagNode{}
	for _, r := range rules {
		for _, child := range r.Contains {
			if _, ok := graph[child.Color]; !ok {
				graph[child.Color] = &BagNode{child.Color, []string{}}
			}

			graph[child.Color].Parents = append(graph[child.Color].Parents, r.Color)
		}
	}

	return graph
}

func parseData(d []string) map[string]*BagRule {
	rules := map[string]*BagRule{}

	for _, l := range d {
		rule := BagRule{}

		s := strings.Split(l, " bags contain ")
		rule.Color = s[0]

		// fmt.Println("Color:", rule.Color)

		if s[1] == "no other bags." {
			rules[rule.Color] = &rule
			continue
		}

		// 1 bright white bag, 2 muted yellow bags.
		// strips the .
		s[1] = s[1][:len(s[1])-1]
		contains := strings.Split(s[1], ", ")
		for _, r := range contains {
			// 1 bright white bag
			text := strings.Split(r, " ")
			n, err := strconv.Atoi(text[0])
			if err != nil {
				panic(fmt.Sprintf("%s; failed to parse", r))
			}

			color := strings.Join(text[1:len(text)-1], " ")
			rule.Contains = append(rule.Contains, struct {
				Color string
				Count int
			}{color, n})

			rules[rule.Color] = &rule
			// fmt.Println("  Contains:", n, color)
		}
	}

	return rules
}

func readFile(filename string) []string {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	return lines
}
