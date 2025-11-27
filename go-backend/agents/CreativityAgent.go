// go-backend/agents/CreativityAgent.go
package agents

import (
    "core"
    "fmt"
)

// CreativityAgent generates ideas, variations, enhancements, and alternative outputs
type CreativityAgent struct {
    Name string
}

func NewCreativityAgent() *CreativityAgent {
    agent := &CreativityAgent{Name: "CreativityAgent"}

    // Subscribe to events (optional, matches Python-style)
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// GenerateIdeas produces multiple creative variations from a base concept
func (c *CreativityAgent) GenerateIdeas(concept string) []string {
    ideas := []string{
        fmt.Sprintf("%s — futuristic version", concept),
        fmt.Sprintf("%s — simplified minimal design", concept),
        fmt.Sprintf("%s — expanded enterprise model", concept),
        fmt.Sprintf("%s — rewritten for speed/performance", concept),
    }

    core.Log(fmt.Sprintf("[%s] Ideas generated for: %s", c.Name, concept))
    return ideas
}

// EnhanceContent improves or expands a piece of text/content
func (c *CreativityAgent) EnhanceContent(content string) string {
    enhanced := fmt.Sprintf("%s\n\nEnhanced: Added clarity, structure, and expressive style.", content)

    core.Log(fmt.Sprintf("[%s] Content enhanced", c.Name))
    return enhanced
}

// Remix generates alternative variations from a given input
func (c *CreativityAgent) Remix(input string) []string {
    remixes := []string{
        fmt.Sprintf("Creative remix 1 → %s (story edition)", input),
        fmt.Sprintf("Creative remix 2 → %s (technical edition)", input),
        fmt.Sprintf("Creative remix 3 → %s (marketing edition)", input),
    }

    core.Log(fmt.Sprintf("[%s] Remixes generated", c.Name))
    return remixes
}

// Event: DB updated
func (c *CreativityAgent) HandleDBUpdate(event map[string]interface{}) {
    core.Log(fmt.Sprintf("[%s] DB update received from %s",
        c.Name,
        event["source"].(string),
    ))
}

// Event: DB deleted
func (c *CreativityAgent) HandleDBDelete(event map[string]interface{}) {
    core.Log(fmt.Sprintf("[%s] DB delete received", c.Name))
}

// Error recovery
func (c *CreativityAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", c.Name, err))
}

func init() {
    core.RegisterAgent("CreativityAgent", NewCreativityAgent())
}
