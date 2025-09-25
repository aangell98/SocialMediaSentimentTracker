import { useState } from 'react';
import axios from 'axios';
import { Loader2, MessageSquare, TrendingUp, TrendingDown, Minus } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const SentimentAnalyzer = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  const getSentimentIcon = (label) => {
    switch (label) {
      case 'positive':
        return <TrendingUp className="w-5 h-5 text-positive" />;
      case 'negative':
        return <TrendingDown className="w-5 h-5 text-negative" />;
      default:
        return <Minus className="w-5 h-5 text-neutral" />;
    }
  };

  const getSentimentColor = (label) => {
    switch (label) {
      case 'positive':
        return 'text-positive bg-green-50 border-green-200';
      case 'negative':
        return 'text-negative bg-red-50 border-red-200';
      default:
        return 'text-neutral bg-gray-50 border-gray-200';
    }
  };

  const analyzeSentiment = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, {
        text: text.trim()
      });

      const newResult = {
        id: Date.now(),
        text: text.trim(),
        ...response.data,
        timestamp: new Date().toLocaleString()
      };

      setResult(newResult);
      setHistory(prev => [newResult, ...prev.slice(0, 9)]); // Keep last 10 results
      setText('');
    } catch (err) {
      console.error('Error analyzing sentiment:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to analyze sentiment. Make sure the backend is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      analyzeSentiment();
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          🎭 Sentiment Analysis
        </h1>
        <p className="text-lg text-gray-600">
          Analyze the emotional tone of your text using advanced AI
        </p>
      </div>

      {/* Main Input Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="mb-4">
          <label htmlFor="textInput" className="block text-sm font-medium text-gray-700 mb-2">
            Enter text to analyze:
          </label>
          <textarea
            id="textInput"
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your text here... (Press Enter to analyze)"
            className="w-full h-32 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
            maxLength={2000}
            disabled={loading}
          />
          <div className="flex justify-between items-center mt-2">
            <span className="text-sm text-gray-500">
              {text.length}/2000 characters
            </span>
            <button
              onClick={analyzeSentiment}
              disabled={loading || !text.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <MessageSquare className="w-4 h-4" />
                  Analyze Sentiment
                </>
              )}
            </button>
          </div>
        </div>
        
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
            {error}
          </div>
        )}
      </div>

      {/* Current Result */}
      {result && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Analysis Result</h2>
          <div className="border-l-4 border-blue-500 pl-4 mb-4">
            <p className="text-gray-700 italic">"{result.text}"</p>
          </div>
          <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full border ${getSentimentColor(result.label)}`}>
            {getSentimentIcon(result.label)}
            <span className="font-semibold capitalize">{result.label}</span>
            <span className="text-sm">({(result.score * 100).toFixed(1)}% confidence)</span>
          </div>
          <div className="mt-4 bg-gray-100 rounded-md p-3">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${
                  result.label === 'positive' ? 'bg-positive' : 
                  result.label === 'negative' ? 'bg-negative' : 'bg-neutral'
                }`}
                style={{ width: `${result.score * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
      )}

      {/* History */}
      {history.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Analysis History</h2>
          <div className="space-y-4">
            {history.map((item) => (
              <div key={item.id} className="border-b border-gray-100 pb-4 last:border-b-0">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <p className="text-gray-700 text-sm mb-2">{item.text}</p>
                    <div className="flex items-center gap-4">
                      <div className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm border ${getSentimentColor(item.label)}`}>
                        {getSentimentIcon(item.label)}
                        <span className="capitalize">{item.label}</span>
                        <span>({(item.score * 100).toFixed(1)}%)</span>
                      </div>
                      <span className="text-xs text-gray-500">{item.timestamp}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SentimentAnalyzer;