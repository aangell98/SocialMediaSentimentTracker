# Deployment Guide

This guide covers different deployment options for the SocialMediaSentimentTracker v2.0.

## 🚀 Quick Deployment Options

### Option 1: Docker Compose (Recommended for Local Development)

```bash
# Clone and start
git clone https://github.com/aangell98/SocialMediaSentimentTracker.git
cd SocialMediaSentimentTracker
docker-compose up --build
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## ☁️ Cloud Deployment

### Backend Deployment Options

#### Railway
1. Connect your GitHub repository to Railway
2. Set the root directory to `backend`
3. Railway will auto-detect the Dockerfile
4. Set environment variables if needed

#### Render
1. Create a new Web Service
2. Connect your GitHub repository
3. Set build command: `cd backend && pip install -r requirements.txt`
4. Set start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set environment: `PYTHON_VERSION=3.11`

#### AWS (Docker)
```bash
# Build and push to ECR
docker build -t sentiment-api ./backend
docker tag sentiment-api:latest YOUR_ECR_URI/sentiment-api:latest
docker push YOUR_ECR_URI/sentiment-api:latest
```

### Frontend Deployment Options

#### Vercel
1. Connect your GitHub repository
2. Set the root directory to `frontend`
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Add environment variable: `VITE_API_URL=https://your-backend-url`

#### Netlify
1. Connect your GitHub repository
2. Set build directory: `frontend`
3. Set build command: `npm run build`
4. Set publish directory: `frontend/dist`
5. Add environment variable: `VITE_API_URL=https://your-backend-url`

#### GitHub Pages
```bash
cd frontend
npm run build
# Deploy the dist/ folder to gh-pages branch
```

## 🔧 Environment Configuration

### Backend (.env)
```bash
# Optional configurations
MODEL_NAME=nlptown/bert-base-multilingual-uncased-sentiment
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

### Frontend (.env)
```bash
# Update this to your backend URL in production
VITE_API_URL=https://your-backend-domain.com
```

## 🔒 Production Considerations

### Security
- [ ] Configure CORS origins for production
- [ ] Use HTTPS for all endpoints
- [ ] Implement rate limiting
- [ ] Add authentication if needed

### Performance
- [ ] Enable gzip compression
- [ ] Add caching headers
- [ ] Use CDN for frontend assets
- [ ] Monitor API response times

### Monitoring
- [ ] Set up health check endpoints
- [ ] Configure logging and alerts
- [ ] Monitor resource usage
- [ ] Track API usage metrics

## 🧪 Testing Deployment

### Test Backend
```bash
curl https://your-backend-url/health
curl -X POST "https://your-backend-url/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text":"Test message"}'
```

### Test Frontend
1. Open your frontend URL
2. Try analyzing different types of text
3. Check browser console for errors
4. Verify API calls are working

## 🔄 CI/CD Pipeline

The project includes GitHub Actions workflows that:

1. **Backend Pipeline** (`.github/workflows/backend.yml`):
   - Run tests on Python 3.11
   - Build Docker image
   - Test containerized application

2. **Frontend Pipeline** (`.github/workflows/frontend.yml`):
   - Install dependencies
   - Run linting
   - Build for production
   - Test build artifacts

To enable automatic deployment, uncomment and configure the deployment sections in the workflow files.

## 📊 Scaling Considerations

### Backend Scaling
- Use load balancers for multiple instances
- Consider caching for frequently analyzed texts
- Implement database for persistent storage
- Use container orchestration (Kubernetes, Docker Swarm)

### Frontend Scaling
- Use CDN for global distribution
- Implement client-side caching
- Optimize bundle size
- Use service workers for offline support

## 🆘 Troubleshooting

### Common Issues

**Backend not starting:**
- Check if all dependencies are installed
- Verify Python version (3.11+ recommended)
- Check if port 8000 is available

**Frontend can't connect to backend:**
- Verify VITE_API_URL is set correctly
- Check CORS configuration in backend
- Ensure backend is accessible from frontend domain

**Build failures:**
- Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
- Check Node.js version (20+ recommended)
- Verify all environment variables are set

### Getting Help
- Check the logs in the deployment platform
- Test locally first with Docker Compose
- Review the GitHub Actions for build errors
- Open an issue on GitHub for help