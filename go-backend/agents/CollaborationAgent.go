// go-backend/agents/CollaborationAgent.go
package agents

import (
    "core"
    "fmt"
    "time"
)

type CollaborationAgent struct {
    Name string
}

func NewCollaborationAgent() *CollaborationAgent {
    agent := &CollaborationAgent{Name: "CollaborationAgent"}

    // Subscribe to DB events
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// Create a collaboration workspace
func (c *CollaborationAgent) CreateWorkspace(workspaceID string, members []string, meta map[string]interface{}) map[string]interface{} {
    record := map[string]interface{}{
        "id":        workspaceID,
        "members":   members,
        "meta":      meta,
        "createdAt": time.Now().String(),
    }

    // Save to edge DB
    core.DB.Set("collaboration", workspaceID, record, "edge")

    // Publish DB update event
    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": "collaboration",
        "key":        workspaceID,
        "value":      record,
        "source":     c.Name,
    })

    core.Log(fmt.Sprintf("[%s] Workspace created → %s", c.Name, workspaceID))
    return record
}

// Add member to existing workspace
func (c *CollaborationAgent) AddMember(workspaceID string, memberID string) map[string]interface{} {
    record := core.DB.Get("collaboration", workspaceID, "edge")
    if record == nil {
        core.Log(fmt.Sprintf("[%s] Workspace not found: %s", c.Name, workspaceID))
        return nil
    }

    members := record["members"].([]string)
    members = append(members, memberID)
    record["members"] = members

    // Save updated record
    core.DB.Set("collaboration", workspaceID, record, "edge")

    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": "collaboration",
        "key":        workspaceID,
        "value":      record,
        "source":     c.Name,
    })

    core.Log(fmt.Sprintf("[%s] Added member %s to workspace %s", c.Name, memberID, workspaceID))
    return record
}

// Handle DB update events
func (c *CollaborationAgent) HandleDBUpdate(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB update received: %s:%s", c.Name, collection, key))
}

// Handle DB delete events
func (c *CollaborationAgent) HandleDBDelete(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB delete received: %s:%s", c.Name, collection, key))
}

// Recover from errors
func (c *CollaborationAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", c.Name, err))
}

func init() {
    core.RegisterAgent("CollaborationAgent", NewCollaborationAgent())
}
