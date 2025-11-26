// go-backend/agents/BillingAgent.go
package agents

import (
    "core"
    "fmt"
    "time"
)

type BillingAgent struct {
    Name string
}

func NewBillingAgent() *BillingAgent {
    agent := &BillingAgent{Name: "BillingAgent"}

    // Subscribe to DB events
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// Generate a billing record
func (b *BillingAgent) GenerateInvoice(userID string, amount float64, details map[string]interface{}) map[string]interface{} {
    invoiceID := fmt.Sprintf("invoice_%d", time.Now().UnixMilli())
    invoice := map[string]interface{}{
        "id":        invoiceID,
        "userID":    userID,
        "amount":    amount,
        "details":   details,
        "createdAt": time.Now().String(),
    }

    // Save invoice to edge DB
    core.DB.Set("billing", invoiceID, invoice, "edge")

    // Emit DB update event
    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": "billing",
        "key":        invoiceID,
        "value":      invoice,
        "source":     b.Name,
    })

    core.Log(fmt.Sprintf("[%s] Invoice generated → %s for user %s", b.Name, invoiceID, userID))
    return invoice
}

// Fetch all invoices for a user
func (b *BillingAgent) GetInvoices(userID string) []map[string]interface{} {
    records := core.DB.GetAll("billing")
    var filtered []map[string]interface{}
    for _, rec := range records {
        if rec["userID"] == userID {
            filtered = append(filtered, rec)
        }
    }
    return filtered
}

// Handle DB update events
func (b *BillingAgent) HandleDBUpdate(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB update received: %s:%s", b.Name, collection, key))
}

// Handle DB delete events
func (b *BillingAgent) HandleDBDelete(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB delete received: %s:%s", b.Name, collection, key))
}

// Recover from errors
func (b *BillingAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", b.Name, err))
}

func init() {
    core.RegisterAgent("BillingAgent", NewBillingAgent())
}
