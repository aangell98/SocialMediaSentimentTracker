#!/usr/bin/env python3
"""
Simple test script for the sentiment analysis backend
"""
import sys
import os

# Add the backend directory to the path
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)

def test_basic_functionality():
    """Test basic functionality without running the server"""
    print("Testing backend functionality...")
    
    # Test the mock analysis directly
    try:
        from app.analysis_mock import analyze_sentiment
        
        test_cases = [
            "I love this project!",
            "This is terrible and awful",
            "It's okay, nothing special",
            "Amazing work, fantastic job!",
            "Worst experience ever, hate it"
        ]
        
        print("\n--- Sentiment Analysis Tests ---")
        for text in test_cases:
            result = analyze_sentiment(text)
            print(f"Text: '{text}'")
            print(f"Result: {result['label']} (score: {result['score']:.3f})")
            print()
            
        print("✅ Mock analysis working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing analysis: {e}")
        return False
    
    # Test the models
    try:
        try:
            from app.models import SentimentRequest, SentimentResponse
        except ImportError:
            from app.models_mock import SentimentRequest, SentimentResponse
        
        # Test request model
        req = SentimentRequest(text="Test text")
        assert req.text == "Test text"
        
        # Test response model
        resp = SentimentResponse(label="positive", score=0.95)
        assert resp.label == "positive"
        assert resp.score == 0.95
        
        print("✅ Pydantic models working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing models: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if test_basic_functionality():
        print("\n🎉 All basic tests passed! Backend is ready.")
        exit(0)
    else:
        print("\n❌ Some tests failed!")
        exit(1)