import os
import requests
import re
import json
# 1. Import VADER
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Replace with your actual API key
API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyDfpECcL7gshs8hynaMjhnGGWDLOVcnvf4")

# Test video ID (e.g., from any popular podcast or video)
# In YouTube URLs: youtube.com/watch?v=VIDEO_ID
VIDEO_ID = "YMTJw1G3yOM"  # Replace with any valid YouTube Video ID

COMMON_FAQ_PATTERNS = {
    "gear_setup": [r"\bmic\b", r"\bcamera\b", r"\bsetup\b", r"\blighting\b", r"\bwhich mic\b"],
    "book_recommendation": [r"\bbook\b", r"\bbooks\b", r"\breading\b", r"\bauthor\b"],
    "guest_request": [r"\bnext guest\b", r"\bbring\b", r"\binvite\b", r"\bplease call\b"],
    "financials": [r"\bnet worth\b", r"\bearning\b", r"\bsalary\b", r"\binvestment\b", r"\bhow much do you make\b"],
}

def fetch_raw_comments(video_id: str, api_key: str, max_results: int = 50) -> dict:
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": api_key,
        "maxResults": max_results,
        "order": "relevance",
        "textFormat": "plainText"
    }
    
    print(f"[*] Fetching top {max_results} comments for Video ID: {video_id}...")
    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        return {}
    return response.json()

def classify_comment(text: str) -> list[str]:
    text_lower = text.lower()
    matched_categories = []
    for category, patterns in COMMON_FAQ_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                matched_categories.append(category)
                break  
    return matched_categories

def parse_and_filter_comments(raw_data: dict) -> list[dict]:
    # 2. Initialize the Sentiment Analyzer
    analyzer = SentimentIntensityAnalyzer()
    
    items = raw_data.get("items", [])
    processed_records = []

    for item in items:
        top_comment = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
        text = top_comment.get("textOriginal", "")
        author = top_comment.get("authorDisplayName", "Unknown")
        likes = top_comment.get("likeCount", 0)

        if not text:
            continue

        matched_faqs = classify_comment(text)
        is_question = "?" in text or any(text.lower().startswith(w) for w in ["what", "why", "how", "where", "who", "which"])

        # 3. Calculate Sentiment
        # VADER returns a dictionary like: {'neg': 0.0, 'neu': 0.5, 'pos': 0.5, 'compound': 0.8}
        sentiment_scores = analyzer.polarity_scores(text)
        compound_score = sentiment_scores['compound']
        
        # 4. Categorize the compound score
        if compound_score >= 0.05:
            sentiment_label = "Positive"
        elif compound_score <= -0.05:
            sentiment_label = "Critical (Negative)"
        else:
            sentiment_label = "Neutral"

        processed_records.append({
            "author": author,
            "text": text,
            "likes": likes,
            "is_question": is_question,
            "faq_tags": matched_faqs,
            "sentiment_label": sentiment_label,
            "sentiment_score": round(compound_score, 2)
        })

    return processed_records

if __name__ == "__main__":
    raw_data = fetch_raw_comments(VIDEO_ID, API_KEY, max_results=50)

    if raw_data:
        cleaned_data = parse_and_filter_comments(raw_data)
        
        output_file = "processed_comments.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

        total = len(cleaned_data)
        critical = sum(1 for c in cleaned_data if c["sentiment_label"] == "Critical (Negative)")
        positive = sum(1 for c in cleaned_data if c["sentiment_label"] == "Positive")

        print(f"\n[+] Processing Complete!")
        print(f"    - Total Comments Parsed: {total}")
        print(f"    - Overwhelmingly Positive: {positive}")
        print(f"    - Needs PR Review (Critical): {critical}")
        print(f"    - Results saved to '{output_file}'")