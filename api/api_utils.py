# File: api/api_utils.py
import requests
import os
from dotenv import load_dotenv
import urllib.parse
import re
import time

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GNEWS_KEY = os.getenv("GNEWS_KEY")
FACTCHECK_KEY = os.getenv("FACTCHECK_KEY")
MEDIASTACK_KEY = os.getenv("MEDIASTACK_KEY")
NEWSDATA_KEY = os.getenv("NEWSDATA_KEY")
CURRENTS_KEY = os.getenv("CURRENTS_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def extract_keywords(text, max_words=8):
    """Extract key terms from the news text for better API search"""
    # For headlines and short text, use more liberal extraction
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'this', 'that', 'these', 'those'}
    
    # Clean the text but preserve important punctuation context
    words = []
    for word in text.split():
        # Remove punctuation but keep apostrophes for contractions
        clean_word = word.strip('.,!?":;()[]{}').replace('"', '').replace('"', '')
        if len(clean_word) > 2 and clean_word.lower() not in stop_words:
            words.append(clean_word)
    
    # For very short text (likely headlines), be more generous
    if len(text.split()) <= 15:
        return ' '.join(words[:max_words])
    else:
        # For longer text, be more selective
        return ' '.join(words[:6])

def clean_query_for_gnews(query):
    """Clean query specifically for GNews API to avoid syntax errors"""
    # Remove problematic characters and patterns that cause 400 errors
    cleaned = re.sub(r'[^\w\s-]', ' ', query)  # Keep only alphanumeric, whitespace, and hyphens
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()  # Normalize whitespace
    # Limit length to avoid issues
    if len(cleaned) > 100:
        cleaned = cleaned[:100].rsplit(' ', 1)[0]  # Cut at word boundary
    return cleaned

def search_newsapi_articles(query):
    """Search NewsAPI for articles matching the query"""
    if not NEWSAPI_KEY:
        return {"error": "API key not configured", "articles": []}
    
    # Try multiple search strategies
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 8),  # Then keywords
        extract_keywords(query, 4)   # Fallback with fewer keywords
    ]
    
    for search_query in search_queries:
        if not search_query:
            continue
            
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": search_query,
            "apiKey": NEWSAPI_KEY,
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 15,
            "searchIn": "title,description,content"
        }
        
        try:
            response = requests.get(url, params=params, timeout=20)
            print(f"NewsAPI Status Code: {response.status_code}")
            print(f"NewsAPI Search Query: '{search_query}'")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                print(f"NewsAPI found {len(articles)} articles with query: '{search_query}'")
                if articles:  # Return first successful result
                    return {"error": None, "articles": articles}
            elif response.status_code == 429:
                return {"error": "Rate limit exceeded - please try again later", "articles": []}
            elif response.status_code == 401:
                return {"error": "Invalid API key", "articles": []}
            else:
                print(f"NewsAPI Error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            return {"error": "Request timed out - API may be slow", "articles": []}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection failed - API may be down", "articles": []}
        except Exception as e:
            print(f"NewsAPI Exception with query '{search_query}': {e}")
            continue
    
    return {"error": None, "articles": []}

def search_gnews_articles(query):
    """Search GNews for articles matching the query"""
    if not GNEWS_KEY:
        return {"error": "API key not configured", "articles": []}
    
    # Try multiple search strategies with improved cleaning
    search_queries = [
        clean_query_for_gnews(query.strip()),  # Original query first, cleaned
        clean_query_for_gnews(extract_keywords(query, 6)),  # Then keywords
        clean_query_for_gnews(extract_keywords(query, 3))   # Fallback with fewer keywords
    ]
    
    for search_query in search_queries:
        if not search_query or len(search_query) < 3:
            continue
            
        url = f"https://gnews.io/api/v4/search"
        params = {
            "q": search_query,
            "lang": "en",
            "max": 15,
            "token": GNEWS_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=20)
            print(f"GNews Status Code: {response.status_code}")
            print(f"GNews Search Query: '{search_query}'")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                print(f"GNews found {len(articles)} articles with query: '{search_query}'")
                if articles:  # Return first successful result
                    return {"error": None, "articles": articles}
            elif response.status_code == 400:
                print(f"GNews 400 Error with query '{search_query}': {response.text}")
                continue  # Try next query
            elif response.status_code == 429:
                return {"error": "Rate limit exceeded - please try again later", "articles": []}
            elif response.status_code == 401:
                return {"error": "Invalid API key", "articles": []}
            else:
                print(f"GNews Error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            return {"error": "Request timed out - API may be slow", "articles": []}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection failed - API may be down", "articles": []}
        except Exception as e:
            print(f"GNews Exception with query '{search_query}': {e}")
            continue
    
    return {"error": None, "articles": []}

