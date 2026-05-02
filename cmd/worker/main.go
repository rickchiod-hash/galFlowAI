package main

import (
	"fmt"
	"time"
)

func main() {
	fmt.Println("galFlowAI Worker - Processando jobs...")
	for {
		fmt.Println("Verificando fila de jobs...")
		time.Sleep(10 * time.Second)
	}
}
