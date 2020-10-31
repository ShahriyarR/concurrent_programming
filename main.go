package main

import (
	"fmt"
	"time"
	"sync"
)

type item struct {
    price int
    category string
}

func main() {
    c := gen(
        item{8, "shirt"},
        item{20, "shoe"},
        item{24, "shoe"},
        item{4, "drink"},
    )
    c1 := discount(c)
    c2 := discount(c)
    out := fanIn(c1, c2)
    for processed := range out {
//         fmt.Println("Category:", processed.category, "Price:", processed.price)
        fmt.Println(processed)

    }
}


func gen(items ...item) <-chan item {
    out := make(chan item, len(items))
    for _, i := range items {
        out <- i
    }
    close(out)
    return out
}


func discount(items <-chan item) <-chan item {
    out := make(chan item)
    go func() {
        defer close(out)
        for i := range items {
            time.Sleep(time.Second)
            // We have a sale going on
            // Shoes are half off!
            if i.category == "shoe" {
                i.price /= 2
            }
            out <- i
        }
    }()
    return out
}

func fanIn(channels ...<-chan item) <-chan item {
    var wg sync.WaitGroup
    out := make(chan item)
    output := func(c <-chan item) {
        defer wg.Done()
        for i := range c {
            out <- i
        }
    }
    wg.Add(len(channels))
    for _, c := range channels {
        go output(c)
    }

    go func() {
        wg.Wait()
        close(out)
    }()
    return out
}

