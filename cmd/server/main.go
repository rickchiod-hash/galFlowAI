package main

import (
	"fmt"
	"net/http"
)

func main() {
	fmt.Println("galFlowAI Server - Etapa 1 (Backend Go)")
	fmt.Println("Servindo frontend/ em http://localhost:7860")
	http.Handle("/", http.FileServer(http.Dir("../../frontend")))
	http.HandleFunc("/api/hardware", hardwareHandler)
	http.ListenAndServe(":7860", nil)
}

func hardwareHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, `{"gpu": "NVIDIA GTX 1660 Super", "vram_gb": 6.44}`)
}
