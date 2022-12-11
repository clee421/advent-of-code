package day05

import (
	"fmt"
	"strconv"
	"strings"
)

type Runner struct{}
type Stack []rune
type Stacks []Stack
type Instruction struct {
	count int
	from  int
	to    int
}

func CreateTask() *Runner {
	return &Runner{}
}

func parse(lines []string) (Stacks, []Instruction) {
	textStack := []string{}

	i := 0
	for i < len(lines) {
		if lines[i] == "" {
			break
		}

		textStack = append(textStack, lines[i])
		i++
	}

	instructions := []Instruction{}
	i++
	for ; i < len(lines); i++ {
		instructions = append(instructions, parseInstruction(lines[i]))
	}

	return parseStacks(textStack), instructions
}

// Sample Input
// "    [D]"
// "[N] [C]"
// "[Z] [M] [P]"
// " 1   2   3"
func parseStacks(lines []string) Stacks {
	length := len(lines)
	stackSizeLine := lines[length-1]
	stackSize := 0
	for i := 1; i < len(stackSizeLine); i += 4 {
		stackSize, _ = strconv.Atoi(string(stackSizeLine[i]))
	}

	stacks := make([]Stack, stackSize)
	for i := length - 2; i >= 0; i-- {
		for j := 1; j < len(lines[i]); j += 4 {
			stackIndex := (j - 1) / 4
			if lines[i][j] != ' ' {
				stacks[stackIndex] = append(stacks[stackIndex], rune(lines[i][j]))
			}
		}
	}

	return stacks
}

func parseInstruction(line string) Instruction {
	splitLine := strings.Split(line, " ")
	// move 1 from 2 to 1
	// 0 .  1 2 .  3 4  5
	count, _ := strconv.Atoi(splitLine[1])
	from, _ := strconv.Atoi(splitLine[3])
	to, _ := strconv.Atoi(splitLine[5])
	return Instruction{count: count, from: from, to: to}
}

func (s *Stacks) Apply(instruct Instruction) {
	for i := 0; i < instruct.count; i++ {
		s.Move(instruct.from-1, instruct.to-1)
	}
}

func (s *Stacks) Apply2(instruct Instruction) {
	s.Move2(instruct.count, instruct.from-1, instruct.to-1)
}

func (s *Stacks) Move2(count int, from int, to int) {
	length := len((*s)[from])
	v := (*s)[from][length-count:]

	(*s)[from] = (*s)[from][:length-count]
	(*s)[to] = append((*s)[to], v...)
}

func (s *Stacks) Move(from int, to int) {
	stack, v := (*s)[from].Pop()
	(*s)[from] = stack
	(*s)[to] = append((*s)[to], v)
}

func (s *Stack) Pop() (Stack, rune) {
	last := len(*s) - 1
	r := (*s)[last]
	a := (*s)[:last]

	return a, r
}

func (s *Stacks) TopLayer() string {
	top := []string{}
	for _, stack := range *s {
		top = append(top, stack.Last())
	}

	return strings.Join(top, "")
}

func (s *Stacks) Print() {
	rows := []string{}
	for i := len(*s) - 1; i >= 0; i-- {
		row := []string{strconv.Itoa(i + 1)}
		for j := 0; j < len((*s)[i]); j++ {
			row = append(row, (*s)[i].Get(j))
		}

		v := strings.Join(row, " ")
		rows = append(rows, v)
	}

	fmt.Println("========================")
	fmt.Println(strings.Join(rows, "\n"))
	fmt.Println("========================")
}

func (s *Stack) Get(index int) string {
	if len(*s) > index {
		return string((*s)[index])
	}

	return " "
}

func (s *Stack) Last() string {
	return string((*s)[len(*s)-1])
}

func (r *Runner) RunPart1(lines []string) string {
	stacks, instructions := parse(lines)

	for _, i := range instructions {
		stacks.Apply(i)
	}

	return fmt.Sprint("top layer: ", stacks.TopLayer())
}

func (r *Runner) RunPart2(lines []string) string {
	stacks, instructions := parse(lines)

	for _, i := range instructions {
		stacks.Apply2(i)
	}

	// fmt.Println(stacks.Print())
	return fmt.Sprint("top layer: ", stacks.TopLayer())
}
