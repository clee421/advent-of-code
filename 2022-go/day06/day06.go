package day06

import (
	"fmt"
)

type Runner struct{}
type PacketDectector struct {
	size     int
	buffer   []rune
	location int
}

func CreateTask() *Runner {
	return &Runner{}
}

func (pd *PacketDectector) Add(r rune) {
	if len(pd.buffer) >= pd.size {
		pd.buffer = pd.buffer[1:]
	}

	pd.location += 1
	pd.buffer = append(pd.buffer, r)
}

func (pd *PacketDectector) HaveMarker() bool {
	counter := map[rune]bool{}
	for _, r := range pd.buffer {
		counter[r] = true
	}

	return len(counter) == pd.size
}

func (pd *PacketDectector) MarkerLocation() int {
	return pd.location
}

func (r *Runner) RunPart1(lines []string) string {
	code := lines[0]
	pd := &PacketDectector{size: 4, buffer: []rune{}}
	for _, c := range code {
		pd.Add(c)
		if pd.HaveMarker() {
			break
		}
	}

	return fmt.Sprint("first marker after ", pd.MarkerLocation())
}

func (r *Runner) RunPart2(lines []string) string {
	code := lines[0]
	pd := &PacketDectector{size: 14, buffer: []rune{}}
	for _, c := range code {
		pd.Add(c)
		if pd.HaveMarker() {
			break
		}
	}

	return fmt.Sprint("first marker after ", pd.MarkerLocation())
}
