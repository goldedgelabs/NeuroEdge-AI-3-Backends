// core/agentManager.go
package core

type Agent interface {
    Handle(task map[string]interface{}) map[string]interface{}
}

var AgentManager = map[string]Agent{}

func RegisterAgent(name string, agent Agent) {
    AgentManager[name] = agent
}

func RunAgent(name string, task map[string]interface{}) map[string]interface{} {
    if ag, ok := AgentManager[name]; ok {
        return ag.Handle(task)
    }
    return map[string]interface{}{"error": "agent not found"}
}
