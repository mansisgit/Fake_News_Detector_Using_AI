## 🔧 How to Add Your API Keys on Streamlit Cloud (For Deployment)

If you're planning to **deploy this project on [Streamlit Cloud](https://streamlit.io/cloud)**, here's how to securely add your API keys so your deployed app works correctly.

---

### ✅ Step-by-Step Instructions

1. Go to your [Streamlit Cloud dashboard](https://streamlit.io/cloud) and log in.
2. Click on **“New app”** and select this repository (after you've forked or uploaded it to your GitHub).
3. Before deploying, scroll down and open the **“Advanced settings”**.
4. Click on **“Secrets”**.
5. In the **Secrets editor**, paste the following:

    ```toml
    NEWSAPI_KEY = "your_newsapi_key"
    GNEWS_KEY = "your_gnews_key"
    FACTCHECK_KEY = "your_google_factcheck_key"
    MEDIASTACK_KEY = "your_mediastack_key"
    NEWSDATA_KEY = "your_newsdata_key"
    CURRENTS_KEY = "your_currentsapi_key"
    ```

    > 🔐 **Note:** Make sure to wrap all values in **quotes** and replace the dummy values with your actual API keys.

6. Click **Save**.
7. Deploy your app!

---

### 🧠 Notes

- These secrets are securely stored and are **not visible** in your public GitHub repository.
- You do **not** need a `.env` file in your code when using Streamlit secrets — it automatically injects them at runtime.
- You can access them directly in your code using `st.secrets`:

    ```python
    import streamlit as st

    news_api_key = st.secrets["NEWSAPI_KEY"]
    gnews_key = st.secrets["GNEWS_KEY"]
    # ...and so on
    ```

---