# AWS Support Agent - Full-Stack Application

A production-ready, full-stack AWS Support Agent featuring FastAPI backend with LangChain & GROQ, and Vue 3 frontend with Tailwind CSS, authentication, real-time streaming, and chat history persistence.

## 🌟 Features

### Backend (FastAPI + LangChain)
- 🤖 **Intelligent Agent** - Powered by GROQ LLM (Llama-3.1-8b-instant)
- 📚 **Vector Search** - FAISS-based knowledge retrieval
- 🔐 **API Key Authentication** - Secure endpoints with Bearer tokens
- ⚡ **WebSocket Streaming** - Real-time response streaming
- 📖 **Auto-generated Docs** - Swagger UI and ReDoc
- 🔒 **Protected Endpoints** - All agent operations require auth

### Frontend (Vue 3 + Tailwind CSS)
- 🎨 **Modern UI** - Beautiful design with gradients and animations
- 🔐 **Login System** - API key authentication with session management
- 💾 **Chat History** - Automatic localStorage persistence
- ⚡ **Real-time Streaming** - Toggle WebSocket streaming on/off
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🌙 **Clean Architecture** - Well-organized components

## 🚀 Quick Start

### Automated Setup (Recommended)

```powershell
# Run the setup script
.\setup.ps1

# Start both servers
.\start.ps1
```

Then open http://localhost:3000 and login with `demo-key-123`

### Manual Setup

**1. Install Backend Dependencies (using virtual environment)**
```powershell
# Install/update dependencies in the virtual environment
.\aws-env\Scripts\python.exe -m pip install -r requirements.txt
```

**2. Install Frontend Dependencies**
```powershell
cd frontend
npm install
cd ..
```

**3. Start Backend** (using virtual environment Python)
```powershell
.\aws-env\Scripts\python.exe api_run.py
```

**4. Start Frontend** (in another terminal)
```powershell
cd frontend
npm run dev
```

**5. Open Browser**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔐 Authentication

Login with one of these demo API keys:
- `demo-key-123` - Demo user
- `admin-key-456` - Admin user
- Any key with 5+ characters - Generic user

## 💡 Usage

1. **Login** - Enter your API key
2. **Initialize** - Click "Initialize Agent" to load knowledge base
3. **Query** - Ask questions about AWS services
4. **Stream** - Toggle "Stream response" for real-time output
5. **Sources** - Check "Include sources" to see documentation references

## 📁 Project Structure

```
AWS-Support-Agent/
├── frontend/              # Vue 3 frontend
│   ├── src/
│   │   ├── components/   # Vue components
│   │   ├── api.js        # API client
│   │   └── ...
│   └── package.json
├── api/                   # FastAPI backend
│   ├── routers/          # API endpoints
│   ├── main.py           # FastAPI app
│   ├── auth.py           # Authentication
│   └── ...
├── steps/                 # Pipeline steps
├── configs/               # Configuration files
├── api_run.py            # Backend entry point
├── setup.ps1             # Automated setup
└── start.ps1             # Start both servers
```

## 📚 Documentation

- **FULLSTACK_GUIDE.md** - Complete guide with all features
- **API_README.md** - Backend API documentation
- **frontend/README.md** - Frontend documentation
- **FASTAPI_INTEGRATION.md** - API integration guide

## 🛠️ Technologies

**Backend:**
- FastAPI - Modern web framework
- LangChain - LLM orchestration
- GROQ - Fast LLM inference
- FAISS - Vector similarity search
- Socket.IO - WebSocket support
- Pydantic - Data validation

**Frontend:**
- Vue 3 - Progressive framework
- Vite - Fast build tool
- Tailwind CSS - Utility-first CSS
- Axios - HTTP client
- Socket.IO Client - WebSocket client

## 🔧 Configuration

### Backend (.env)
```env
GROQ_API_KEY=your_key_here
LLM_TYPE=groq
GROQ_MODEL_NAME=llama-3.1-8b-instant
TEMPERATURE=0.2
MAX_TOKENS=1200
```

### Frontend (frontend/.env)
```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🧪 Testing

**Backend:**
```powershell
python test_api.py
```

**Frontend:**
Open browser DevTools and check:
- Console for errors
- Network tab for API calls
- Application tab for localStorage

## 🚀 Deployment

### Frontend (Vercel/Netlify)
```powershell
cd frontend
npm run build
# Deploy 'dist/' folder
```

### Backend (Docker)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🐛 Troubleshooting

### Backend Connection Issues
- Ensure backend is running on port 8000
- Check CORS settings in `api/config.py`
- Verify firewall/antivirus settings

### Authentication Failures
- Use minimum 5 characters for API key
- Clear localStorage and re-login
- Check browser console for errors

### WebSocket Issues
- Verify `python-socketio` is installed
- Check `/ws` endpoint is accessible
- Try disabling streaming temporarily

## 📝 API Endpoints

### Authentication
- `POST /auth/login` - Login with API key
- `GET /auth/validate` - Validate session

### Agent (Protected)
- `POST /agent/initialize` - Initialize agent
- `GET /agent/status` - Get status
- `GET /agent/config` - Get configuration
- `POST /agent/query` - Query agent

### WebSocket
- Connect to `/ws` for streaming
- Events: `query`, `chunk`, `complete`, `error`

## 🎯 Next Steps

- [ ] Add JWT tokens for enhanced security
- [ ] Implement rate limiting
- [ ] Add user profile management
- [ ] Export chat to PDF/Markdown
- [ ] Add voice input/output
- [ ] Implement dark mode
- [ ] Multi-language support

## 📄 License

Apache 2.0

---

**Built with ❤️ using FastAPI, LangChain, Vue 3, and Tailwind CSS**
