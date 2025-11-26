// app.go
package main

import (
    "log"
    "net/http"
    "github.com/gorilla/mux"
    "core"
)

func RunEngineHandler(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    name := vars["name"]
    // Parse JSON body
    var payload map[string]interface{}
    err := json.NewDecoder(r.Body).Decode(&payload)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    result := core.RunEngine(name, payload)
    json.NewEncoder(w).Encode(result)
}

func RunAgentHandler(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    name := vars["name"]
    var task map[string]interface{}
    err := json.NewDecoder(r.Body).Decode(&task)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    result := core.RunAgent(name, task)
    json.NewEncoder(w).Encode(result)
}

func main() {
    r := mux.NewRouter()
    r.HandleFunc("/engine/{name}/run", RunEngineHandler).Methods("POST")
    r.HandleFunc("/agent/{name}/task", RunAgentHandler).Methods("POST")
    log.Println("NeuroEdge Go backend running on :8080")
    http.ListenAndServe(":8080", r)
}