def search_factcheck(query):
    """Search Google Fact Check API for claims matching the query"""
    if not FACTCHECK_KEY:
        return {"error": "API key not configured", "claims": []}
    
    # Try multiple search strategies
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 6),  # Then keywords
        extract_keywords(query, 3)   # Fallback with fewer keywords
    ]
    
    for search_query in search_queries:
        if not search_query:
            continue
            
        # Clean query for FactCheck API
        clean_query = search_query.replace("'", "").replace('"', '')
        encoded_query = urllib.parse.quote(clean_query)
        
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {
            "query": encoded_query,
            "key": FACTCHECK_KEY,
            "languageCode": "en"
        }
        
        try:
            response = requests.get(url, params=params, timeout=20)
            print(f"FactCheck Status Code: {response.status_code}")
            print(f"FactCheck Search Query: '{clean_query}'")
            
            if response.status_code == 200:
                data = response.json()
                claims = data.get("claims", [])
                print(f"FactCheck found {len(claims)} claims with query: '{clean_query}'")
                if claims:  # Return first successful result
                    return {"error": None, "claims": claims}
            elif response.status_code == 429:
                return {"error": "Rate limit exceeded - please try again later", "claims": []}
            elif response.status_code == 401:
                return {"error": "Invalid API key", "claims": []}
            else:
                print(f"FactCheck API Error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            return {"error": "Request timed out - API may be slow", "claims": []}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection failed - API may be down", "claims": []}
        except Exception as e:
            print(f"FactCheck API Exception with query '{clean_query}': {e}")
            continue
    
    return {"error": None, "claims": []}

def search_mediastack(query):
    """Search MediaStack API for news articles (Free tier: 500 requests/month)"""
    if not MEDIASTACK_KEY:
        return {"error": "API key not configured", "articles": []}
    
    # Try multiple search strategies
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 6),  # Then keywords
        extract_keywords(query, 3)   # Fallback with fewer keywords
    ]
    
    for search_query in search_queries:
        if not search_query:
            continue
            
        url = "http://api.mediastack.com/v1/news"
        params = {
            "access_key": MEDIASTACK_KEY,
            "keywords": search_query,
            "languages": "en",
            "limit": 15
        }
        
        try:
            response = requests.get(url, params=params, timeout=25)
            print(f"MediaStack Status Code: {response.status_code}")
            print(f"MediaStack Search Query: '{search_query}'")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("data", [])
                print(f"MediaStack found {len(articles)} articles with query: '{search_query}'")
                if articles:  # Return first successful result
                    return {"error": None, "articles": articles}
            elif response.status_code == 429:
                return {"error": "Rate limit exceeded - free quota exhausted", "articles": []}
            elif response.status_code == 401:
                return {"error": "Invalid API key", "articles": []}
            else:
                print(f"MediaStack Error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            return {"error": "Request timed out - API may be slow", "articles": []}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection failed - API may be down", "articles": []}
        except Exception as e:
            print(f"MediaStack Exception with query '{search_query}': {e}")
            continue
    
    return {"error": None, "articles": []}

def search_newsdata_io(query):
    """Search NewsData.io API (Free tier: 200 requests/day)"""
    if not NEWSDATA_KEY:
        return {"error": "API key not configured", "articles": []}
    
    # Try multiple search strategies
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 6),  # Then keywords
        extract_keywords(query, 3)   # Fallback with fewer keywords
    ]
    
    for search_query in search_queries:
        if not search_query:
            continue
            
        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": NEWSDATA_KEY,
            "q": search_query,
            "language": "en",
            "size": 10
        }
        
        try:
            response = requests.get(url, params=params, timeout=20)
            print(f"NewsData Status Code: {response.status_code}")
            print(f"NewsData Search Query: '{search_query}'")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("results", [])
                print(f"NewsData found {len(articles)} articles with query: '{search_query}'")
                if articles:  # Return first successful result
                    return {"error": None, "articles": articles}
            elif response.status_code == 429:
                return {"error": "Rate limit exceeded - daily quota exhausted", "articles": []}
            elif response.status_code == 401:
                return {"error": "Invalid API key", "articles": []}
            else:
                print(f"NewsData Error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            return {"error": "Request timed out - API may be slow", "articles": []}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection failed - API may be down", "articles": []}
        except Exception as e:
            print(f"NewsData Exception with query '{search_query}': {e}")
            continue
    
    return {"error": None, "articles": []}

