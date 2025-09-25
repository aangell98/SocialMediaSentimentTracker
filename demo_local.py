#!/usr/bin/env python3
"""
Local demo of sentiment analysis without requiring external dependencies
"""

import sys
import os

# Add the backend directory to the path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

from app.analysis_mock import analyze_sentiment

def demo_analysis():
    print("🎭 Local Sentiment Analysis Demo")
    print("="*50)
    
    test_cases = [
        "I absolutely love this new design! It's amazing and wonderful!",
        "This is terrible and awful, worst experience ever!",
        "It's okay, nothing special really.",
        "Great work on the project, fantastic job everyone!",
        "Not bad, but could be better with some improvements.",
        "Amazing results! I'm so excited about this project.",
        "Disappointing performance, really frustrating to use.",
        "The service is adequate for basic needs."
    ]
    
    print("\n📊 Analyzing various texts...")
    print("-" * 50)
    
    for i, text in enumerate(test_cases, 1):
        try:
            result = analyze_sentiment(text)
            sentiment = result['label'].upper()
            confidence = result['score'] * 100
            
            # Choose emoji based on sentiment
            if result['label'] == 'positive':
                emoji = "😊"
                color = "✅"
            elif result['label'] == 'negative':
                emoji = "😞" 
                color = "❌"
            else:
                emoji = "😐"
                color = "⚪"
            
            print(f"\n{i}. 📝 Text: \"{text}\"")
            print(f"   {color} {emoji} Result: {sentiment} ({confidence:.1f}% confidence)")
            
        except Exception as e:
            print(f"   ❌ Error analyzing text {i}: {e}")
    
    print("\n" + "="*50)
    print("✅ Local demo completed!")
    print("💡 This demonstrates the sentiment analysis logic")
    print("🚀 For full API demo, run the backend and use demo.py")
    print("="*50)

if __name__ == "__main__":
    demo_analysis()