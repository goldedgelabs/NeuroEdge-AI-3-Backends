// go-backend/agents/BackupAgent.go
package agents

import (
    "core"
    "fmt"
    "time"
)

type BackupAgent struct {
    Name string
}

func NewBackupAgent() *BackupAgent {
    agent := &BackupAgent{Name: "BackupAgent"}

    // Subscribe to DB events
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// Create a backup of a given collection or record
func (b *BackupAgent) CreateBackup(collection string, key string, data map[string]interface{}) map[string]interface{} {
    backupID := fmt.Sprintf("backup_%d", time.Now().UnixMilli())
    backupRecord := map[string]interface{}{
        "id":         backupID,
        "collection": collection,
        "key":        key,
        "data":       data,
        "createdAt":  time.Now().String(),
    }

    // Save backup to edge DB
    core.DB.Set("backups", backupID, backupRecord, "edge")

    // Emit DB update event
    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": "backups",
        "key":        backupID,
        "value":      backupRecord,
        "source":     b.Name,
    })

    core.Log(fmt.Sprintf("[%s] Backup created → %s", b.Name, backupID))
    return backupRecord
}

// Retrieve all backups for a collection
func (b *BackupAgent) GetBackups(collection string) []map[string]interface{} {
    records := core.DB.GetAll("backups") // Assume DB.GetAll returns []map[string]interface{}
    var filtered []map[string]interface{}
    for _, rec := range records {
        if rec["collection"] == collection {
            filtered = append(filtered, rec)
        }
    }
    return filtered
}

// Handle DB update events
func (b *BackupAgent) HandleDBUpdate(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB update received: %s:%s", b.Name, collection, key))
}

// Handle DB delete events
func (b *BackupAgent) HandleDBDelete(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB delete received: %s:%s", b.Name, collection, key))
}

// Recover from errors
func (b *BackupAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", b.Name, err))
}

func init() {
    core.RegisterAgent("BackupAgent", NewBackupAgent())
}
