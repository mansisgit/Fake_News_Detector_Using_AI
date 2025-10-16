@echo off
title 📰 Fake News Detector - Streamlit App
echo Setting up Python path...
set PYTHONPATH=.
echo Starting Streamlit app...
python -m streamlit run api_integrated_app\api_integrated_app.py
pause
