# ezScmFullstack-AI-chatbot
# Multi-Provider Streaming AI Chat Application

## Project Description
This project is a full-stack AI chat application that supports multiple AI providers such as OpenAI, Anthropic Claude, and Google Gemini. It allows real-time streaming of AI responses, multi-session management, file attachments, and seamless switching between AI providers and models. Users can interact with AI in a chat interface while maintaining session histories.

Key Features:
- Multi-provider AI support (OpenAI, Claude, Gemini)
- Real-time token-by-token streaming responses
- Persistent session and message storage
- File attachments for messages
- Responsive and interactive chat interface
- Session management with deletion and search

---

## Technology Stack

### Backend
- **FastAPI** – Python web framework for REST and SSE APIs  
- **SQLAlchemy** – ORM for database management  
- **PostgreSQL/SQLite** – Relational database (choose as per `.env`)  
- **sse-starlette** – Server-Sent Events support for streaming AI responses  

### Frontend
- **React.js** – SPA for chat interface  
- **JavaScript (ES6)** – Frontend logic and state management  
- **CSS/Inline Styles** – Styling and responsive layouts  

---

## Installation & Setup

### Backend
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/multi-provider-ai-chat.git
   cd multi-provider-ai-chat/backend
2.Install dependencies:
pip install -r requirements.txt
3.Configure environment variables:
	•	Copy .env.example to .env:
•	Update the variables:
 DATABASE_URL=sqlite:///./chat.db  # or PostgreSQL URL
OPENAI_API_KEY=your_openai_key
CLAUDE_API_KEY=your_claude_key
GEMINI_API_KEY=your_gemini_key
4.Run the backend server:
uvicorn app.main:app --reload

   
