"use client"

import { useState, useRef, useEffect } from "react"
import "./App.css"

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "assistant",
      content:
        "Hello! I'm your USPTO Patent Assistant. I can help you with questions about the patent process, filing requirements, deadlines, and more. How can I assist you today?",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const typeMessage = (message, messageId) => {
    setIsTyping(true)
    let index = 0
    const typingSpeed = 15 // milliseconds per character

    const typeInterval = setInterval(() => {
      if (index < message.length) {
        setMessages((prev) =>
          prev.map((msg) => (msg.id === messageId ? { ...msg, content: message.substring(0, index + 1) } : msg)),
        )
        index++
      } else {
        clearInterval(typeInterval)
        setIsTyping(false)
      }
    }, typingSpeed)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      type: "user",
      content: input.trim(),
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      // Replace with your actual backend endpoint
    const response = await fetch(`http://127.0.0.1:8000/question/${encodeURIComponent(input.trim())}`)

      if (!response.ok) {
        throw new Error("Failed to get response from server")
      }

      const data = await response.json() // Change from response.text() to response.json()
      const responseText = Array.isArray(data) ? data[0] : data // Extract the first element if it's an array

      const assistantMessage = {
        id: Date.now() + 1,
        type: "assistant",
        content: "",
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])
      typeMessage(responseText, assistantMessage.id)
    } catch (error) {
      console.error("Error:", error)
      const errorMessage = {
        id: Date.now() + 1,
        type: "assistant",
        content:
          "I apologize, but I encountered an error while processing your request. Please try again or contact support if the issue persists.",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo">⚖️</div>
            <div className="title-section">
              <h1>USPTO Patent Assistant</h1>
              <p>Professional Patent Process Guidance</p>
            </div>
          </div>
          <div className="status-indicator">
            <div className="status-dot"></div>
            <span>Online</span>
          </div>
        </div>
      </header>

      <main className="chat-container">
        <div className="messages-container">
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              <div className="message-avatar">{message.type === "user" ? "👤" : "🤖"}</div>
              <div className="message-content">
                <div className="message-text">{message.content}</div>
                <div className="message-timestamp">
                  {message.timestamp.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </div>
              </div>
            </div>
          ))}

          {isLoading && !isTyping && (
            <div className="message assistant">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <div className="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <span className="typing-text">...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <form className="input-form" onSubmit={handleSubmit}>
          <div className="input-container">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about patents, filing procedures, deadlines, or any USPTO-related questions..."
              className="message-input"
              rows="1"
              disabled={isLoading}
            />
            <button type="submit" className="send-button" disabled={!input.trim() || isLoading}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22,2 15,22 11,13 2,9 22,2"></polygon>
              </svg>
            </button>
          </div>
        </form>
      </main>

      <footer className="app-footer">
        <p>
          <strong>Disclaimer:</strong> This assistant provides general information about USPTO procedures. For specific
          legal advice, please consult with a qualified patent attorney.
        </p>
      </footer>
    </div>
  )
}

export default App
