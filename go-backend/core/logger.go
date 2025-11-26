// core/logger.go
package core

import (
    "log"
    "time"
)

func Log(msg string) {
    log.Printf("[NeuroEdge] %s %s", time.Now().Format(time.RFC3339), msg)
}

func Error(msg string) {
    log.Printf("[NeuroEdge][ERROR] %s %s", time.Now().Format(time.RFC3339), msg)
}
