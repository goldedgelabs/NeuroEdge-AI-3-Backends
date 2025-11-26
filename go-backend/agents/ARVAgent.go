package agents

import (
    "core"
    "time"
)

// ARVAgent handles ARV-specific processing tasks
type ARVAgent struct{}

// Handle processes incoming tasks
func (a *ARVAgent) Handle(task map[string]interface{}) map[string]interface{} {
    core.Log("[ARVAgent] Handling task...")

    id := "unknown"
    if val, ok := task["id"].(string); ok {
        id = val
    }

    result := map[string]interface{}{
        "collection": "arv_data",
        "id":         id,
        "payload":    task,
        "timestamp":  time.Now(),
    }

    // Save to edge DB
    core.DB.Set("arv_data", id, result, "edge")

    // Publish DB update event
    core.Bus.Publish("db:update", map[string]interface{}{
        "collection": "arv_data",
        "key":        id,
        "value":      result,
        "source":     "ARVAgent",
    })

    core.Log("[ARVAgent] Task processed and saved to DB: " + id)
    return result
}

// Register agent automatically
func init() {
    core.RegisterAgent("ARVAgent", &ARVAgent{})
}
