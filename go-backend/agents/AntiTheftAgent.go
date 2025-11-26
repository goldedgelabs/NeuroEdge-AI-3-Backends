// go-backend/agents/AntiTheftAgent.go
package agents

import (
    "core"
    "fmt"
    "time"
)

type AntiTheftAgent struct {
    Name string
}

func NewAntiTheftAgent() *AntiTheftAgent {
    agent := &AntiTheftAgent{Name: "AntiTheftAgent"}

    // Subscribe to DB events
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// Detect unauthorized access attempts
func (a *AntiTheftAgent) DetectTheft(collection, key string, details map[string]interface{}) map[string]interface{} {
    report := map[string]interface{}{
        "id":          fmt.Sprintf("theft_%d", time.Now().UnixMilli()),
        "collection":  collection,
        "details":     details,
        "detected_at": time.Now().String(),
    }

    // Save report to edge DB
    core.DB.Set("anti_theft_logs", report["id"].(string), report, "edge")

    // Emit DB update event concurrently
    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": "anti_theft_logs",
        "key":        report["id"],
        "value":      report,
        "source":     a.Name,
    })

    core.Log(fmt.Sprintf("[%s] Theft detected and logged → %s", a.Name, report["id"]))
    return report
}

// Handle DB update events
func (a *AntiTheftAgent) HandleDBUpdate(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB update received: %s:%s", a.Name, collection, key))
}

// Handle DB delete events
func (a *AntiTheftAgent) HandleDBDelete(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB delete received: %s:%s", a.Name, collection, key))
}

// Recover from errors
func (a *AntiTheftAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", a.Name, err))
}

func init() {
    core.RegisterAgent("AntiTheftAgent", NewAntiTheftAgent())
}
