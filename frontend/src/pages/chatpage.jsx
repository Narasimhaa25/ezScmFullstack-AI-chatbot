import React, { useState, useEffect, useRef } from "react";

const providers = {
  openai: ["gpt-3.5-turbo", "gpt-4"],
  claude: ["Claude-3-Haiku", "Claude-3-Sonnet"],
  gemini: ["Gemini Flash", "Gemini Pro"],
};

function ChatPage() {
  const [profile, setProfile] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [provider, setProvider] = useState("gemini");
  const [model, setModel] = useState("Gemini Flash");
  const [files, setFiles] = useState([]);

  const messageEndRef = useRef(null);

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Fetch sessions
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/sessions")
      .then((res) => res.json())
      .then((data) => setSessions(Array.isArray(data) ? data : []))
      .catch((err) => console.error("Failed to fetch sessions:", err));
  }, []);

  // Fetch messages for selected session
  useEffect(() => {
    if (!selectedSession) return;

    fetch(`http://127.0.0.1:8000/api/sessions/${selectedSession.id}/messages`)
      .then((res) => (res.status === 404 ? [] : res.json()))
      .then((data) => setMessages(Array.isArray(data) ? data : []))
      .catch((err) => console.error("Failed to fetch messages:", err));
  }, [selectedSession]);

  // Create new session
  const createSession = () => {
    fetch("http://127.0.0.1:8000/api/sessions", { method: "POST" })
      .then((res) => res.json())
      .then((newSession) => {
        setSessions([newSession, ...sessions]);
        setSelectedSession(newSession);
        setMessages([]);
      })
      .catch((err) => console.error("Failed to create session:", err));
  };

  // Delete session permanently
  const deleteSession = (sessionId, title) => {
    if (window.confirm(`Are you sure you want to delete session "${title}"?`)) {
      fetch(`http://127.0.0.1:8000/api/sessions/${sessionId}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
      })
        .then((res) => {
          if (!res.ok) throw new Error("Failed to delete session from server");
          setSessions((prev) => prev.filter((s) => s.id !== sessionId));
          if (selectedSession?.id === sessionId) setSelectedSession(null);
        })
        .catch((err) => console.error(err));
    }
  };

  // Send message (SSE)
  const sendMessage = () => {
    if (!input.trim() || !selectedSession) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: input, timestamp: new Date().toISOString(), files },
    ]);
    setLoading(true);
    setFiles([]);

    let assistantMessage = "";

    const evtSource = new EventSource(
      `http://127.0.0.1:8000/api/chat/stream?session_id=${selectedSession.id}&provider=${provider}&model=${model}&prompt=${encodeURIComponent(
        input
      )}`
    );

    evtSource.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data.delta === "[DONE]") {
          evtSource.close();
          setLoading(false);
          return;
        }
        assistantMessage += data.delta;
        setMessages((prev) => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg?.role === "assistant") {
            return [
              ...prev.slice(0, -1),
              { role: "assistant", content: assistantMessage, timestamp: new Date().toISOString() },
            ];
          } else {
            return [...prev, { role: "assistant", content: assistantMessage, timestamp: new Date().toISOString() }];
          }
        });
      } catch (err) {
        console.error("Failed to parse SSE:", e.data, err);
      }
    };

    evtSource.onerror = () => {
      evtSource.close();
      setLoading(false);
    };

    setInput("");
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial, sans-serif" }}>
      {/* Sidebar */}
      <div style={{ width: "300px", borderRight: "1px solid #ccc", padding: "15px", display: "flex", flexDirection: "column", backgroundColor: "#1e2f50", color: "#fff" }}>
        <div style={{ marginBottom: "20px" }}>
          <h3>Hello, {profile?.username || "User"}</h3>
        </div>

        <button
          onClick={createSession}
          style={{ marginBottom: "10px", padding: "8px", borderRadius: "5px", border: "none", cursor: "pointer", backgroundColor: "#4caf50", color: "#fff" }}
        >
          + New Session
        </button>

        <input
          type="text"
          placeholder="Search sessions..."
          style={{ marginBottom: "10px", padding: "8px", borderRadius: "5px", border: "none" }}
        />

        <div style={{ overflowY: "auto", flex: 1 }}>
          {sessions.map((session) => (
            <div
              key={session.id}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "10px",
                cursor: "pointer",
                borderRadius: "5px",
                marginBottom: "5px",
                backgroundColor: selectedSession?.id === session.id ? "#0d1b33" : "#1e2f50",
              }}
            >
              <div onClick={() => setSelectedSession(session)}>
                <b>{session.title || "Untitled"}</b>
                <br />
                <small style={{ color: "#aaa" }}>{session.updated_at ? new Date(session.updated_at).toLocaleString() : ""}</small>
              </div>
              <div
                style={{ cursor: "pointer" }}
                onClick={() => deleteSession(session.id, session.title || "Untitled")}
                title="Delete Session"
              >
                🗑️
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", padding: "15px" }}>
        <div style={{ flex: 1, overflowY: "auto", marginBottom: "10px", paddingRight: "5px" }}>
          {messages.map((msg, idx) => (
            <div key={idx} style={{ display: "flex", justifyContent: msg.role === "user" ? "flex-end" : "flex-start", marginBottom: "10px" }}>
              <div style={{ maxWidth: "70%", padding: "10px", borderRadius: "12px", backgroundColor: msg.role === "user" ? "#4caf50" : "#e0e0e0", color: msg.role === "user" ? "#fff" : "#000", wordBreak: "break-word" }}>
                {msg.content}
              </div>
            </div>
          ))}
          {loading && <div><i>Assistant is typing...</i></div>}
          <div ref={messageEndRef} />
        </div>

        {/* Bottom Bar */}
        <div style={{ display: "flex", gap: "10px", alignItems: "center", paddingTop: "10px" }}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            rows={2}
            style={{ flex: 3, padding: "10px", borderRadius: "8px", border: "1px solid #ccc", resize: "none" }}
            disabled={loading}
            placeholder="Type your message..."
          />

          {/* Provider & Model */}
          <div style={{ display: "flex", flexDirection: "column", gap: "5px" }}>
            <select value={provider} onChange={(e) => { setProvider(e.target.value); setModel(providers[e.target.value][0]); }} style={{ borderRadius: "5px", padding: "5px" }}>
              {Object.keys(providers).map((p) => <option key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</option>)}
            </select>
            <select value={model} onChange={(e) => setModel(e.target.value)} style={{ borderRadius: "5px", padding: "5px" }}>
              {providers[provider].map((m) => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>

          {/* File Attachment */}
          <input type="file" multiple onChange={(e) => setFiles(Array.from(e.target.files))} style={{ borderRadius: "5px", padding: "5px" }} />

          {/* Send & Stop */}
          <button onClick={sendMessage} disabled={loading || !input.trim()} style={{ padding: "10px 15px", borderRadius: "8px", backgroundColor: "#4caf50", color: "#fff", border: "none" }}>Send</button>
          <button onClick={() => setLoading(false)} disabled={!loading} style={{ padding: "10px 15px", borderRadius: "8px", backgroundColor: "#f44336", color: "#fff", border: "none" }}>Stop</button>

          {/* Character Count */}
          <div style={{ fontSize: "0.8em", color: "#555" }}>{input.length} chars</div>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;