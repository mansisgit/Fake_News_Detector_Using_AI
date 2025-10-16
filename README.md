# 🧠 Fake News Detector 📰

A smart, AI-powered app that verifies the authenticity of news using a custom-trained model combined with six real-world verification APIs. Built to tackle the challenge of misleading news by analyzing both linguistic patterns and contextual credibility.

---

## 🌟 Project Intuition & Motivation

Fake news isn't just misleading — it’s dangerous. Traditional ML models can classify text as fake or real, but news articles need **context**, **language analysis**, and **external fact-checking** to make an accurate judgment.

That’s why I went beyond just model training and built an integrated system that combines machine learning with **6 powerful APIs** for real-time credibility analysis.

---

## 🚀 Approach & Architecture

1. **Custom ML Model**
   - Trained on over **50,000+ labeled news articles**
   - Built using **logistic regression**, with preprocessing via NLTK and Scikit-learn
   - Achieved **high accuracy (~98%)** on test data

2. **Layered Validation System**
   - The app first checks the **language and structural patterns** using the ML model.
   - Then, it verifies the **authenticity** of the content by querying **6 fact-checking & credibility APIs**:
      - **NewsAPI**
      - **GNews API**
      - **Google Fact Check Tools API**
      - **MediaStack API**
      - **NewsData.io API**
      - **Currents API**


3. **Streamlit Web App**
   - Clean, modern UI with real-time feedback
   - Dynamically styled feedback boxes (green/red)
   - Context-aware intermediate responses
   - Justified final verdict with AI-generated reasoning

---

## 🛠️ Tech Stack

- **Python** (NLTK, Scikit-learn, Pandas, Requests)
- **Streamlit** (for web app UI)
- **APIs** (for cross-verification)
- **Google Colab** (model training)
- **Git + GitHub** (version control)
- **Mac/Linux & Windows support** (via `.sh` and `.bat` scripts)


---

## 📊 Dataset Info

- Source: Kaggle “Fake and Real News Dataset”
- Data: ~50,000 articles
- Labels: Real vs. Fake
- Focus: Primarily political news (US-based)
- Preprocessing: Tokenization, stopword removal, TF-IDF

---

## 🔐 Why Use APIs?

> “ML models learn language — not truth.”

Since fake news often includes real words with fake contexts, my app integrates **external APIs** to cross-check if the content is verified or disputed elsewhere.

This multi-layered pipeline ensures more **realistic and trustworthy** results.

---

## 📈 Future Improvements

- Auto-news summarization
- Language translation for Urdu & Hindi support
- Real-time news stream monitoring
- Deeper sentiment & emotion detection
