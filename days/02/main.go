package main

import (
	"bufio"
	"fmt"
	"os"
)

func parseCommand(line string) (string, int, bool) {
	var distance int
	var direction string

	count, err := fmt.Sscanf(line, "%s %d", &direction, &distance)
	if count < 2 || err != nil {
		return "", 0, false
	}
	return direction, distance, true
}

func main() {
	f_input, err := os.Open("days/02/input.txt")
	if err != nil {
		panic(err)
	}
	defer f_input.Close()

	var x, part1_y, part2_y, aim int
	scanner := bufio.NewScanner(f_input)
	for scanner.Scan() {
		direction, distance, success := parseCommand(scanner.Text())
		if !success {
			continue
		}

		switch direction {
		case "forward":
			x += distance
			part2_y += distance * aim
			break
		case "up":
			part1_y -= distance
			aim -= distance
			break
		case "down":
			part1_y += distance
			aim += distance
			break
		default:
			panic("Unknown command")
		}
	}

	fmt.Printf("Part I: %d\n", x*part1_y)
	fmt.Printf("Part II: %d\n", x*part2_y)
}
