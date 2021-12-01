package main

import (
	"bufio"
	"fmt"
	"os"
)

func parseDepth(line string) (int, bool) {
	depth := 0
	count, err := fmt.Sscanf(line, "%d", &depth)
	if count < 1 || err != nil {
		return 0, false
	}
	return depth, true
}

func part1() {
	f_input, err := os.Open("days/01/input.txt")
	if err != nil {
		panic(err)
	}
	defer f_input.Close()

	scanner := bufio.NewScanner(f_input)
	previousSonarReading := -1
	incrementCounter := 0
	for scanner.Scan() {
		depth, success := parseDepth(scanner.Text())
		if !success {
			continue
		}

		if previousSonarReading >= 0 && depth > previousSonarReading {
			incrementCounter++
		}
		previousSonarReading = depth
	}

	fmt.Printf("Part I: Number of increases: %d\n", incrementCounter)
}

func part2() {
	f_input, err := os.Open("days/01/input.txt")
	if err != nil {
		panic(err)
	}
	defer f_input.Close()

	// Ring buffer for storing last 4 readings
	ring := [4]int{0, 0, 0, 0}
	ring_ptr := 0

	scanner := bufio.NewScanner(f_input)
	incrementCounter := 0
	for scanner.Scan() {
		depth, success := parseDepth(scanner.Text())
		if !success {
			continue
		}

		// Place latest reading in to our ring buffer
		ring[ring_ptr%4] = depth
		ring_ptr++

		if ring_ptr < 4 {
			// Not enough readings to do anything yet
			continue
		}

		if ring[(ring_ptr-4)%4] < ring[(ring_ptr-1)%4] {
			// No need to actually sum anything; elements (ring_ptr-2)%4 and (ring_ptr-3)%4
			// appear on both sides and cancel out.
			incrementCounter++
		}
	}

	fmt.Printf("Part II: Number of increases: %d\n", incrementCounter)
}

func main() {
	part1()
	part2()
}
