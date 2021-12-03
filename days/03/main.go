package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func mostCommonBit(lines map[string]bool, pos int) byte {
	var count0, count1 int

	for k, _ := range lines {
		if k[pos] == '1' {
			count1++
		} else {
			count0++
		}
	}
	if count1 >= count0 {
		return '1'
	} else {
		return '0'
	}
}

func part1(lines map[string]bool, numBits int) {
	gamma := 0
	epsilon := 0
	for i := 0; i < numBits; i++ {
		if mostCommonBit(lines, i) == '1' {
			// 1 is more common
			gamma |= (1 << (numBits - i - 1))
		} else {
			// 1 is less common
			epsilon |= (1 << (numBits - i - 1))
		}
	}

	fmt.Printf("Part I: %d * %d = %d\n", gamma, epsilon, epsilon*gamma)
}

func part2(lines map[string]bool, numBits int) {
	// Make two copies of the set, one for O2 and the
	// other for CO2, since we will be destructive.
	all_lines_co2 := make(map[string]bool)
	all_lines_o2 := make(map[string]bool)
	for k, v := range lines {
		all_lines_co2[k] = v
		all_lines_o2[k] = v
	}

	for i := 0; i < numBits; i++ {
		// Oxygen
		most_common := mostCommonBit(all_lines_o2, i)

		// Delete all where bit i is NOT most_common
		for k, _ := range all_lines_o2 {
			if k[i] != most_common {
				delete(all_lines_o2, k)
			}
		}

		if len(all_lines_o2) == 1 {
			break
		}
	}

	for i := 0; i < numBits; i++ {
		// CO2
		most_common := mostCommonBit(all_lines_co2, i)

		// Delete all where bit i is most_common
		for k, _ := range all_lines_co2 {
			if k[i] == most_common {
				delete(all_lines_co2, k)
			}
		}

		if len(all_lines_co2) == 1 {
			break
		}

	}

	// Pull out remaining line from each set and convert to ints
	var o2, co2 int64
	for k, _ := range all_lines_co2 {
		co2, _ = strconv.ParseInt(k, 2, 64)
	}
	for k, _ := range all_lines_o2 {
		o2, _ = strconv.ParseInt(k, 2, 64)
	}

	fmt.Printf("Part II: %d * %d = %d\n", o2, co2, co2*o2)
}

func main() {
	f_input, err := os.Open("days/03/input.txt")
	if err != nil {
		panic(err)
	}
	defer f_input.Close()

	lines := make(map[string]bool)

	scanner := bufio.NewScanner(f_input)
	numBits := 0
	for scanner.Scan() {
		line := scanner.Text()
		numBits = len(line)
		lines[line] = true
	}

	part1(lines, numBits)
	part2(lines, numBits)
}
