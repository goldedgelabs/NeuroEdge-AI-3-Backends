// core/eventBus.go
package core

import "sync"

type EventHandler func(data map[string]interface{})

type EventBus struct {
    subscribers map[string][]EventHandler
    mu          sync.RWMutex
}

var Bus = &EventBus{
    subscribers: make(map[string][]EventHandler),
}

func (eb *EventBus) Subscribe(event string, handler EventHandler) {
    eb.mu.Lock()
    defer eb.mu.Unlock()
    eb.subscribers[event] = append(eb.subscribers[event], handler)
}

func (eb *EventBus) Publish(event string, data map[string]interface{}) {
    eb.mu.RLock()
    defer eb.mu.RUnlock()
    if handlers, ok := eb.subscribers[event]; ok {
        for _, h := range handlers {
            go h(data)
        }
    }
}