def search_currents_api(query):
    """Search Currents API with strict 6-second TOTAL timeout (Free tier: 600 requests/month)"""
    if not CURRENTS_KEY:
        return {"error": "API key not configured", "articles": []}
    
    # Start timing for TOTAL 6-second limit
    start_time = time.time()
    
    # Try multiple search strategies but with strict time limit
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 6),  # Then keywords
        extract_keywords(query, 3)   # Fallback with fewer keywords
    ]
    
    for i, search_query in enumerate(search_queries):
        # Check if we've exceeded 6 seconds total
        elapsed_time = time.time() - start_time
        if elapsed_time >= 6:
            return {"error": "Request timed out - API took too long (6s limit)", "articles": []}
        
        if not search_query:
            continue
        
        # Calculate remaining time for this request (minimum 1 second)
        remaining_time = max(1, 6 - elapsed_time)
        # For later queries, use even shorter timeout to stay within limit
        if i > 0:
            remaining_time = min(remaining_time, 2)
            
        url = "https://api.currentsapi.services/v1/search"
        params = {
            "apiKey": CURRENTS_KEY,
            "keywords": search_query,
            "language": "en"
        }
        
        try:
            response = requests.get(url, params=params, timeout=remaining_time)
            print(f"Currents Status Code: {response.status_code}")
            print(f"Currents Search Query: '{search_query}' (timeout: {remaining_time}s)")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("news", [])
                print(f"Currents found {len(articles)} articles with query: '{search_query}'")
                if articles:  # Return first successful result
                    return {"error": None, "articles": articles}
            elif response.status_code == 429:
                return {"error": "Rate limit exceeded - monthly quota exhausted", "articles": []}
            elif response.status_code == 401:
                return {"error": "Invalid API key", "articles": []}
            else:
                print(f"Currents Error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            print(f"Currents timeout after {remaining_time}s with query '{search_query}'")
            # Continue to next query if we still have time
            if time.time() - start_time < 5.5:  # Leave some buffer
                continue
            else:
                return {"error": "Request timed out - API took too long (6s limit)", "articles": []}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection failed - API may be down", "articles": []}
        except Exception as e:
            print(f"Currents Exception with query '{search_query}': {e}")
            continue
        
        # Final time check after successful request
        if time.time() - start_time >= 6:
            return {"error": "Request timed out - API took too long (6s limit)", "articles": []}
    
    return {"error": None, "articles": []}

def search_rapidapi_news(query):
    """Search RapidAPI News with strict 6-second TOTAL timeout"""
    if not RAPIDAPI_KEY:
        return {"error": "API key not configured", "articles": []}
    
    # Start timing for TOTAL 6-second limit
    start_time = time.time()
    
    # Try multiple search strategies but with strict time limit
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 6),  # Then keywords
        extract_keywords(query, 3)   # Fallback with fewer keywords
    ]
    
    for i, search_query in enumerate(search_queries):
        # Check if we've exceeded 6 seconds total
        elapsed_time = time.time() - start_time
        if elapsed_time >= 6:
            return {"error": "Request timed out - API took too long (6s limit)", "articles": []}
        
        if not search_query:
            continue
        
        # Calculate remaining time for this request (minimum 1 second)
        remaining_time = max(1, 6 - elapsed_time)
        # For later queries, use even shorter timeout to stay within limit
        if i > 0:
            remaining_time = min(remaining_time, 2)
            
        # Using a popular news API endpoint from RapidAPI
        url = "https://newsapi-v2.p.rapidapi.com/everything"
        
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "newsapi-v2.p.rapidapi.com"
        }
        
        params = {
            "q": search_query,
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 15
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=remaining_time)
            print(f"RapidAPI Status Code: {response.status_code}")
            print(f"RapidAPI Search Query: '{search_query}' (timeout: {remaining_time}s)")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                print(f"RapidAPI found {len(articles)} articles with query: '{search_query}'")
                if articles:  # Return first successful result
                    return {"error": None, "articles": articles}
            elif response.status_code == 429:
                return {"error": "Rate limit exceeded - quota exhausted", "articles": []}
            elif response.status_code == 401:
                return {"error": "Invalid API key", "articles": []}
            elif response.status_code == 403:
                return {"error": "Access forbidden - check subscription", "articles": []}
            else:
                print(f"RapidAPI Error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            print(f"RapidAPI timeout after {remaining_time}s with query '{search_query}'")
            # Continue to next query if we still have time
            if time.time() - start_time < 5.5:  # Leave some buffer
                continue
            else:
                return {"error": "Request timed out - API took too long (6s limit)", "articles": []}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection failed - API may be down", "articles": []}
        except Exception as e:
            print(f"RapidAPI Exception with query '{search_query}': {e}")
            continue
        
        # Final time check after successful request
        if time.time() - start_time >= 6:
            return {"error": "Request timed out - API took too long (6s limit)", "articles": []}
    
    return {"error": None, "articles": []}