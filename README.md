
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
**uvicorn app.main:app --reload**
5.Frontend
	1.Navigate to the frontend folder:
 	2.	Install dependencies:
  			npm install
	3.Start the React development server:
 		npm run dev
   	4.	Open your browser at:
	http://localhost:3000
 <img width="1680" height="1050" alt="Screenshot 2025-09-05 at 02 31 19" src="https://github.com/user-attachments/assets/3a87e682-8a0e-4574-a1f4-a48ed43e9780" />
<img width="1680" height="1050" alt="Screenshot 2025-09-05 at 02 30 53" src="https://github.com/user-attachments/assets/eb6371a6-e2f3-4ecc-9520-7c8465b76bdf" />

DATABASE

<img width="1680" height="1050" alt="Screenshot 2025-09-05 at 03 24 59" src="https://github.com/user-attachments/assets/077726cb-51db-4584-8f99-ade54965c81f" />


   <img width="1680" height="1050" alt="Screenshot 2025-09-05 at 03 27 45" src="https://github.com/user-attachments/assets/4c60702e-b12f-46e3-a7b5-5e59e6e18667" />

<img width="1680" height="1050" alt="Screenshot 2025-09-05 at 03 28 12" src="https://github.com/user-attachments/assets/d92da32c-3daf-48f1-bbdb-fdb741881bc4" />
<img width="1680" height="1050" alt="Screenshot 2025-09-05 at 03 28 32" src="https://github.com/user-attachments/assets/e3d23972-3748-48ab-a31c-575620ec7877" />
