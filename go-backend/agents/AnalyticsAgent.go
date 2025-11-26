package agents

import (
    "core"
    "time"
)

// AnalyticsAgent performs analytics on incoming data
type AnalyticsAgent struct{}

// Handle processes incoming tasks
func (a *AnalyticsAgent) Handle(task map[string]interface{}) map[string]interface{} {
    core.Log("[AnalyticsAgent] Handling task...")

    folder := "unknown"
    if val, ok := task["folder"].(string); ok {
        folder = val
    }

    role := "user"
    if val, ok := task["role"].(string); ok {
        role = val
    }

    // Example analytics processing: simple summary
    data, _ := task["data"].([]interface{})
    summary := map[string]interface{}{
        "count":     len(data),
        "sample":    data,
        "folder":    folder,
        "role":      role,
        "timestamp": time.Now(),
    }

    // Save to DB
    recordID := folder + "_" + role + "_" + time.Now().Format("20060102150405")
    core.DB.Set("analytics_results", recordID, summary, "edge")

    // Emit DB update event
    core.Bus.Publish("db:update", map[string]interface{}{
        "collection": "analytics_results",
        "key":        recordID,
        "value":      summary,
        "source":     "AnalyticsAgent",
    })

    core.Log("[AnalyticsAgent] Task processed and saved to DB: " + recordID)
    return summary
}

// Register agent automatically
func init() {
    core.RegisterAgent("AnalyticsAgent", &AnalyticsAgent{})
}
