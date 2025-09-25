# SocialMediaSentimentTracker v2.0

> **Redesigned with modern architecture**: A sentiment analysis microservice with React frontend

A complete redesign of the sentiment analysis tool using modern technologies and microservice architecture. The new version provides a FastAPI backend for sentiment analysis and a React frontend with Tailwind CSS.

## 🏗️ Architecture

```
┌─────────────────┐    HTTP API    ┌─────────────────┐
│  React Frontend │ ──────────────▶ │ FastAPI Backend │
│   (Port 5173)   │                │   (Port 8000)   │
└─────────────────┘                └─────────────────┘
        │                                   │
        ├─ Tailwind CSS                     ├─ Transformers
        ├─ Axios for API calls              ├─ Pydantic models
        ├─ Recharts for visualization       ├─ CORS middleware
        └─ Local history storage            └─ Health checks
```

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/aangell98/SocialMediaSentimentTracker.git
cd SocialMediaSentimentTracker

# Start the services
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## 🎯 Features

### Backend (FastAPI Microservice)
- **Modern API**: RESTful API with automatic OpenAPI documentation
- **Advanced NLP**: Uses state-of-the-art Hugging Face transformers
- **Multilingual Support**: Supports text in multiple languages
- **Health Checks**: Built-in health monitoring endpoints
- **CORS Support**: Configured for frontend integration
- **Docker Ready**: Containerized for easy deployment
- **Error Handling**: Comprehensive error handling and logging

### Frontend (React + Tailwind)
- **Modern UI**: Clean, responsive interface with Tailwind CSS
- **Real-time Analysis**: Instant sentiment analysis with confidence scores
- **Visual Feedback**: Color-coded sentiment indicators and progress bars
- **Analysis History**: Local storage of recent analyses
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: User-friendly error messages

## 📊 API Endpoints

### `POST /analyze`
Analyze sentiment of provided text.

**Request:**
```json
{
  "text": "I love this new approach to the project!"
}
```

**Response:**
```json
{
  "label": "positive",
  "score": 0.9845
}
```

### `GET /health`
Health check endpoint for monitoring.

### `POST /batch-analyze`
Analyze multiple texts at once (up to 10 per request).

## 🧪 Testing

### Backend Tests
```bash
cd backend
python test_backend.py
```

### Frontend Tests
```bash
cd frontend
npm run build  # Test the build process
npm run lint   # Check code quality
```

## 🚢 Deployment

### Backend Deployment
The backend can be deployed to any cloud provider that supports Docker:

- **Railway**: Connect your GitHub repo and deploy automatically
- **Render**: Use the provided Dockerfile
- **AWS**: Use ECS or Lambda with container support
- **Google Cloud**: Use Cloud Run

### Frontend Deployment
The frontend can be deployed to static hosting services:

- **Vercel**: Connect GitHub repo for automatic deployments
- **Netlify**: Deploy the `dist` folder after building
- **GitHub Pages**: Use GitHub Actions for deployment

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
# Optional: Configure the model to use
MODEL_NAME=nlptown/bert-base-multilingual-uncased-sentiment

# Optional: Configure logging
LOG_LEVEL=INFO
```

#### Frontend (.env)
```bash
# Backend API URL
VITE_API_URL=http://localhost:8000
```

## 🎨 Customization

### Adding New Models
To use a different sentiment analysis model, update `backend/app/analysis.py`:

```python
pipe = pipeline(
    "sentiment-analysis", 
    model="your-preferred-model",
    return_all_scores=False
)
```

### Styling the Frontend
The frontend uses Tailwind CSS. Customize colors in `frontend/tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      positive: '#10B981',  // Customize positive color
      negative: '#EF4444',  // Customize negative color
      neutral: '#6B7280',   // Customize neutral color
    }
  },
}
```

## 📈 Monitoring

### Health Checks
- Backend health: `GET /health`
- Frontend build: Check for successful compilation

### Logging
The backend provides structured logging for:
- API requests and responses
- Model loading and predictions
- Error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆚 Migration from v1.0

The new version maintains the core sentiment analysis functionality while providing:

✅ **Modern Architecture**: Microservice design vs monolithic structure  
✅ **Better UI/UX**: React + Tailwind vs Streamlit  
✅ **API-First**: RESTful API for integration  
✅ **Cloud Ready**: Docker + CI/CD pipeline  
✅ **Scalable**: Separate frontend and backend  

### Legacy Components (v1.0)
The original Reddit scraping functionality is preserved in the `src/` directory for reference, but the new version focuses on the sentiment analysis service itself.

---

**Built with ❤️ using FastAPI, React, and modern web technologies.**
