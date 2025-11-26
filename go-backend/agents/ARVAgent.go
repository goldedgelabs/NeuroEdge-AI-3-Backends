// go-backend/agents/ARVAgent.go
package agents

import (
    "core"
    "fmt"
)

type ARVAgent struct {
    Name string
}

func NewARVAgent() *ARVAgent {
    agent := &ARVAgent{Name: "ARVAgent"}

    // Subscribe to DB events
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// Process and store ARV data
func (a *ARVAgent) ProcessARVData(collection, key string, data map[string]interface{}) map[string]interface{} {
    record := map[string]interface{}{
        "id":         key,
        "collection": collection,
        "payload":    data,
    }

    // Save record in edge DB
    core.DB.Set(collection, key, record, "edge")

    // Emit DB update event concurrently
    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": collection,
        "key":        key,
        "value":      record,
        "source":     a.Name,
    })

    core.Log(fmt.Sprintf("[%s] DB updated → %s:%s", a.Name, collection, key))
    return record
}

// Handle DB update events
func (a *ARVAgent) HandleDBUpdate(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB update received: %s:%s", a.Name, collection, key))
}

// Handle DB delete events
func (a *ARVAgent) HandleDBDelete(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB delete received: %s:%s", a.Name, collection, key))
}

// Recover from errors
func (a *ARVAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", a.Name, err))
}

func init() {
    core.RegisterAgent("ARVAgent", NewARVAgent())
}
