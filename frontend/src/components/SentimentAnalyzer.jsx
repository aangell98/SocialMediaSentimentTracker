import { useState } from "react";
import axios from "axios";
import { Loader2, Link, BarChart2, MessageSquare, ThumbsUp, ThumbsDown, Meh } from "lucide-react";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const SentimentAnalyzer = () => {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url) {
      setError("Por favor, introduce una URL de un post de Reddit.");
      return;
    }
    setIsLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/reddit/analyze`, {
        post_url: url,
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Ocurrió un error al contactar la API.");
    } finally {
      setIsLoading(false);
    }
  };

  const getSentimentIcon = (sentiment) => {
    switch (sentiment) {
      case "positive": return <ThumbsUp className="text-green-500" />;
      case "negative": return <ThumbsDown className="text-red-500" />;
      default: return <Meh className="text-yellow-500" />;
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-4 md:p-8">
      <div className="bg-slate-800 p-6 rounded-xl shadow-lg">
        <h1 className="text-3xl font-bold text-center mb-2 text-white">Reddit Sentiment Tracker</h1>
        <p className="text-center text-slate-400 mb-6">Pega la URL de un post de Reddit para analizar la opinión pública.</p>
        
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-grow">
            <Link className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.reddit.com/r/..."
              className="w-full bg-slate-700 text-white border border-slate-600 rounded-lg py-3 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="bg-sky-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-sky-700 transition-colors disabled:bg-slate-600 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isLoading ? <><Loader2 className="animate-spin" /> Analizando...</> : "Analizar Post"}
          </button>
        </form>
        {error && <p className="text-red-400 text-center mt-4">{error}</p>}
      </div>

      {isLoading && (
        <div className="text-center mt-8">
          <Loader2 className="animate-spin inline-block text-sky-500" size={48} />
          <p className="text-slate-300 mt-2">Obteniendo y analizando comentarios... Esto puede tardar un momento.</p>
        </div>
      )}

      {result && (
        <div className="mt-8">
          {/* Summary Section */}
          <div className="bg-slate-800 p-6 rounded-xl shadow-lg mb-6">
            <h2 className="text-xl font-bold text-white mb-4">Análisis del Post: "{result.summary.post_title}"</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
              <div className="bg-green-500/20 p-4 rounded-lg">
                <p className="text-3xl font-bold text-green-400">{result.summary.positive_count}</p>
                <p className="text-green-300">Positivos</p>
              </div>
              <div className="bg-red-500/20 p-4 rounded-lg">
                <p className="text-3xl font-bold text-red-400">{result.summary.negative_count}</p>
                <p className="text-red-300">Negativos</p>
              </div>
              <div className="bg-yellow-500/20 p-4 rounded-lg">
                <p className="text-3xl font-bold text-yellow-400">{result.summary.neutral_count}</p>
                <p className="text-yellow-300">Neutrales</p>
              </div>
            </div>
            <div className="mt-4">
                <p className="text-slate-400 text-center">Total de comentarios analizados: <span className="font-bold text-white">{result.summary.total_comments_analyzed}</span></p>
            </div>
          </div>

          {/* Comments List */}
          <div className="bg-slate-800 p-6 rounded-xl shadow-lg">
            <h3 className="text-lg font-bold text-white mb-4">Comentarios Destacados</h3>
            <div className="space-y-4 max-h-[60vh] overflow-y-auto pr-2">
              {result.comments.map((comment, index) => (
                <div key={index} className="bg-slate-700/50 p-4 rounded-lg border-l-4 border-slate-600 flex gap-4">
                  <div className="flex-shrink-0 mt-1">{getSentimentIcon(comment.sentiment)}</div>
                  <div>
                    <p className="text-slate-300 text-sm">"{comment.text}"</p>
                    <p className="text-xs text-slate-500 mt-2">- u/{comment.author}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SentimentAnalyzer;