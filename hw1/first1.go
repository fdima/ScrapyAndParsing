package main

import . "fmt"

func main() {
	const (
		_ = iota
		a
	)

	Println("привет\n")
	Println( string(a))
}
