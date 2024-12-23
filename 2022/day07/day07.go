package day07

import (
	"fmt"
)

type Runner struct{}

func CreateTask() *Runner {
	return &Runner{}
}

func (r *Runner) RunPart1(lines []string) string {
	return fmt.Sprint("hello world")
}

func (r *Runner) RunPart2(lines []string) string {
	return fmt.Sprint("hello world")
}
