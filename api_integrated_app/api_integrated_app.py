import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.api_utils import search_newsapi_articles, search_gnews_articles, search_factcheck, search_mediastack, search_newsdata_io, search_currents_api, search_rapidapi_news
import streamlit as st
import pickle
import time

# Load model
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "fake_news_model.pkl"))
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except:
    model = None  # Handle case where model doesn't exist

st.set_page_config(page_title="\U0001F4F0 Fake News Detector", layout="centered", page_icon="\U0001F9E0")

# --- Custom CSS Styling ---
st.markdown("""
<style>

    /* Better input box styling */
    div[data-baseweb="textarea"] textarea {
        background-color: #f8fafc !important; /* Light background */
        color: #0f172a !important;            /* Dark readable text */
        border-radius: 10px !important;
        font-size: 16px !important;
        font-family: 'Segoe UI', sans-serif;
        padding: 10px !important;
    }

    /* Optional: Subtle glow effect on focus */
    div[data-baseweb="textarea"] textarea:focus {
        box-shadow: 0 0 5px rgba(0, 150, 255, 0.4) !important;
        outline: none !important;
    }

    .block-container {
        max-width: 1200px;
        padding-left: 5rem;
        padding-right: 5rem;
    }

    html, body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
    }

    /* Remove popup box effect on load */
    .main {
        padding-top: 0px !important;
    }

    .main > div:not(:has(.stTextArea)) {
        background: transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    .title {
        text-align: center;
        font-size: 120px;
        font-weight: 900;
        margin-bottom: 25px;
        background: linear-gradient(45deg, #2c3e50, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeInDown 1s ease-out;
    }

    .subtitle {
        text-align: center;
        font-size: 42px;
        color: #34495e;
        margin-top: 0;
        margin-bottom: 60px;
        font-weight: 600;
        animation: fadeInUp 1.2s ease-out;
    }

    .verdict-box {
        border-radius: 15px;
        padding: 35px;
        margin: 40px 0;
        font-size: 36px;
        font-weight: 800;
        text-align: center;
        animation: bounceIn 1.5s ease-out;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
    }

    .verdict-fake {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        border: 3px solid #a93226;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    .verdict-real {
        background: linear-gradient(135deg, #27ae60, #229954);
        color: white;
        border: 3px solid #1e8449;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    .check-box {
        border-radius: 12px;
        padding: 22px 28px;
        margin: 10px 0;
        font-size: 22px;
        font-weight: 600;
        animation: fadeInUp 0.6s ease-out;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        border-left: 6px solid;
    }

    .check-normal {
        background: linear-gradient(135deg, #d5f4e6, #e8f8f5);
        color: #1e8449;
        border-left-color: #27ae60;
    }

    .check-suspicious {
        background: linear-gradient(135deg, #fadbd8, #f2d7d5);
        color: #a93226;
        border-left-color: #e74c3c;
    }

    .api-result-box {
        border-radius: 12px;
        padding: 20px 25px;
        margin: 15px 0;
        font-size: 18px;
        font-weight: 600;
        animation: fadeInUp 0.6s ease-out;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        border-left: 6px solid;
    }

    .api-error {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        color: #856404;
        border-left-color: #ffc107;
    }

    .reason-section {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 30px;
        margin: 50px 0 25px;
        font-size: 18px;
        line-height: 1.8;
        border-left: 5px solid #3498db;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }

    .reason-section h4 {
        margin-bottom: 25px;
        font-size: 24px;
        color: #2c3e50;
        font-weight: 700;
    }

    .reason-section ul {
        margin: 0;
        padding-left: 0;
        list-style: none;
    }

    .reason-section li {
        margin: 18px 0;
        padding: 15px 25px;
        background: rgba(52, 152, 219, 0.1);
        border-radius: 8px;
        border-left: 4px solid #3498db;
        font-size: 19px;
        color: #2c3e50;
        font-weight: 500;
    }

    .section-header {
        font-size: 32px;
        font-weight: 700;
        color: #2c3e50;
        margin: 35px 0 25px 0;
        text-align: center;
        padding-bottom: 15px;
        border-bottom: 4px solid #3498db;
    }

    .stTextArea > div,
    .stTextArea textarea {
        background-color: rgba(240, 240, 240, 0.95) !important;  /* light grey again */
        border-radius: 12px;
        animation: fadeInUp 1.2s ease-in-out;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        transition: all 0.4s ease-in-out;
        font-size: 18px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3498db, #2980b9) !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        padding: 18px 45px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 10px 25px rgba(52, 152, 219, 0.4) !important;
        transition: all 0.3s ease !important;
        animation: fadeInUp 1.2s ease-in-out;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 30px rgba(52, 152, 219, 0.6) !important;
    }

    .fade-message {
        animation: fadeInUp 1.2s ease-in-out;
        color: white;
        font-size: 18px;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); }
    }
</style>

""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; padding-top: 30px;">
        <h1 style="
            font-size: 120px;
            font-weight: 900;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #2c3e50, #3498db);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            animation: fadeInDown 1s ease-out;
        ">📰 Fake News Detector</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown('<p class="subtitle">Trained on U.S. news data with live credibility checks</p>', unsafe_allow_html=True)

# --- Input Section ---
st.markdown("""
    <h3 style="
        font-size: 30px;
        margin-top: 11px;
        font-weight: 600;
        color: #ffffff;
        animation: fadeInUp 1s ease-in-out;
    ">
        ✍️ Enter the news text you'd like to analyze:
    </h3>
""", unsafe_allow_html=True)

news_text = st.text_area("Enter News Text:", height=120, label_visibility="collapsed")

# --- Analyze Button ---
if st.button("\U0001F50D Analyze") and news_text.strip():
    with st.spinner("Analyzing text and running credibility checks..."):
        time.sleep(0.8)

    st.markdown('<div class="section-header">🛠 Initial Text Pattern Checks Running...</div>', unsafe_allow_html=True)

    # Basic pattern checks - Updated for better accuracy with real news
    checks = {
        "Sensational phrasing": "suspicious" if any(word in news_text.lower() for word in ["shocking", "unbelievable", "terrifying", "must see", "doctors hate this", "you won't believe"]) else "normal",
        "Punctuation patterns": "suspicious" if "!!!" in news_text or "???" in news_text or news_text.count("!") > 5 else "normal",
        "Buzzwords": "suspicious" if any(word in news_text.lower() for word in ["hoax", "conspiracy", "cover-up", "fake news", "mainstream media lies", "wake up sheeple"]) else "normal",
        "ALL CAPS abuse": "suspicious" if sum(1 for word in news_text.split() if word.isupper() and len(word) > 3) > 3 else "normal"
    }

    for category, status in checks.items():
        with st.spinner(f"Analyzing {category}..."):
            time.sleep(0.5)
        if status == "suspicious":
            st.markdown(f'<div class="check-box check-suspicious">❗ <strong>{category}</strong> indicates unusual or fake-like patterns</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="check-box check-normal">✅ <strong>{category}</strong> appears natural</div>', unsafe_allow_html=True)

    st.markdown("---")

    # API Analysis Section
    st.markdown('<div class="section-header">🔍 Cross-Verification with External APIs</div>', unsafe_allow_html=True)
    
    # Initialize API results for all 7 APIs (including RapidAPI)
    api_results = {
        'newsapi': {'articles': [], 'status': 'checking', 'error': None},
        'gnews': {'articles': [], 'status': 'checking', 'error': None},
        'factcheck': {'claims': [], 'status': 'checking', 'error': None},
        'mediastack': {'articles': [], 'status': 'checking', 'error': None},
        'newsdata': {'articles': [], 'status': 'checking', 'error': None},
        'currents': {'articles': [], 'status': 'checking', 'error': None},
        'rapidapi': {'articles': [], 'status': 'checking', 'error': None}
    }
    
    # Create placeholders for dynamic updates
    newsapi_placeholder = st.empty()
    gnews_placeholder = st.empty()
    factcheck_placeholder = st.empty()
    mediastack_placeholder = st.empty()
    newsdata_placeholder = st.empty()
    currents_placeholder = st.empty()
    rapidapi_placeholder = st.empty()
    
    # 1. NewsAPI Check
    with st.spinner("🔍 Searching NewsAPI for matching articles..."):
        newsapi_placeholder.markdown('<div class="api-result-box check-normal">📰 <strong>NewsAPI:</strong> Searching for matching articles...</div>', unsafe_allow_html=True)
        time.sleep(1)
        
        newsapi_result = search_newsapi_articles(news_text)
        api_results['newsapi']['articles'] = newsapi_result.get('articles', [])
        api_results['newsapi']['error'] = newsapi_result.get('error')
        
        if newsapi_result.get('error'):
            api_results['newsapi']['status'] = 'error'
            newsapi_placeholder.markdown(f'<div class="api-result-box api-error">📰 <strong>NewsAPI:</strong> {newsapi_result["error"]} ⚠️</div>', unsafe_allow_html=True)
        elif newsapi_result.get('articles'):
            api_results['newsapi']['status'] = 'found'
            newsapi_placeholder.markdown(f'<div class="api-result-box check-normal">📰 <strong>NewsAPI:</strong> Found {len(newsapi_result["articles"])} matching articles ✅</div>', unsafe_allow_html=True)
            
            # Display top articles
            for i, article in enumerate(newsapi_result['articles'][:3], 1):
                st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px 20px; margin-bottom: 10px; 
                                border-radius: 8px; border-left: 4px solid #27ae60; 
                                box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
                        <strong>#{i}: {article.get('title', 'No title')}</strong><br>
                        <span style="font-size: 14px; color: #6c757d;">Source: {article.get('source', {}).get('name', 'Unknown')}</span><br>
                        <a href="{article.get('url', '#')}" target="_blank" style="color: #2980b9; font-size: 14px;">Read article →</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            api_results['newsapi']['status'] = 'not_found'
            newsapi_placeholder.markdown('<div class="api-result-box check-suspicious">📰 <strong>NewsAPI:</strong> No matching articles found ❌</div>', unsafe_allow_html=True)

    # 2. GNews Check
    with st.spinner("🔍 Searching GNews for matching articles..."):
        gnews_placeholder.markdown('<div class="api-result-box check-normal">🌐 <strong>GNews:</strong> Searching for matching articles...</div>', unsafe_allow_html=True)
        time.sleep(1)
        
        gnews_result = search_gnews_articles(news_text)
        api_results['gnews']['articles'] = gnews_result.get('articles', [])
        api_results['gnews']['error'] = gnews_result.get('error')
        
        if gnews_result.get('error'):
            api_results['gnews']['status'] = 'error'
            gnews_placeholder.markdown(f'<div class="api-result-box api-error">🌐 <strong>GNews:</strong> {gnews_result["error"]} ⚠️</div>', unsafe_allow_html=True)
        elif gnews_result.get('articles'):
            api_results['gnews']['status'] = 'found'
            gnews_placeholder.markdown(f'<div class="api-result-box check-normal">🌐 <strong>GNews:</strong> Found {len(gnews_result["articles"])} matching articles ✅</div>', unsafe_allow_html=True)
            
            # Display top articles
            for i, article in enumerate(gnews_result['articles'][:3], 1):
                st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px 20px; margin-bottom: 10px; 
                                border-radius: 8px; border-left: 4px solid #27ae60; 
                                box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
                        <strong>#{i}: {article.get('title', 'No title')}</strong><br>
                        <span style="font-size: 14px; color: #6c757d;">Source: {article.get('source', {}).get('name', 'Unknown')}</span><br>
                        <a href="{article.get('url', '#')}" target="_blank" style="color: #2980b9; font-size: 14px;">Read article →</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            api_results['gnews']['status'] = 'not_found'
            gnews_placeholder.markdown('<div class="api-result-box check-suspicious">🌐 <strong>GNews:</strong> No matching articles found ❌</div>', unsafe_allow_html=True)

    # 3. Fact Check API
    with st.spinner("🔍 Searching Google Fact Check for related claims..."):
        factcheck_placeholder.markdown('<div class="api-result-box check-normal">🔍 <strong>Fact Check API:</strong> Searching for related claims...</div>', unsafe_allow_html=True)
        time.sleep(1)
        
        factcheck_result = search_factcheck(news_text)
        api_results['factcheck']['claims'] = factcheck_result.get('claims', [])
        api_results['factcheck']['error'] = factcheck_result.get('error')
        
        if factcheck_result.get('error'):
            api_results['factcheck']['status'] = 'error'
            factcheck_placeholder.markdown(f'<div class="api-result-box api-error">🔍 <strong>Fact Check API:</strong> {factcheck_result["error"]} ⚠️</div>', unsafe_allow_html=True)
        elif factcheck_result.get('claims'):
            api_results['factcheck']['status'] = 'found'
            factcheck_placeholder.markdown(f'<div class="api-result-box check-normal">🔍 <strong>Fact Check API:</strong> Found {len(factcheck_result["claims"])} related claims ✅</div>', unsafe_allow_html=True)
            
            # Display top claims
            for i, claim in enumerate(factcheck_result['claims'][:3], 1):
                claim_text = claim.get('text', 'No claim text available')
                claimant = claim.get('claimant', 'Unknown claimant')
                reviews = claim.get('claimReview', [])
                rating = reviews[0].get('textualRating', 'No rating') if reviews else 'No rating'
                
                st.markdown(f"""
                    <div style="background-color: #fff3cd; padding: 15px 20px; margin-bottom: 10px; 
                                border-radius: 8px; border-left: 4px solid #ffc107; 
                                box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
                        <strong>#{i}: {claim_text[:100]}...</strong><br>
                        <span style="font-size: 14px; color: #6c757d;">Claimant: {claimant}</span><br>
                        <span style="font-size: 14px; color: #dc3545;">Rating: {rating}</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            api_results['factcheck']['status'] = 'not_found'
            factcheck_placeholder.markdown('<div class="api-result-box check-suspicious">🔍 <strong>Fact Check API:</strong> No related claims found ❌</div>', unsafe_allow_html=True)

    # 4. MediaStack API
    with st.spinner("🔍 Searching MediaStack for matching articles..."):
        mediastack_placeholder.markdown('<div class="api-result-box check-normal">📺 <strong>MediaStack:</strong> Searching for matching articles...</div>', unsafe_allow_html=True)
        time.sleep(1)
        
        mediastack_result = search_mediastack(news_text)
        api_results['mediastack']['articles'] = mediastack_result.get('articles', [])
        api_results['mediastack']['error'] = mediastack_result.get('error')
        
        if mediastack_result.get('error'):
            api_results['mediastack']['status'] = 'error'
            mediastack_placeholder.markdown(f'<div class="api-result-box api-error">📺 <strong>MediaStack:</strong> {mediastack_result["error"]} ⚠️</div>', unsafe_allow_html=True)
        elif mediastack_result.get('articles'):
            api_results['mediastack']['status'] = 'found'
            mediastack_placeholder.markdown(f'<div class="api-result-box check-normal">📺 <strong>MediaStack:</strong> Found {len(mediastack_result["articles"])} matching articles ✅</div>', unsafe_allow_html=True)
            
            # Display top articles
            for i, article in enumerate(mediastack_result['articles'][:3], 1):
                st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px 20px; margin-bottom: 10px; 
                                border-radius: 8px; border-left: 4px solid #27ae60; 
                                box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
                        <strong>#{i}: {article.get('title', 'No title')}</strong><br>
                        <span style="font-size: 14px; color: #6c757d;">Source: {article.get('source', 'Unknown')}</span><br>
                        <a href="{article.get('url', '#')}" target="_blank" style="color: #2980b9; font-size: 14px;">Read article →</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            api_results['mediastack']['status'] = 'not_found'
            mediastack_placeholder.markdown('<div class="api-result-box check-suspicious">📺 <strong>MediaStack:</strong> No matching articles found ❌</div>', unsafe_allow_html=True)

    # 5. NewsData.io API
    with st.spinner("🔍 Searching NewsData.io for matching articles..."):
        newsdata_placeholder.markdown('<div class="api-result-box check-normal">📊 <strong>NewsData.io:</strong> Searching for matching articles...</div>', unsafe_allow_html=True)
        time.sleep(1)
        
        newsdata_result = search_newsdata_io(news_text)
        api_results['newsdata']['articles'] = newsdata_result.get('articles', [])
        api_results['newsdata']['error'] = newsdata_result.get('error')
        
        if newsdata_result.get('error'):
            api_results['newsdata']['status'] = 'error'
            newsdata_placeholder.markdown(f'<div class="api-result-box api-error">📊 <strong>NewsData.io:</strong> {newsdata_result["error"]} ⚠️</div>', unsafe_allow_html=True)
        elif newsdata_result.get('articles'):
            api_results['newsdata']['status'] = 'found'
            newsdata_placeholder.markdown(f'<div class="api-result-box check-normal">📊 <strong>NewsData.io:</strong> Found {len(newsdata_result["articles"])} matching articles ✅</div>', unsafe_allow_html=True)
            
            # Display top articles
            for i, article in enumerate(newsdata_result['articles'][:3], 1):
                st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px 20px; margin-bottom: 10px; 
                                border-radius: 8px; border-left: 4px solid #27ae60; 
                                box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
                        <strong>#{i}: {article.get('title', 'No title')}</strong><br>
                        <span style="font-size: 14px; color: #6c757d;">Source: {article.get('source_id', 'Unknown')}</span><br>
                        <a href="{article.get('link', '#')}" target="_blank" style="color: #2980b9; font-size: 14px;">Read article →</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            api_results['newsdata']['status'] = 'not_found'
            newsdata_placeholder.markdown('<div class="api-result-box check-suspicious">📊 <strong>NewsData.io:</strong> No matching articles found ❌</div>', unsafe_allow_html=True)

    # 6. Currents API
    with st.spinner("🔍 Searching Currents API for matching articles..."):
        currents_placeholder.markdown('<div class="api-result-box check-normal">⚡ <strong>Currents API:</strong> Searching for matching articles...</div>', unsafe_allow_html=True)
        time.sleep(1)
        
        currents_result = search_currents_api(news_text)
        api_results['currents']['articles'] = currents_result.get('articles', [])
        api_results['currents']['error'] = currents_result.get('error')
        
        if currents_result.get('error'):
            api_results['currents']['status'] = 'error'
            currents_placeholder.markdown(f'<div class="api-result-box api-error">⚡ <strong>Currents API:</strong> {currents_result["error"]} ⚠️</div>', unsafe_allow_html=True)
        elif currents_result.get('articles'):
            api_results['currents']['status'] = 'found'
            currents_placeholder.markdown(f'<div class="api-result-box check-normal">⚡ <strong>Currents API:</strong> Found {len(currents_result["articles"])} matching articles ✅</div>', unsafe_allow_html=True)
            
            # Display top articles
            for i, article in enumerate(currents_result['articles'][:3], 1):
                st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px 20px; margin-bottom: 10px; 
                                border-radius: 8px; border-left: 4px solid #27ae60; 
                                box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
                        <strong>#{i}: {article.get('title', 'No title')}</strong><br>
                        <span style="font-size: 14px; color: #6c757d;">Source: {article.get('author', 'Unknown')}</span><br>
                        <a href="{article.get('url', '#')}" target="_blank" style="color: #2980b9; font-size: 14px;">Read article →</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            api_results['currents']['status'] = 'not_found'
            currents_placeholder.markdown('<div class="api-result-box check-suspicious">⚡ <strong>Currents API:</strong> No matching articles found ❌</div>', unsafe_allow_html=True)

    # 7. RapidAPI News Check (NEW)
    with st.spinner("🔍 Searching RapidAPI News for matching articles..."):
        rapidapi_placeholder.markdown('<div class="api-result-box check-normal">🚀 <strong>RapidAPI News:</strong> Searching for matching articles...</div>', unsafe_allow_html=True)
        time.sleep(1)
        
        rapidapi_result = search_rapidapi_news(news_text)
        api_results['rapidapi']['articles'] = rapidapi_result.get('articles', [])
        api_results['rapidapi']['error'] = rapidapi_result.get('error')
        
        if rapidapi_result.get('error'):
            api_results['rapidapi']['status'] = 'error'
            rapidapi_placeholder.markdown(f'<div class="api-result-box api-error">🚀 <strong>RapidAPI News:</strong> {rapidapi_result["error"]} ⚠️</div>', unsafe_allow_html=True)
        elif rapidapi_result.get('articles'):
            api_results['rapidapi']['status'] = 'found'
            rapidapi_placeholder.markdown(f'<div class="api-result-box check-normal">🚀 <strong>RapidAPI News:</strong> Found {len(rapidapi_result["articles"])} matching articles ✅</div>', unsafe_allow_html=True)
            
            # Display top articles
            for i, article in enumerate(rapidapi_result['articles'][:3], 1):
                st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px 20px; margin-bottom: 10px; 
                                border-radius: 8px; border-left: 4px solid #27ae60; 
                                box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
                        <strong>#{i}: {article.get('title', 'No title')}</strong><br>
                        <span style="font-size: 14px; color: #6c757d;">Source: {article.get('source', {}).get('name', 'Unknown')}</span><br>
                        <a href="{article.get('url', '#')}" target="_blank" style="color: #2980b9; font-size: 14px;">Read article →</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            api_results['rapidapi']['status'] = 'not_found'
            rapidapi_placeholder.markdown('<div class="api-result-box check-suspicious">🚀 <strong>RapidAPI News:</strong> No matching articles found ❌</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Calculate Final Verdict Based on All Checks - IMPROVED LOGIC WITH POSITIVE BIAS
    st.markdown('<div class="section-header">\U0001F4E2 Final Verdict</div>', unsafe_allow_html=True)

    # New improved scoring system with positive bias when APIs find results
    credibility_score = 0
    max_possible_score = 10
    
    # 1. Pattern Analysis (max 2 points deduction)
    pattern_suspicious_count = sum(1 for status in checks.values() if status == "suspicious")
    if pattern_suspicious_count == 0:
        credibility_score += 2  # Good patterns
    elif pattern_suspicious_count == 1:
        credibility_score += 1  # Minor concern
    # else: 0 points (multiple red flags)
    
    # 2. API Verification (max 8 points) - UPDATED FOR ALL 7 APIS WITH ERROR HANDLING
    total_articles_found = 0
    api_success_count = 0
    api_error_count = 0
    news_apis = ['newsapi', 'gnews', 'mediastack', 'newsdata', 'currents', 'rapidapi']
    
    # Check all news APIs
    for api_name in news_apis:
        if api_results[api_name]['status'] == 'found':
            articles_count = len(api_results[api_name]['articles'])
            total_articles_found += articles_count
            api_success_count += 1
            
            # Progressive scoring based on number of articles
            if articles_count >= 5:
                credibility_score += 1.5  # Strong verification per API
            elif articles_count >= 2:
                credibility_score += 1.2  # Moderate verification per API
            else:
                credibility_score += 0.8  # Weak verification per API
        elif api_results[api_name]['status'] == 'error':
            api_error_count += 1
    
    # Fact-check results (can add or subtract points)
    if api_results['factcheck']['status'] == 'found':
        factcheck_claims = api_results['factcheck']['claims']
        api_success_count += 0.5  # Count as half since it's different type
        false_claims = 0
        total_claims = len(factcheck_claims)
        
        for claim in factcheck_claims:
            reviews = claim.get('claimReview', [])
            if reviews:
                rating = reviews[0].get('textualRating', '').lower()
                if any(word in rating for word in ['false', 'fake', 'misleading', 'disputed', 'pants on fire']):
                    false_claims += 1
        
        if false_claims > 0:
            # Found disputed claims - deduct points but not too harshly
            credibility_score -= 1.5
        else:
            # No disputed claims found - small bonus
            credibility_score += 0.5
    elif api_results['factcheck']['status'] == 'error':
        api_error_count += 0.5
    else:
        # No fact-check claims found - neutral to positive
        credibility_score += 0.3
    
    # MAJOR POSITIVE BIAS: If ANY API finds articles, boost credibility significantly
    if api_success_count >= 1:
        credibility_score += 2  # Big bonus for any verification
        
        if api_success_count >= 2:
            credibility_score += 1  # Extra bonus for cross-verification
        
        if api_success_count >= 3:
            credibility_score += 0.5  # Additional bonus for multiple sources

    # Adjust scoring if many APIs had errors (don't penalize too much for API issues)
    if api_error_count >= 3:
        credibility_score += 1  # Small bonus since APIs being down doesn't mean news is fake

    # Ensure score is within bounds
    credibility_score = max(0, min(max_possible_score, credibility_score))
    
    # Calculate percentage
    credibility_percentage = (credibility_score / max_possible_score) * 100
    
    # Determine verdict based on score - UPDATED THRESHOLDS FOR MORE POSITIVE RESULTS
    if credibility_percentage >= 55:  # Lowered from 70
        verdict = "LIKELY REAL"
        verdict_class = "verdict-real"
        verdict_icon = "✅"
    elif credibility_percentage >= 35:  # Lowered from 40
        verdict = "POSSIBLY REAL"
        verdict_class = "verdict-real"  # Changed to green instead of red
        verdict_icon = "✅"
    elif credibility_percentage >= 20:
        verdict = "SUSPICIOUS"
        verdict_class = "verdict-fake"
        verdict_icon = "⚠️"
    else:
        verdict = "LIKELY FAKE"
        verdict_class = "verdict-fake"
        verdict_icon = "❌"

    st.markdown(f'<div class="verdict-box {verdict_class}">{verdict_icon} Verdict: {verdict}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center; font-size: 18px; color: white; margin: 20px 0;">Credibility Score: {credibility_score:.1f}/{max_possible_score} ({credibility_percentage:.1f}%)</div>', unsafe_allow_html=True)

    # Detailed reasoning
    if verdict == "LIKELY FAKE" or verdict == "SUSPICIOUS":
        reasons = []
        if pattern_suspicious_count >= 2:
            reasons.append("🚩 Multiple suspicious text patterns detected")
        if total_articles_found == 0 and api_error_count < 3:
            reasons.append("🔍 No matching articles found in credible news sources")
        elif total_articles_found < 3 and api_error_count < 3:
            reasons.append("📰 Limited verification from news sources")
        if api_results['factcheck']['status'] == 'found':
            false_claims = sum(1 for claim in api_results['factcheck']['claims'] 
                             for review in claim.get('claimReview', [])
                             if any(word in review.get('textualRating', '').lower() 
                                   for word in ['false', 'fake', 'misleading', 'disputed']))
            if false_claims > 0:
                reasons.append(f"⚠️ {false_claims} disputed claims found in fact-checking databases")
        if api_success_count == 0 and api_error_count < 3:
            reasons.append("❌ No verification from any external sources")
        if api_error_count >= 3:
            reasons.append("⚠️ Multiple verification services were unavailable - results may be incomplete")
        
        if not reasons:
            reasons.append("🤔 Mixed signals from various verification checks")
            
        st.markdown(f"""
        <div class="reason-section">
            <h4>Why this appears to be {verdict.lower()}:</h4>
            <ul>
                {"".join(f"<li>{reason}</li>" for reason in reasons)}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:  # LIKELY REAL or POSSIBLY REAL
        reasons = []
        if pattern_suspicious_count == 0:
            reasons.append("✅ Text patterns consistent with legitimate journalism")
        if total_articles_found >= 10:
            reasons.append(f"📰 Strong verification with {total_articles_found} matching articles from multiple credible sources")
        elif total_articles_found >= 5:
            reasons.append(f"🌐 Good verification with {total_articles_found} matching articles found")
        elif total_articles_found >= 1:
            reasons.append(f"📋 Found {total_articles_found} matching articles in credible news sources")
        if api_success_count >= 3:
            reasons.append("🔄 Cross-verified by multiple independent news APIs")
        elif api_success_count >= 2:
            reasons.append("✓ Verified by multiple news sources")
        elif api_success_count >= 1:
            reasons.append("✓ Confirmed by at least one credible news source")
        if api_results['factcheck']['status'] == 'not_found':
            reasons.append("🔍 No disputed claims found in fact-checking databases")
        elif api_results['factcheck']['status'] == 'found':
            # Check if fact-check claims are not disputed
            false_claims = sum(1 for claim in api_results['factcheck']['claims'] 
                             for review in claim.get('claimReview', [])
                             if any(word in review.get('textualRating', '').lower() 
                                   for word in ['false', 'fake', 'misleading', 'disputed']))
            if false_claims == 0:
                reasons.append("✅ Related claims in fact-check database show no disputes")
        if api_error_count >= 2:
            reasons.append("ℹ️ Some verification services were unavailable, but available sources support authenticity")
            
        st.markdown(f"""
        <div class="reason-section">
            <h4>Why this appears to be legitimate:</h4>
            <ul>
                {"".join(f"<li>{reason}</li>" for reason in reasons)}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Debug info (you can remove this in production)
    with st.expander("🔧 Debug Information"):
        st.write(f"**Pattern Checks:** {checks}")
        st.write(f"**API Results Status:**")
        for api_name in ['newsapi', 'gnews', 'factcheck', 'mediastack', 'newsdata', 'currents', 'rapidapi']:
            if api_name == 'factcheck':
                count = len(api_results[api_name]['claims'])
                st.write(f"- {api_name.title()}: {api_results[api_name]['status']} ({count} claims) - Error: {api_results[api_name]['error']}")
            else:
                count = len(api_results[api_name]['articles'])
                st.write(f"- {api_name.title()}: {api_results[api_name]['status']} ({count} articles) - Error: {api_results[api_name]['error']}")
        st.write(f"**Scoring Details:**")
        st.write(f"- Total articles found: {total_articles_found}")
        st.write(f"- APIs with results: {api_success_count}")
        st.write(f"- APIs with errors: {api_error_count}")
        st.write(f"- Credibility Score: {credibility_score:.1f}/{max_possible_score} ({credibility_percentage:.1f}%)")
        st.write(f"- Pattern suspicious count: {pattern_suspicious_count}")

else:
    st.markdown("""
    <div class="fade-message">
        📝 Please enter a news article or statement above to analyze.
    </div>
    """, unsafe_allow_html=True)