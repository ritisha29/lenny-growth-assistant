# Design

## Product Design

The product is intentionally designed around a simple three-column workflow:

**Context → Conversation → Output**

### Left: Conversation

The left sidebar provides:

- New conversation
- Current session
- Ship 30 tool

This gives the user persistent context without overwhelming the main interaction.

### Center: Ask Lenny

The chat is the primary interaction surface.

The user can:

- ask a question;
- read the grounded answer;
- inspect sources;
- continue with a follow-up.

Suggested prompts help new users understand what the system can do.

### Right: Artifact Viewer

Generated content appears beside the conversation rather than replacing it.

This follows the mental model of an AI workspace where generated work becomes a separate reusable object.

## Interaction Principles

### 1. Conversation first

The assistant should feel like a conversational research tool rather than a traditional search interface.

### 2. Evidence should be visible

Answers expose source information so users can verify where an insight came from.

### 3. Generated work is separate

Long-form generated content belongs in the Artifact Viewer rather than inside the chat bubble.

### 4. Fail clearly

When the system cannot support an answer from the knowledge base, it should say so instead of inventing an answer.

## Ship 30 Flow

1. User selects "Create Ship 30 essay".
2. User provides a topic.
3. The Ship 30 skill retrieves relevant transcript evidence.
4. The agent generates a grounded Markdown essay.
5. The artifact is persisted in PostgreSQL.
6. The Artifact Viewer displays the result.

## Visual Direction

The UI uses:

- neutral backgrounds;
- restrained borders;
- compact controls;
- clear typography;
- responsive layout;
- distinct visual hierarchy between chat and artifacts.

The goal is to make the interface feel like a focused professional productivity tool rather than a generic chatbot.