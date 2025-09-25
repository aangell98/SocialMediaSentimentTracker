#!/usr/bin/env python3
"""
Demo script for the Sentiment Analysis API
Shows how to use the API programmatically
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_api_connection():
    """Test if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and healthy!")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print("Make sure the backend is running on http://localhost:8000")
        return False

def analyze_text(text):
    """Analyze sentiment of a single text"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"text": text},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def demo_single_analysis():
    """Demo single text analysis"""
    print("\n" + "="*50)
    print("SINGLE TEXT ANALYSIS DEMO")
    print("="*50)
    
    test_texts = [
        "I absolutely love this new design! It's amazing!",
        "This is terrible, I hate everything about it.",
        "It's okay, nothing special really.",
        "¡Me encanta este proyecto! Es fantástico.",
        "C'est vraiment horrible, je déteste ça.",
    ]
    
    for text in test_texts:
        print(f"\n📝 Text: {text}")
        result = analyze_text(text)
        if result:
            sentiment = result['label'].upper()
            confidence = result['score'] * 100
            emoji = "😊" if result['label'] == 'positive' else "😞" if result['label'] == 'negative' else "😐"
            print(f"   {emoji} Sentiment: {sentiment} ({confidence:.1f}% confidence)")
        time.sleep(0.5)  # Small delay for readability

def demo_batch_analysis():
    """Demo batch analysis"""
    print("\n" + "="*50)
    print("BATCH ANALYSIS DEMO")
    print("="*50)
    
    batch_texts = [
        "Great product, highly recommend!",
        "Poor quality, disappointing experience",
        "Average service, nothing noteworthy",
        "Outstanding customer support team!",
        "Could be better, needs improvement"
    ]
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/batch-analyze",
            json=batch_texts,
            timeout=15
        )
        
        if response.status_code == 200:
            results = response.json()
            print(f"📊 Analyzed {results['count']} texts:")
            for i, result in enumerate(results['results'], 1):
                sentiment = result['sentiment']['label'].upper()
                confidence = result['sentiment']['score'] * 100
                emoji = "😊" if result['sentiment']['label'] == 'positive' else "😞" if result['sentiment']['label'] == 'negative' else "😐"
                print(f"   {i}. {emoji} {sentiment} ({confidence:.1f}%) - {result['text']}")
        else:
            print(f"Batch analysis failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Batch request failed: {e}")

def main():
    print("🎭 Sentiment Analysis API Demo")
    print("This script demonstrates the API functionality")
    
    # Test API connection
    if not test_api_connection():
        print("\n💡 To start the backend:")
        print("   cd backend")
        print("   uvicorn app.main:app --reload")
        return
    
    # Run demos
    demo_single_analysis()
    demo_batch_analysis()
    
    print("\n" + "="*50)
    print("✅ Demo completed successfully!")
    print("🌐 Visit http://localhost:8000/docs for API documentation")
    print("🎨 Visit http://localhost:5173 for the web interface")
    print("="*50)

if __name__ == "__main__":
    main()