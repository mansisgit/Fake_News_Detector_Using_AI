# 🔐 Setting Up Your `.env` File

This project requires multiple API keys to fetch and verify news content from various platforms. These keys should be stored in a `.env` file in the root directory.

> ⚠️ Do **NOT** share your `.env` file publicly or upload it to GitHub. It contains private credentials and is already included in `.gitignore`.

---

## 📁 Create `.env` in the Root Directory

Create a file named `.env` at the root level of your project.

---

## 🧩 Required Environment Variables

Inside `.env`, paste the following (replace placeholder values with your actual keys):

```env
NEWSAPI_KEY=your_newsapi_key
GNEWS_KEY=your_gnews_key
FACTCHECK_KEY=your_google_factcheck_key
MEDIASTACK_KEY=your_mediastack_key
NEWSDATA_KEY=your_newsdata_key
CURRENTS_KEY=your_currentsapi_key
```

---

## 🔑 How to Get These API Keys

### 1. 📰 NewsAPI
- Sign up at [https://newsapi.org](https://newsapi.org)
- Go to your dashboard and copy the API key  
**Purpose:** Fetches recent news from trusted outlets

---

### 2. 🌍 GNews API
- Register at [https://gnews.io](https://gnews.io)
- Get your API key from the dashboard  
**Purpose:** Provides global news headlines and summaries

---

### 3. ✅ Google Fact Check Tools API
- Visit [Google Cloud Console](https://console.cloud.google.com/)
- Enable "Fact Check Tools API"
- Navigate to **APIs & Services > Credentials** → Create API key  
**Purpose:** Verifies fake news using Google’s public fact checks

---

### 4. 🧾 MediaStack
- Sign up at [https://mediastack.com](https://mediastack.com)
- Copy the key from your account dashboard  
**Purpose:** Offers real-time and historical news data

---

### 5. 📡 NewsData.io
- Register at [https://newsdata.io](https://newsdata.io)
- Get your API key from the dashboard  
**Purpose:** Retrieves archived and live news articles

---

### 6. 🌐 Currents API
- Sign up at [https://currentsapi.services](https://currentsapi.services)
- Copy your personal API key  
**Purpose:** Searches breaking news from multiple global sources

---

✅ Once you’ve added all the above keys to your `.env`, the app will be able to access all services safely and privately.

---

> Need help? Feel free to raise an issue or connect via discussions tab.
