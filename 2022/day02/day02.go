package day02

import (
	"fmt"
	"strings"
)

type HandValue int
type ResultValue int

const (
	Rock HandValue = iota
	Paper
	Scissors
)

const (
	Lose ResultValue = iota
	Draw
	Win
)

type Hand struct {
	value HandValue
}

func parse(lines []string) ([]Hand, []Hand) {
	opponents := []Hand{}
	mine := []Hand{}
	for i := 0; i < len(lines); i++ {
		strat := strings.Split(lines[i], " ")
		opponents = append(opponents, getHandValue(strat[0]))
		mine = append(mine, getHandValue(strat[1]))
	}

	return opponents, mine
}

func parse2(lines []string) ([]Hand, []ResultValue) {
	hands := []Hand{}
	results := []ResultValue{}
	for i := 0; i < len(lines); i++ {
		strat := strings.Split(lines[i], " ")
		hands = append(hands, getHandValue(strat[0]))
		results = append(results, getResult(strat[1]))
	}

	return hands, results
}

func getHandValue(str string) Hand {
	if str == "A" || str == "X" {
		return Hand{value: Rock}
	}

	if str == "B" || str == "Y" {
		return Hand{value: Paper}
	}

	if str == "C" || str == "Z" {
		return Hand{value: Scissors}
	}

	fmt.Print("wtf")
	return Hand{value: Rock}
}

func getResult(str string) ResultValue {
	if str == "X" {
		return Lose
	}

	if str == "Y" {
		return Draw
	}

	if str == "Z" {
		return Win
	}

	fmt.Print("dafuq")
	return Lose
}

func (h *Hand) Value() int {
	if h.value == Paper {
		return 2
	}

	if h.value == Rock {
		return 1
	}

	if h.value == Scissors {
		return 3
	}

	fmt.Println("huh?")
	return 0
}

func handValue(v HandValue) int {
	h := Hand{v}
	return h.Value()
}

func (h *Hand) ValueOnResult(result ResultValue) int {
	if result == Draw {
		return h.Value()
	}

	if result == Lose {
		if h.value == Paper {
			return handValue(Rock)
		}

		if h.value == Rock {
			return handValue(Scissors)
		}

		return handValue(Paper)
	}

	if result == Win {
		if h.value == Paper {
			return handValue(Scissors)
		}

		if h.value == Rock {
			return handValue(Paper)
		}

		return handValue(Rock)
	}

	fmt.Println("bleh?")
	return 0
}

func (h *Hand) Shoot(other *Hand) int {
	if h.value == other.value {
		return 3
	}

	if (h.value == Rock && other.value == Scissors) || (h.value == Paper && other.value == Rock) || (h.value == Scissors && other.value == Paper) {
		return 6
	}

	return 0
}

func (r *ResultValue) Shoot() int {
	if *r == Lose {
		return 0
	}

	if *r == Draw {
		return 3
	}

	if *r == Win {
		return 6
	}

	fmt.Println("hmmm")
	return 0
}

func RunPart1(lines []string) {
	opponentHands, myHands := parse(lines)
	score := 0
	for i := 0; i < len(opponentHands); i++ {
		score = score + myHands[i].Value() + myHands[i].Shoot(&opponentHands[i])
	}

	fmt.Println("Score:", score)
}

func RunPart2(lines []string) {
	hands, results := parse2(lines)
	score := 0
	for i := 0; i < len(hands); i++ {
		score = score + hands[i].ValueOnResult(results[i]) + results[i].Shoot()
	}

	fmt.Println("Score:", score)
}
