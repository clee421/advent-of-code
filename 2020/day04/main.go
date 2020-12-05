package main

import (
	"fmt"
	"io/ioutil"
	"reflect"
	"regexp"
	"strconv"
	"strings"
)

// PassportData passport data
type PassportData []string

// Passport passport
type Passport struct {
	BirthYear      string
	IssueYear      string
	ExpirationYear string
	Height         string
	HairColor      string
	EyeColor       string
	PassportID     string
	CountryID      string
}

// DataPair is the mapping pair from id to struct key
var DataPair map[string]string = map[string]string{
	"byr": "BirthYear",
	"iyr": "IssueYear",
	"eyr": "ExpirationYear",
	"hgt": "Height",
	"hcl": "HairColor",
	"ecl": "EyeColor",
	"pid": "PassportID",
	"cid": "CountryID",
}

func main() {
	passports := readFile("./input.data")

	result := countValidPasswords(passports)
	fmt.Println("Valid passports:", result)
}

func countValidPasswords(ps []Passport) int {
	count := 0

	for _, p := range ps {
		if isValidPassport(&p) {
			count++
		}
	}

	return count
}

func isValidPassport(p *Passport) bool {
	if p.BirthYear == "" || !isValidBirthYear(p.BirthYear) {
		return false
	}

	if p.IssueYear == "" || !isValidIssueYear(p.IssueYear) {
		return false
	}

	if p.ExpirationYear == "" || !isValidExpirationYear(p.ExpirationYear) {
		return false
	}

	if p.Height == "" || !isValidHeight(p.Height) {
		return false
	}

	if p.HairColor == "" || !isValidHairColor(p.HairColor) {
		return false
	}

	if p.EyeColor == "" || !isValidEyeColor(p.EyeColor) {
		return false
	}

	if p.PassportID == "" || !isValidPassportID(p.PassportID) {
		return false
	}

	return true
}

func isValidBirthYear(yr string) bool {
	n, err := strconv.Atoi(yr)
	if err != nil {
		return false
	}

	return 1920 <= n && n <= 2002
}

func isValidIssueYear(ir string) bool {
	n, err := strconv.Atoi(ir)
	if err != nil {
		return false
	}

	return 2010 <= n && n <= 2020
}

func isValidExpirationYear(er string) bool {
	n, err := strconv.Atoi(er)
	if err != nil {
		return false
	}

	return 2020 <= n && n <= 2030
}

func isValidHeight(h string) bool {
	l := len(h)
	if l < 3 {
		return false
	}

	t := string(h[l-2:])
	n, err := strconv.Atoi(string(h[:l-2]))
	if err != nil {
		return false
	}

	if t == "cm" {
		return 150 <= n && n <= 193
	}

	if t == "in" {
		return 59 <= n && n <= 76
	}

	return false
}

func isValidHairColor(hc string) bool {
	re := regexp.MustCompile("^#[0-9|a-f]{6}$")
	return re.MatchString(hc)
}

func isValidEyeColor(ec string) bool {
	colors := []string{"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
	for _, c := range colors {
		if c == ec {
			return true
		}
	}

	return false
}

func isValidPassportID(pid string) bool {
	re := regexp.MustCompile("^[0-9]{9}$")
	return re.MatchString(pid)
}

func parsePassportData(pd PassportData) Passport {
	p := Passport{}
	for _, d := range pd {
		dataSet := strings.Split(d, " ")

		for _, ds := range dataSet {
			pair := strings.Split(ds, ":")

			k := DataPair[pair[0]]
			reflect.ValueOf(&p).Elem().FieldByName(k).SetString(pair[1])
		}
	}

	return p
}

func readFile(filename string) []Passport {
	data, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(data), "\n")

	passports := []Passport{}

	pd := PassportData{}
	for _, l := range lines {
		if l == "" {
			p := parsePassportData(pd)
			pd = PassportData{}
			passports = append(passports, p)
			continue
		}

		pd = append(pd, l)
	}

	p := parsePassportData(pd)
	passports = append(passports, p)

	return passports
}
