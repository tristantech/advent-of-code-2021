package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	f_input, err := os.Open("days/04/input-example.txt")
	if err != nil {
		panic(err)
	}
	defer f_input.Close()

	scanner := bufio.NewScanner(f_input)
	for scanner.Scan() {
	}
}