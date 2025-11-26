// go-backend/agents/AutoUpdateAgent.go
package agents

import (
    "core"
    "fmt"
    "time"
)

type AutoUpdateAgent struct {
    Name string
}

func NewAutoUpdateAgent() *AutoUpdateAgent {
    agent := &AutoUpdateAgent{Name: "AutoUpdateAgent"}

    // Subscribe to DB events
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// Check and apply updates
func (a *AutoUpdateAgent) ApplyUpdate(target string, version string, changes map[string]interface{}) map[string]interface{} {
    updateRecord := map[string]interface{}{
        "id":        fmt.Sprintf("update_%d", time.Now().UnixMilli()),
        "target":    target,
        "version":   version,
        "changes":   changes,
        "appliedAt": time.Now().String(),
    }

    // Save record to edge DB
    core.DB.Set("auto_update_logs", updateRecord["id"].(string), updateRecord, "edge")

    // Emit DB update event concurrently
    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": "auto_update_logs",
        "key":        updateRecord["id"],
        "value":      updateRecord,
        "source":     a.Name,
    })

    core.Log(fmt.Sprintf("[%s] Update applied → %s", a.Name, updateRecord["id"]))
    return updateRecord
}

// Handle DB update events
func (a *AutoUpdateAgent) HandleDBUpdate(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB update received: %s:%s", a.Name, collection, key))
}

// Handle DB delete events
func (a *AutoUpdateAgent) HandleDBDelete(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB delete received: %s:%s", a.Name, collection, key))
}

// Recover from errors
func (a *AutoUpdateAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", a.Name, err))
}

func init() {
    core.RegisterAgent("AutoUpdateAgent", NewAutoUpdateAgent())
}
