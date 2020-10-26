package main

import (
	"fmt"
	"time"
)

func main() {
	c := make(chan string)
	go process("order", c)
	for item := range(c) {
	    fmt.Println("Processed", item)
	}

}

func process(item string, c chan string) {
	for i := 1; i <= 5; i++ {
	    fmt.Println("Put the", item)
	    c <- item
		time.Sleep(time.Second / 2) // 0.5
	}
	close(c)
}
