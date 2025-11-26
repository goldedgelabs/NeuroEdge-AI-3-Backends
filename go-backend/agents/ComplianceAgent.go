// go-backend/agents/ComplianceAgent.go
package agents

import (
    "core"
    "fmt"
    "time"
)

type ComplianceAgent struct {
    Name string
}

func NewComplianceAgent() *ComplianceAgent {
    agent := &ComplianceAgent{Name: "ComplianceAgent"}

    // Subscribe to DB events
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// Verify compliance for a record
func (c *ComplianceAgent) VerifyRecord(collection string, key string, rules map[string]interface{}) map[string]interface{} {
    record := core.DB.Get(collection, key, "edge")
    if record == nil {
        core.Log(fmt.Sprintf("[%s] Record not found: %s:%s", c.Name, collection, key))
        return nil
    }

    complianceResult := map[string]interface{}{
        "recordID": key,
        "collection": collection,
        "status": "compliant",
        "violations": []string{},
        "checkedAt": time.Now().String(),
    }

    // Example rule checking
    for field, rule := range rules {
        if val, ok := record[field]; ok {
            if val != rule {
                complianceResult["status"] = "non-compliant"
                complianceResult["violations"] = append(complianceResult["violations"].([]string), field)
            }
        }
    }

    // Save compliance result
    complianceID := fmt.Sprintf("compliance_%s_%d", key, time.Now().UnixMilli())
    core.DB.Set("compliance_results", complianceID, complianceResult, "edge")

    // Publish DB update event
    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": "compliance_results",
        "key": complianceID,
        "value": complianceResult,
        "source": c.Name,
    })

    core.Log(fmt.Sprintf("[%s] Compliance check done → %s:%s Status: %s", c.Name, collection, key, complianceResult["status"]))
    return complianceResult
}

// Handle DB update events
func (c *ComplianceAgent) HandleDBUpdate(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB update received: %s:%s", c.Name, collection, key))
}

// Handle DB delete events
func (c *ComplianceAgent) HandleDBDelete(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB delete received: %s:%s", c.Name, collection, key))
}

// Recover from errors
func (c *ComplianceAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", c.Name, err))
}

func init() {
    core.RegisterAgent("ComplianceAgent", NewComplianceAgent())
}
