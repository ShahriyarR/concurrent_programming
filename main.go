package main

import (
	"fmt"
	"time"
	"sync"
)

func main() {
	var wg sync.WaitGroup
	wg.Add(2)
	go func() {
	    defer wg.Done()
	    process("order")
	}()

	go func() {
	    defer wg.Done()
	    process("refund")
	}()
	wg.Wait()

	process("cancel")
}

func process(item string) {
	for i := 1; i <= 5; i++ {
		fmt.Println("Processed", i, item)
		time.Sleep(time.Second) // 0.5
	}
}
