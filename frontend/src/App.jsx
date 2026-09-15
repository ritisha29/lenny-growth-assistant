import { useEffect, useState } from "react";
import {
  createSession,
  sendMessage,
  generateShip30,
} from "./services/api";
import "./App.css";

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [artifact, setArtifact] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    startNewSession();
  }, []);

  async function startNewSession() {
    try {
      setError("");

      const session = await createSession("New conversation");

      setSessionId(session.id);
      setMessages([]);
      setArtifact(null);
    } catch (err) {
      setError("Unable to create a conversation.");
    }
  }

  async function handleSend(event) {
    event.preventDefault();

    if (!input.trim() || !sessionId || loading) {
      return;
    }

    const userMessage = input.trim();

    setInput("");
    setError("");

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setLoading(true);

    try {
      const response = await sendMessage(
        sessionId,
        userMessage,
      );

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: response.answer,
          sources: response.sources,
        },
      ]);
    } catch (err) {
      setError(
        "Unable to generate an answer. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleShip30() {
    if (!sessionId || loading) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await generateShip30(
        sessionId,
        "What to do when product growth stops",
        "https://www.youtube.com/watch?v=8xLquwfx6p0",
      );

      setArtifact({
        id: response.artifact_id,
        content: response.essay,
      });
    } catch (err) {
      setError(
        "Unable to generate the Ship 30 essay.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <h1>Lenny Growth Assistant</h1>
          <p>
            Product and growth advice grounded in Lenny's
            Podcast transcripts.
          </p>
        </div>

        <div className="model-badge">
          Model: Ollama
        </div>
      </header>

      <main className="workspace">
        <aside className="sidebar">
          <button
            className="new-chat-button"
            onClick={startNewSession}
          >
            + New conversation
          </button>

          <div className="sidebar-section">
            <h3>Current session</h3>

            {sessionId ? (
              <div className="session-card">
                <span>Active conversation</span>
                <small>{sessionId}</small>
              </div>
            ) : (
              <p>Creating session...</p>
            )}
          </div>

          <div className="sidebar-section">
            <h3>Tools</h3>

            <button
              className="tool-button"
              onClick={handleShip30}
              disabled={!sessionId || loading}
            >
              Create Ship 30 essay
            </button>
          </div>
        </aside>

        <section className="chat-panel">
          <div className="chat-header">
            <div>
              <h2>Ask Lenny</h2>
              <span>
                Answers are grounded in transcript evidence.
              </span>
            </div>
          </div>

          <div className="messages">
            {messages.length === 0 && (
              <div className="empty-state">
                <h2>What are you working on?</h2>
                <p>
                  Ask a product or growth question and get an
                  answer grounded in Lenny's transcripts.
                </p>

                <div className="suggestions">
                  <button
                    onClick={() =>
                      setInput(
                        "What are the five questions Jason Cohen recommends asking when a product stops growing?"
                      )
                    }
                  >
                    Jason Cohen's growth framework
                  </button>

                  <button
                    onClick={() =>
                      setInput(
                        "How should a product team think about retention?"
                      )
                    }
                  >
                    Product retention
                  </button>
                </div>
              </div>
            )}

            {messages.map((message, index) => (
              <div
                className={`message ${message.role}`}
                key={index}
              >
                <div className="message-role">
                  {message.role === "user"
                    ? "You"
                    : "Lenny Assistant"}
                </div>

                <div className="message-content">
                  {message.content}
                </div>

                {message.sources &&
                  message.sources.length > 0 && (
                    <div className="sources">
                      <strong>Sources</strong>

                      {message.sources.map(
                        (source, sourceIndex) => (
                          <a
                            href={source.source_url}
                            target="_blank"
                            rel="noreferrer"
                            key={sourceIndex}
                          >
                            {source.episode_title}
                          </a>
                        ),
                      )}
                    </div>
                  )}
              </div>
            ))}

            {loading && (
              <div className="message assistant">
                <div className="message-role">
                  Lenny Assistant
                </div>

                <div className="message-content">
                  Thinking...
                </div>
              </div>
            )}
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <form
            className="composer"
            onSubmit={handleSend}
          >
            <input
              value={input}
              onChange={(event) =>
                setInput(event.target.value)
              }
              placeholder="Ask a product or growth question..."
              disabled={loading}
            />

            <button
              type="submit"
              disabled={
                loading ||
                !input.trim() ||
                !sessionId
              }
            >
              Send
            </button>
          </form>
        </section>

        <aside className="artifact-panel">
          <div className="artifact-header">
            <div>
              <h2>Artifact Viewer</h2>
              <span>
                Generated content appears here.
              </span>
            </div>
          </div>

          <div className="artifact-content">
            {artifact ? (
              <>
                <div className="artifact-meta">
                  <span>Markdown artifact</span>
                  <small>{artifact.id}</small>
                </div>

                <pre>
                  {artifact.content}
                </pre>
              </>
            ) : (
              <div className="artifact-empty">
                <h3>No artifact yet</h3>
                <p>
                  Use "Create Ship 30 essay" to generate a
                  transcript-grounded article.
                </p>
              </div>
            )}
          </div>
        </aside>
      </main>
    </div>
  );
}

export default App;