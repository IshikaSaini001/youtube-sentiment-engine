# 📊 YouTube Creator Sentiment & FAQ Analysis Engine

An automated data pipeline built in Python to extract, structure, and analyze YouTube comment sections. The tool parses audience discussions, identifies recurring FAQ patterns ("Already Answered" questions), and computes social sentiment scores using rule-based NLP to flag potential PR issues.

---

## 🚀 Key Features

* **Automated API Ingestion:** Direct integration with YouTube Data API v3 to fetch comment threads using standard query parameters and relevance sorting.
* **Recurring FAQ Classifier:** Regex-based classification engine to flag redundant questions across common creator topics (gear/equipment, book recommendations, guest requests, financial queries).
* **VADER Sentiment Analysis:** Lexicon and rule-based sentiment scoring specifically optimized for social media text, classifying comments into `Positive`, `Neutral`, and `Critical (Negative)` categories.
* **Defensive Data Handling:** Resilient JSON parsing utilizing defensive dictionary traversal (`.get()`) to safely handle missing fields, edge-case characters, and malformed API responses.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **APIs & Libraries:**
  * `requests` — HTTP communication with YouTube Data API v3
  * `vaderSentiment` — Rule-based social sentiment analysis
  * `json` & `re` — Standard library data serialization and regex pattern matching

---

## 📁 Project Structure

```text
youtube-sentiment-engine/
├── scraper.py                 # Core extraction, classification & sentiment logic
├── requirements.txt           # Environment dependencies
├── .gitignore                 # Excluded environments and sensitive tokens
├── README.md                  # Project documentation
└── processed_comments.json    # Sample structured output (local only)

```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/YOUR_USERNAME/youtube-sentiment-engine.git](https://github.com/YOUR_USERNAME/youtube-sentiment-engine.git)
cd youtube-sentiment-engine

```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv workvenv
source workvenv/bin/activate  # On Windows: workvenv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## 🔑 Configuration & Usage

1. **Obtain API Key:** Get a free YouTube Data API v3 key from the [Google Cloud Console](https://console.cloud.google.com/).
2. **Set Environment Variable:**
```bash
export YOUTUBE_API_KEY="your_api_key_here"

```


*(Or replace the default fallback string in `scraper.py` during local debugging).*
3. **Run the Script:**
```bash
python scraper.py

```



---

## 📊 Sample Output Schema

The extracted and analyzed data is structured into a clean JSON output:

```json
[
  {
    "author": "@tech_enthusiast",
    "text": "What camera and mic are you using for this podcast setup?",
    "likes": 14,
    "is_question": true,
    "faq_tags": ["gear_setup"],
    "sentiment_label": "Neutral",
    "sentiment_score": 0.0
  },
  {
    "author": "@great_insights",
    "text": "This was an incredible breakdown! Best episode so far.",
    "likes": 52,
    "is_question": false,
    "faq_tags": [],
    "sentiment_label": "Positive",
    "sentiment_score": 0.85
  }
]

```

---

## 🔍 Limitations & Future Enhancements

* **Contextual Nuance & Sarcasm:** VADER relies on a pre-built lexicon; subtle cultural context, Hinglish slang, or heavy sarcasm may require fine-tuned transformer models (e.g., RoBERTa).
* **Pagination:** Current implementation fetches the top batch of relevant comments; scaling to thousands of comments per video involves handling pagination tokens (`nextPageToken`).

