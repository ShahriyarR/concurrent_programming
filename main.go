package main

import (
	"fmt"
	"time"
)

func main() {
    out1 := make(chan string)
    out2 := make(chan string)
    done := make(chan int)

    go func(){
        for i := 1; i <=5; i++ {
            time.Sleep(time.Second / 2)
            out1 <- "order processed"
        }
        done <- 1
    }()

    go func() {
        for i := 1; i <=5; i++ {
            time.Sleep(time.Second)
            out2 <- "refund processed"
        }
        done <- 1
    }()

    for n:=2; n>0;  {
        select {
            case msg := <- out1:
                fmt.Println(msg)
            case msg := <- out2:
                fmt.Println(msg)
            case <-done:
                n--
        }
    }


//         fmt.Println(<-out1)
//         fmt.Println(<-out2)
//     }

}