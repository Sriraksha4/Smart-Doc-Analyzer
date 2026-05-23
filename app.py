#streamlit run app.py
import os
import re
import ast
import html
import json
import hashlib
from datetime import datetime

import numpy as np
import streamlit as st
import pypdf


# =============================================================================
# Page config
# =============================================================================
st.set_page_config(
    page_title="Lumina — AI Document Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# Beautiful Elegant UI — Soft Luxury Aesthetic
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --bg: #0d0f14;
  --bg2: #13161d;
  --bg3: #181c26;
  --surface: #1e2330;
  --surface2: #252b3b;
  --border: rgba(139,120,255,0.15);
  --border2: rgba(139,120,255,0.3);
  --primary: #8b78ff;
  --primary-glow: rgba(139,120,255,0.25);
  --gold: #f0c060;
  --gold-soft: rgba(240,192,96,0.15);
  --teal: #5ce6d4;
  --text: #e8e4f4;
  --text-muted: #8b87a8;
  --text-dim: #555270;
  --success: #5cdb95;
  --danger: #ff6b8a;
  --radius: 12px;
  --radius-lg: 20px;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}

#MainMenu, footer { visibility: hidden; }

.stApp {
  background: var(--bg) !important;
}

.stApp::before {
  content: "";
  position: fixed;
  top: -40%;
  left: -20%;
  width: 60%;
  height: 80%;
  background: radial-gradient(ellipse, rgba(139,120,255,0.06) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

.stApp::after {
  content: "";
  position: fixed;
  bottom: -30%;
  right: -15%;
  width: 50%;
  height: 70%;
  background: radial-gradient(ellipse, rgba(92,230,212,0.05) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
  font-family: 'DM Sans', sans-serif !important;
}

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSidebar"] .stTextInput input {
  background: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 14px !important;
  padding: 0.7rem 1rem !important;
  transition: all 0.2s !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px var(--primary-glow) !important;
  outline: none !important;
}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
  color: var(--text-dim) !important;
}

/* Buttons */
.stButton > button {
  background: linear-gradient(135deg, var(--primary), #6b55ff) !important;
  color: white !important;
  border: none !important;
  border-radius: var(--radius) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  padding: 0.65rem 1.5rem !important;
  transition: all 0.25s !important;
  letter-spacing: 0.02em !important;
}

.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 24px var(--primary-glow) !important;
  filter: brightness(1.1) !important;
}

.stButton > button:active {
  transform: translateY(0) !important;
}

[data-testid="stFormSubmitButton"] button {
  background: linear-gradient(135deg, var(--primary), #6b55ff) !important;
  color: white !important;
  border: none !important;
  border-radius: var(--radius) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  padding: 0.7rem 1.5rem !important;
  width: 100% !important;
  transition: all 0.25s !important;
}

[data-testid="stFormSubmitButton"] button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 24px var(--primary-glow) !important;
}

[data-testid="stDownloadButton"] button {
  background: transparent !important;
  color: var(--primary) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  transition: all 0.2s !important;
}

[data-testid="stDownloadButton"] button:hover {
  background: var(--primary-glow) !important;
  border-color: var(--primary) !important;
}

/* Sidebar upload button */
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
  background: var(--surface) !important;
  border: 1px dashed var(--border2) !important;
  border-radius: var(--radius) !important;
  padding: 1.2rem !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
  background: transparent !important;
  color: var(--primary) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius) !important;
  font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  color: var(--danger) !important;
  border: 1px solid rgba(255,107,138,0.3) !important;
  font-size: 13px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255,107,138,0.1) !important;
  box-shadow: none !important;
  transform: none !important;
}

[data-testid="stSelectbox"] > div > div {
  background: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius) !important;
}

[data-testid="stExpander"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}

[data-testid="stExpander"] summary {
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
}

[data-testid="stForm"] {
  background: transparent !important;
  border: none !important;
}

.stSpinner > div {
  border-top-color: var(--primary) !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

/* ===================== CUSTOM COMPONENTS ===================== */

.auth-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.auth-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 3rem 2.5rem;
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
  box-shadow: 0 24px 80px rgba(0,0,0,0.4), 0 0 0 1px rgba(139,120,255,0.08);
  animation: fadeSlideUp 0.5s ease forwards;
}

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.auth-logo {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-logo-mark {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, var(--primary), #5ce6d4);
  border-radius: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  margin: 0 auto 1rem;
  box-shadow: 0 8px 32px var(--primary-glow);
}

.auth-title {
  font-family: 'Playfair Display', serif !important;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text);
  text-align: center;
  margin-bottom: 0.35rem;
}

.auth-sub {
  font-size: 14px;
  color: var(--text-muted);
  text-align: center;
  margin-bottom: 0;
}

.auth-divider {
  height: 1px;
  background: var(--border);
  margin: 1.5rem 0;
}

.auth-link {
  text-align: center;
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 1.25rem;
}

.auth-link a {
  color: var(--primary) !important;
  text-decoration: none;
  font-weight: 500;
}

.auth-error {
  background: rgba(255,107,138,0.1);
  border: 1px solid rgba(255,107,138,0.3);
  border-radius: var(--radius);
  padding: 0.75rem 1rem;
  color: var(--danger);
  font-size: 13px;
  margin-bottom: 1rem;
  text-align: center;
}

.auth-success {
  background: rgba(92,219,149,0.1);
  border: 1px solid rgba(92,219,149,0.3);
  border-radius: var(--radius);
  padding: 0.75rem 1rem;
  color: var(--success);
  font-size: 13px;
  margin-bottom: 1rem;
  text-align: center;
}

/* SIDEBAR */
.sidebar-logo {
  padding: 1.25rem 1rem 1rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1rem;
}

.sidebar-logo-name {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  letter-spacing: 0.02em;
}

.sidebar-logo-tag {
  font-size: 11px;
  color: var(--primary);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-top: 0.2rem;
}

.sidebar-section {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-dim);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin: 1.25rem 0 0.6rem;
}

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  margin-bottom: 1rem;
}

.sidebar-avatar {
  width: 34px;
  height: 34px;
  background: linear-gradient(135deg, var(--primary), var(--teal));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.sidebar-username {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}

.sidebar-role {
  font-size: 11px;
  color: var(--text-muted);
}

.doc-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 0.5rem;
  transition: border-color 0.2s;
}

.doc-card:hover { border-color: var(--border2); }

.doc-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, rgba(139,120,255,0.2), rgba(92,230,212,0.1));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.doc-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.doc-meta {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 0.15rem;
}

.doc-badge {
  background: var(--primary-glow);
  color: var(--primary);
  border-radius: 6px;
  padding: 0.15rem 0.45rem;
  font-size: 10px;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
  margin: 0.75rem 0;
}

.stat-box {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.75rem 0.5rem;
  text-align: center;
}

.stat-val {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--primary);
}

.stat-label {
  font-size: 10px;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 0.2rem;
}

/* MAIN AREA */
.main-wrap {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem 8rem;
}

/* MODE TABS */
.mode-tabs {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.mode-tab {
  flex: 1;
  padding: 0.85rem 1.5rem;
  border-radius: var(--radius);
  border: 1px solid var(--border2);
  background: transparent;
  color: var(--text-muted);
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.mode-tab.active {
  background: linear-gradient(135deg, var(--primary), #6b55ff);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 16px var(--primary-glow);
}

/* HERO */
.hero-wrap {
  text-align: center;
  padding: 4rem 2rem 3rem;
  animation: fadeSlideUp 0.6s ease forwards;
}

.hero-badge {
  display: inline-block;
  background: var(--primary-glow);
  color: var(--primary);
  border: 1px solid var(--border2);
  border-radius: 100px;
  padding: 0.35rem 1rem;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 1.75rem;
  animation: pulse 2.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 var(--primary-glow); }
  50% { box-shadow: 0 0 0 6px transparent; }
}

.hero-title {
  font-family: 'Playfair Display', serif !important;
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  line-height: 1.15;
  color: var(--text);
  margin-bottom: 1.25rem;
}

.hero-title span {
  background: linear-gradient(135deg, var(--primary), var(--teal));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-sub {
  font-size: 16px;
  color: var(--text-muted);
  max-width: 520px;
  margin: 0 auto 2.5rem;
  line-height: 1.75;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1rem;
  text-align: left;
}

@media (max-width: 700px) { .steps-grid { grid-template-columns: 1fr; } }

.step-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  transition: all 0.25s;
  animation: fadeSlideUp 0.6s ease forwards;
}

.step-card:hover {
  border-color: var(--border2);
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.3);
}

.step-num {
  font-size: 11px;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 0.85rem;
}

.step-icon {
  font-size: 1.75rem;
  margin-bottom: 0.75rem;
}

.step-title {
  font-weight: 700;
  font-size: 15px;
  color: var(--text);
  margin-bottom: 0.4rem;
}

.step-desc {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.65;
}

/* PDF UPLOADED STATE */
.upload-success {
  background: linear-gradient(135deg, rgba(92,219,149,0.08), rgba(92,230,212,0.05));
  border: 1px solid rgba(92,219,149,0.25);
  border-radius: var(--radius-lg);
  padding: 1.5rem 1.75rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 1.5rem;
  animation: fadeSlideUp 0.4s ease forwards;
}

.upload-success-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.upload-success-title {
  font-weight: 700;
  font-size: 16px;
  color: var(--success);
  margin-bottom: 0.25rem;
}

.upload-success-sub {
  font-size: 13px;
  color: var(--text-muted);
}

/* SUMMARY CARD */
.summary-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  margin-bottom: 1.25rem;
}

.summary-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.summary-label::after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--border);
}

.summary-text {
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.8;
}

/* SUGGESTED QUESTIONS */
.section-header {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-muted);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin: 1.75rem 0 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.section-header::after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--border);
}

.suggest-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.65rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 600px) { .suggest-grid { grid-template-columns: 1fr; } }

/* CHAT */
.chat-area {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-top: 1rem;
}

.msg-user {
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  gap: 0.75rem;
  animation: fadeSlideUp 0.3s ease;
}

.msg-ai {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  animation: fadeSlideUp 0.3s ease;
}

.bubble-user {
  background: linear-gradient(135deg, var(--primary), #6b55ff);
  color: white;
  padding: 0.9rem 1.15rem;
  border-radius: 18px 18px 4px 18px;
  font-size: 14px;
  line-height: 1.7;
  max-width: 75%;
  box-shadow: 0 4px 16px var(--primary-glow);
}

.bubble-ai {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 0.9rem 1.15rem;
  border-radius: 18px 18px 18px 4px;
  font-size: 14px;
  line-height: 1.8;
  max-width: 80%;
}

.av-user {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--primary), var(--teal));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.av-ai {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--gold), #e08030);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.cite-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin-top: 0.65rem;
}

.cite-chip {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 0.25rem 0.7rem;
  font-size: 11px;
  color: var(--text-muted);
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.cite-chip span {
  color: var(--gold);
  font-weight: 600;
}

/* QUERY BOX */
[data-testid="stForm"] {
  background: var(--bg2) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius-lg) !important;
  padding: 1.25rem !important;
  margin-top: 1.5rem !important;
}

[data-testid="stForm"] [data-testid="stTextInput"] label,
[data-testid="stForm"] label {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  color: var(--primary) !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
}

/* QUIZ STYLES */
.quiz-header {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.25rem;
}

.quiz-header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.quiz-title-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.quiz-counter {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
}

.quiz-bar-bg {
  height: 4px;
  background: var(--surface2);
  border-radius: 100px;
  width: 100%;
  overflow: hidden;
}

.quiz-bar-fill {
  height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--teal));
  border-radius: 100px;
  transition: width 0.4s ease;
}

.quiz-question-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.75rem;
  margin-bottom: 1.25rem;
}

.quiz-q-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--gold);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 0.85rem;
}

.quiz-q-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  line-height: 1.65;
}

.quiz-opt {
  display: block;
  width: 100%;
  text-align: left;
  padding: 0.85rem 1.15rem;
  margin-bottom: 0.55rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text-muted);
  font-size: 14px;
  font-family: 'DM Sans', sans-serif;
  cursor: pointer;
  transition: all 0.15s;
  line-height: 1.5;
}

.quiz-opt:hover { border-color: var(--primary); color: var(--text); }
.quiz-opt.correct { border-color: var(--success) !important; color: var(--success) !important; background: rgba(92,219,149,0.08) !important; }
.quiz-opt.wrong   { border-color: var(--danger)  !important; color: var(--danger)  !important; background: rgba(255,107,138,0.08) !important; }
.quiz-opt.neutral { opacity: 0.45; }

.quiz-explanation {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  margin-top: 0.85rem;
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.75;
}

.quiz-result-correct { color: var(--success); font-weight: 700; font-size: 13px; }
.quiz-result-wrong   { color: var(--danger);  font-weight: 700; font-size: 13px; }

.score-box {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 3rem 2rem;
  text-align: center;
  margin-bottom: 1.5rem;
}

.score-big {
  font-family: 'Playfair Display', serif;
  color: var(--primary);
  font-size: clamp(4rem, 12vw, 6rem);
  font-weight: 700;
  line-height: 1;
  margin: 0.5rem 0;
  text-shadow: 0 0 40px var(--primary-glow);
}

.score-sub { color: var(--text-muted); font-size: 15px; margin-top: 0.75rem; }
.score-grade { color: var(--gold); font-size: 12px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; }

.quiz-setup-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 2rem;
  margin-bottom: 1.25rem;
}

/* Floating orbs */
.orb {
  position: fixed;
  border-radius: 50%;
  pointer-events: none;
  z-index: -1;
  filter: blur(80px);
  animation: float 8s ease-in-out infinite;
}

.orb-1 {
  width: 400px; height: 400px;
  background: rgba(139,120,255,0.07);
  top: 10%; left: 5%;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px; height: 300px;
  background: rgba(92,230,212,0.05);
  bottom: 15%; right: 10%;
  animation-delay: -3s;
}

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-30px) scale(1.05); }
}

.step-card:nth-child(1) { animation-delay: 0.1s; }
.step-card:nth-child(2) { animation-delay: 0.2s; }
.step-card:nth-child(3) { animation-delay: 0.3s; }

</style>
""", unsafe_allow_html=True)


# =============================================================================
# Auth helpers
# =============================================================================

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def load_users() -> dict:
    if "users_db" not in st.session_state:
        st.session_state.users_db = {}
    return st.session_state.users_db

def register_user(name: str, email: str, pw: str) -> tuple:
    users = load_users()
    key = email.lower().strip()
    if not name.strip():
        return False, "Please enter your name."
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address."
    if len(pw) < 6:
        return False, "Password must be at least 6 characters."
    if key in users:
        return False, "An account with this email already exists."
    users[key] = {"name": name.strip(), "email": key, "pw": hash_pw(pw)}
    return True, "Account created! You can now log in."

def login_user(email: str, pw: str) -> tuple:
    users = load_users()
    key = email.lower().strip()
    if key not in users:
        return False, "No account found with this email. Please register first."
    if users[key]["pw"] != hash_pw(pw):
        return False, "Incorrect password. Please try again."
    return True, users[key]["name"]


# =============================================================================
# Logic helpers
# =============================================================================

@st.cache_resource(show_spinner=False)
def load_embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def safe(text: str) -> str:
    return html.escape("" if text is None else str(text))


def sanitize_llm_text(text: str) -> str:
    text = "" if text is None else str(text)
    text = text.replace("```", "")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def render_answer(text: str) -> str:
    return sanitize_llm_text(text)


def extract_pdf(file_obj, doc_name: str):
    file_obj.seek(0)
    reader = pypdf.PdfReader(file_obj)
    chunks = []
    full_text = ""
    chunk_size = 260
    overlap = 60

    for page_idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        full_text += page_text + "\n"
        words = page_text.split()
        start = 0
        while start < len(words):
            chunk_text = " ".join(words[start:start + chunk_size]).strip()
            if chunk_text:
                chunks.append({"text": chunk_text, "page": page_idx + 1, "doc": doc_name})
            start += max(1, chunk_size - overlap)

    meta = {
        "pages": len(reader.pages),
        "words": len(re.findall(r"\b[\w'-]+\b", re.sub(r"\s+", " ", full_text).strip())),
        "chunks": len(chunks),
        "full_text": full_text[:5000],
    }
    return chunks, meta


def embed_chunks(chunks):
    model = load_embedder()
    texts = [c["text"] for c in chunks]
    if not texts:
        return np.empty((0, 384))
    return model.encode(texts, show_progress_bar=False, batch_size=32)


def semantic_search(query, all_chunks, all_embeddings, k=5, doc_filter=None):
    from sklearn.metrics.pairwise import cosine_similarity
    if all_embeddings is None or len(all_chunks) == 0:
        return []
    model = load_embedder()
    q_emb = model.encode([query])
    if doc_filter:
        indices = [i for i, c in enumerate(all_chunks) if c["doc"] in doc_filter]
    else:
        indices = list(range(len(all_chunks)))
    if not indices:
        return []
    filtered_embs = all_embeddings[indices]
    scores = cosine_similarity(q_emb, filtered_embs)[0]
    top_local = np.argsort(scores)[::-1][:k]
    results = []
    for local_idx in top_local:
        global_idx = indices[local_idx]
        results.append({
            "text": all_chunks[global_idx]["text"],
            "page": all_chunks[global_idx]["page"],
            "doc": all_chunks[global_idx]["doc"],
            "score": float(scores[local_idx]),
        })
    return results


def _build_messages(system, user_msg, history):
    messages = [{"role": "system", "content": system}]
    for turn in history[-4:]:
        messages.append({"role": "user", "content": sanitize_llm_text(turn["q"])})
        messages.append({"role": "assistant", "content": sanitize_llm_text(turn["a"])})
    messages.append({"role": "user", "content": user_msg})
    return messages


def call_groq(api_key, system, user_msg, history):
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=_build_messages(system, user_msg, history),
            max_tokens=1024,
            temperature=0.3,
        )
        return sanitize_llm_text(response.choices[0].message.content.strip())
    except Exception as e:
        err = str(e)
        if "429" in err:
            return "⚠️ Rate limit reached. Please wait a moment and try again."
        if "401" in err or "invalid" in err.lower():
            return "⚠️ Invalid API key. Please check the key in the sidebar."
        return f"⚠️ Error: {err}"


def call_llm(system, user_msg, history):
    return call_groq(st.session_state.groq_key, system, user_msg, history)


def get_answer(results, question, history):
    context_parts = []
    for r in results:
        score_pct = int(r["score"] * 100)
        context_parts.append(f"[Source: {r['doc']} | Page {r['page']} | Relevance: {score_pct}%]\n{r['text']}")
    context = "\n\n---\n\n".join(context_parts) if context_parts else "NO_CONTEXT_FOUND"
    system = (
        "You are Lumina, a precise document assistant.\n"
        "Rules:\n"
        "- Use ONLY the provided CONTEXT to answer. Do NOT use external knowledge.\n"
        "- If the answer can be found verbatim or inferred from the context, give a short, factual answer.\n"
        "- If you infer, state it briefly as an inference.\n"
        "- If the answer cannot be found, respond: 'Answer not found in the document.'\n"
        "- Do not output HTML, tags, or code blocks.\n"
        "- Be concise and clear."
    )
    user_msg = (
        f"RETRIEVED CONTEXT:\n{context}\n\n"
        f"QUESTION:\n{question}\n\n"
        "Answer briefly, citing sources from the context."
    )
    return call_llm(system, user_msg, history)


def get_summary(full_text):
    system = "You are a document analyst. Be structured, concise, and factual."
    user_msg = (
        "Provide a structured document summary with these sections:\n"
        "Main Topic:\nKey Points:\nImportant Data/Facts:\nConclusion:\n\n"
        f"Document:\n{full_text[:4500]}"
    )
    return call_llm(system, user_msg, [])


def get_suggestions(full_text):
    system = "Output ONLY a Python list of 4 strings. No markdown, no explanation."
    user_msg = (
        'Generate 4 insightful questions for this document.\n'
        'Format exactly like: ["Q1?","Q2?","Q3?","Q4?"]\n\n'
        f"{full_text[:2500]}"
    )
    raw = call_llm(system, user_msg, [])
    try:
        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if match:
            qs = ast.literal_eval(match.group())
            if isinstance(qs, list) and len(qs) >= 4:
                return qs[:4]
    except Exception:
        pass
    return [
        "What is the main topic of this document?",
        "What are the key findings or conclusions?",
        "What data or evidence is presented?",
        "What are the recommendations or next steps?",
    ]


def generate_quiz(doc_texts: str, n: int = 5):
    system = (
        "Generate multiple-choice quiz questions from this document. "
        "Output ONLY a valid Python list of dicts with these exact keys: "
        "q (question string), options (list of exactly 4 strings), "
        "answer (int 0-3 = index of correct option), explanation (1-2 sentence string). "
        "Example: [{\"q\": \"What is X?\", \"options\": [\"A\",\"B\",\"C\",\"D\"], "
        "\"answer\": 2, \"explanation\": \"Because...\"}, ...]. "
        "No markdown, no preamble. Questions must be answerable from the document only."
    )
    user_msg = f"Generate exactly {n} MCQ questions from this document:\n\n{doc_texts[:5000]}"
    raw = call_llm(system, user_msg, [])
    try:
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            items = ast.literal_eval(match.group())
            if isinstance(items, list):
                valid = [
                    item for item in items
                    if (item.get("q")
                        and isinstance(item.get("options"), list)
                        and len(item["options"]) == 4
                        and isinstance(item.get("answer"), int)
                        and 0 <= item["answer"] <= 3)
                ]
                if valid:
                    return valid
    except Exception:
        pass
    return [{
        "q": "Quiz generation failed. Please try again.",
        "options": ["Try again", "Reload PDF", "Check API key", "Restart app"],
        "answer": 0,
        "explanation": "The model could not generate quiz questions. Ensure your API key is valid.",
    }]


def build_export(history, doc_names):
    lines = [
        "LUMINA AI — CHAT EXPORT",
        "=" * 60,
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Documents: {', '.join(doc_names) if doc_names else 'None'}",
        "=" * 60,
        "",
    ]
    for i, turn in enumerate(history, 1):
        lines.append(f"Q{i}: {turn['q']}")
        lines.append(f"A{i}: {turn['a']}")
        if turn.get("citations"):
            cites = ", ".join(
                f"p.{c['page']} in '{c['doc']}' ({int(c['score']*100)}%)"
                for c in turn["citations"]
            )
            lines.append(f"Sources: {cites}")
        lines.append("")
    return "\n".join(lines)


def active_key_ok():
    return bool(st.session_state.groq_key)


def reset_app():
    st.session_state.history = []
    st.session_state.all_chunks = []
    st.session_state.all_embeddings = None
    st.session_state.docs = {}
    st.session_state.summaries = {}
    st.session_state.suggestions = []
    st.session_state.prefill = ""
    st.session_state.doc_filter = None
    reset_quiz()
    st.rerun()


def reset_quiz():
    st.session_state.quiz_items = []
    st.session_state.quiz_index = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_done = False
    st.session_state.quiz_generated = False
    st.session_state.quiz_answered = False
    st.session_state.quiz_chosen = -1


# =============================================================================
# Session state
# =============================================================================
defaults = {
    "mode": "chat",
    "quiz_items": [],
    "quiz_index": 0,
    "quiz_score": 0,
    "quiz_done": False,
    "quiz_generated": False,
    "quiz_answered": False,
    "quiz_chosen": -1,
    "quiz_n": 5,
    "history": [],
    "all_chunks": [],
    "all_embeddings": None,
    "docs": {},
    "summaries": {},
    "suggestions": [],
    "prefill": "",
    "doc_filter": None,
    "groq_key": os.environ.get("GROQ_API_KEY", ""),
    # Auth
    "logged_in": False,
    "current_user": None,
    "current_user_email": None,
    "auth_page": "login",
    "auth_msg": None,
    "auth_msg_type": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =============================================================================
# AUTH PAGES
# =============================================================================

if not st.session_state.logged_in:

    st.markdown('<div class="orb orb-1"></div><div class="orb orb-2"></div>', unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="auth-logo">
          <div class="auth-logo-mark">✦</div>
          <div class="auth-title">Lumina AI</div>
          <div class="auth-sub">Document Intelligence, Reimagined</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.auth_msg:
            if st.session_state.auth_msg_type == "error":
                st.markdown(f'<div class="auth-error">⚠ {safe(st.session_state.auth_msg)}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="auth-success">✓ {safe(st.session_state.auth_msg)}</div>', unsafe_allow_html=True)

        st.markdown('<div class="auth-divider"></div>', unsafe_allow_html=True)

        if st.session_state.auth_page == "login":
            st.markdown('<div style="font-size:14px;font-weight:600;color:var(--text);margin-bottom:0.5rem;">Sign in to your account</div>', unsafe_allow_html=True)

            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email address", placeholder="you@example.com", key="li_email")
                password = st.text_input("Password", placeholder="••••••••", type="password", key="li_pw")
                submitted = st.form_submit_button("Sign In →", use_container_width=True)

            if submitted:
                ok, result = login_user(email, password)
                if ok:
                    st.session_state.logged_in = True
                    st.session_state.current_user = result
                    st.session_state.current_user_email = email.lower().strip()
                    st.session_state.auth_msg = None
                    st.rerun()
                else:
                    st.session_state.auth_msg = result
                    st.session_state.auth_msg_type = "error"
                    st.rerun()

            st.markdown('<div class="auth-link">Don\'t have an account?</div>', unsafe_allow_html=True)

            if st.button("Create an account →", use_container_width=True, key="go_register"):
                st.session_state.auth_page = "register"
                st.session_state.auth_msg = None
                st.rerun()

        else:
            st.markdown('<div style="font-size:14px;font-weight:600;color:var(--text);margin-bottom:0.5rem;">Create your account</div>', unsafe_allow_html=True)

            with st.form("register_form", clear_on_submit=False):
                name = st.text_input("Full name", placeholder="Jane Smith", key="reg_name")
                email = st.text_input("Email address", placeholder="you@example.com", key="reg_email")
                password = st.text_input("Password", placeholder="Min. 6 characters", type="password", key="reg_pw")
                submitted = st.form_submit_button("Create Account →", use_container_width=True)

            if submitted:
                ok, msg = register_user(name, email, password)
                if ok:
                    st.session_state.auth_page = "login"
                    st.session_state.auth_msg = msg
                    st.session_state.auth_msg_type = "success"
                else:
                    st.session_state.auth_msg = msg
                    st.session_state.auth_msg_type = "error"
                st.rerun()

            st.markdown('<div class="auth-link">Already have an account?</div>', unsafe_allow_html=True)

            if st.button("Sign in instead →", use_container_width=True, key="go_login"):
                st.session_state.auth_page = "login"
                st.session_state.auth_msg = None
                st.rerun()

    st.stop()


# =============================================================================
# MAIN APP (authenticated)
# =============================================================================

user_initial = st.session_state.current_user[0].upper() if st.session_state.current_user else "U"

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-logo">
      <div class="sidebar-logo-name">✦ Lumina AI</div>
      <div class="sidebar-logo-tag">Document Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-user">
      <div class="sidebar-avatar">{user_initial}</div>
      <div>
        <div class="sidebar-username">{safe(st.session_state.current_user)}</div>
        <div class="sidebar-role">{safe(st.session_state.current_user_email)}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">API Key</div>', unsafe_allow_html=True)
    groq_value = st.text_input(
        "Groq API Key",
        value=st.session_state.groq_key,
        placeholder="gsk_...",
        type="password",
        label_visibility="collapsed",
    )
    st.session_state.groq_key = groq_value

    st.markdown('<div class="sidebar-section">Documents</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload PDF(s)",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        if not active_key_ok():
            st.error("Add your Groq API key first.")
        else:
            new_docs_loaded = False
            for uploaded in uploaded_files:
                if uploaded.name in st.session_state.docs:
                    continue
                with st.spinner(f"Indexing {uploaded.name}..."):
                    new_chunks, meta = extract_pdf(uploaded, uploaded.name)
                    new_embs = embed_chunks(new_chunks)
                    st.session_state.all_chunks.extend(new_chunks)
                    if st.session_state.all_embeddings is None:
                        st.session_state.all_embeddings = new_embs
                    else:
                        st.session_state.all_embeddings = np.vstack([st.session_state.all_embeddings, new_embs])
                    st.session_state.docs[uploaded.name] = meta
                    st.session_state.summaries[uploaded.name] = get_summary(meta["full_text"])
                    st.session_state.suggestions = get_suggestions(meta["full_text"])
                    new_docs_loaded = True

            if new_docs_loaded:
                st.session_state.history = []
                st.session_state.prefill = ""
                reset_quiz()
                st.success("Documents indexed ✓")

    if st.session_state.docs:
        for doc_name, meta in st.session_state.docs.items():
            short_name = doc_name if len(doc_name) <= 26 else doc_name[:23] + "…"
            words_display = f"{meta['words']:,}" if meta["words"] < 10000 else f"{round(meta['words']/1000,1)}k"
            st.markdown(f"""
            <div class="doc-card">
              <div class="doc-icon">📄</div>
              <div style="flex:1;min-width:0">
                <div class="doc-name">{safe(short_name)}</div>
                <div class="doc-meta">{meta['pages']} pages · {words_display} words</div>
              </div>
              <div class="doc-badge">{meta['pages']}p</div>
            </div>
            """, unsafe_allow_html=True)

        total_pages = sum(m["pages"] for m in st.session_state.docs.values())
        total_words = sum(m["words"] for m in st.session_state.docs.values())

        st.markdown(f"""
        <div class="stats-row">
          <div class="stat-box"><div class="stat-val">{len(st.session_state.docs)}</div><div class="stat-label">Docs</div></div>
          <div class="stat-box"><div class="stat-val">{total_pages}</div><div class="stat-label">Pages</div></div>
          <div class="stat-box"><div class="stat-val">{round(total_words/1000,1) if total_words>=1000 else total_words}k</div><div class="stat-label">Words</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        doc_names = list(st.session_state.docs.keys())
        focus_options = ["All documents"] + doc_names
        current_focus = "All documents"
        if st.session_state.doc_filter:
            current_focus = st.session_state.doc_filter[0] if st.session_state.doc_filter[0] in doc_names else "All documents"
        chosen_focus = st.selectbox("Focus", focus_options, index=focus_options.index(current_focus), label_visibility="visible")
        st.session_state.doc_filter = None if chosen_focus == "All documents" else [chosen_focus]

        if st.button("Clear All Documents", use_container_width=True):
            reset_app()

    st.markdown("---")
    if st.button("Sign Out", use_container_width=True, key="sign_out"):
        for k in ["logged_in", "current_user", "current_user_email", "history", "all_chunks",
                  "all_embeddings", "docs", "summaries", "suggestions", "prefill", "doc_filter"]:
            st.session_state[k] = defaults.get(k)
        st.session_state.auth_page = "login"
        st.session_state.auth_msg = None
        st.rerun()


# ---- MAIN CONTENT ----
st.markdown('<div class="orb orb-1"></div><div class="orb orb-2"></div>', unsafe_allow_html=True)
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

if not st.session_state.docs:
    # ---- LANDING ----
    st.markdown(f"""
    <div class="hero-wrap">
      <div class="hero-badge">✦ AI-Powered RAG</div>
      <div class="hero-title">
        Welcome back, {safe(st.session_state.current_user.split()[0])}.<br>
        <span>Understand any document</span><br>instantly.
      </div>
      <div class="hero-sub">
        Upload a PDF in the sidebar and ask questions in plain English.
        Lumina finds the answers with semantic search and page citations.
      </div>
    </div>
    <div class="steps-grid">
      <div class="step-card">
        <div class="step-num">Step 01</div>
        <div class="step-icon">📂</div>
        <div class="step-title">Upload your PDF</div>
        <div class="step-desc">Drop any document into the sidebar. Multiple PDFs supported simultaneously.</div>
      </div>
      <div class="step-card">
        <div class="step-num">Step 02</div>
        <div class="step-icon">🧠</div>
        <div class="step-title">AI indexes it</div>
        <div class="step-desc">Chunks are embedded using sentence transformers for meaning-based retrieval.</div>
      </div>
      <div class="step-card">
        <div class="step-num">Step 03</div>
        <div class="step-icon">💬</div>
        <div class="step-title">Chat or Quiz</div>
        <div class="step-desc">Get grounded answers with exact page citations, or test your knowledge with a quiz.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # ---- DOCUMENTS LOADED ----

    # Upload success banner
    doc_count = len(st.session_state.docs)
    total_pg = sum(m["pages"] for m in st.session_state.docs.values())
    st.markdown(f"""
    <div class="upload-success">
      <div class="upload-success-icon">✅</div>
      <div>
        <div class="upload-success-title">{doc_count} document{'s' if doc_count > 1 else ''} ready</div>
        <div class="upload-success-sub">{total_pg} pages indexed · Semantic search enabled · Choose Chat or Quiz below</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- MODE TABS (Chat / Quiz) ----
    tab_col1, tab_col2 = st.columns(2)
    with tab_col1:
        chat_active = "active" if st.session_state.mode == "chat" else ""
        if st.button("💬 Chat", use_container_width=True, key="tab_chat"):
            st.session_state.mode = "chat"
            st.rerun()
    with tab_col2:
        quiz_active = "active" if st.session_state.mode == "quiz" else ""
        if st.button("📝 Quiz", use_container_width=True, key="tab_quiz"):
            st.session_state.mode = "quiz"
            if not st.session_state.quiz_generated:
                reset_quiz()
            st.rerun()

    st.markdown("---")

    # ======================================================================
    # CHAT MODE
    # ======================================================================
    if st.session_state.mode == "chat":

        # Summaries
        for doc_name, summary in st.session_state.summaries.items():
            short = doc_name if len(doc_name) <= 40 else doc_name[:37] + "…"
            with st.expander(f"📋 Auto Summary — {short}", expanded=False):
                st.markdown(f"""
                <div class="summary-card" style="margin:0;border:none;background:transparent;padding:0;">
                  <div class="summary-label">Document Summary</div>
                  <div class="summary-text">{render_answer(summary)}</div>
                </div>
                """, unsafe_allow_html=True)

        # Suggested questions
        if not st.session_state.history and st.session_state.suggestions:
            st.markdown('<div class="section-header">✦ Suggested Questions</div>', unsafe_allow_html=True)
            st.markdown('<div class="suggest-grid">', unsafe_allow_html=True)
            cols = st.columns(2)
            for i, q in enumerate(st.session_state.suggestions):
                with cols[i % 2]:
                    if st.button(f"💡 {q}", key=f"suggest_{i}", use_container_width=True):
                        st.session_state.prefill = q
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Conversation
        if st.session_state.history:
            st.markdown('<div class="section-header">💬 Conversation</div>', unsafe_allow_html=True)
            st.markdown('<div class="chat-area">', unsafe_allow_html=True)

            for turn in st.session_state.history:
                st.markdown(f"""
                <div class="msg-user">
                  <div class="bubble-user">{safe(turn['q'])}</div>
                  <div class="av-user">{user_initial}</div>
                </div>
                """, unsafe_allow_html=True)

                answer_text = render_answer(turn['a'])
                citations_html = ""
                if turn.get("citations"):
                    chips = ""
                    for c in turn["citations"]:
                        score_pct = int(c["score"] * 100)
                        short_doc = c["doc"] if len(c["doc"]) <= 18 else c["doc"][:15] + "…"
                        chips += f'<div class="cite-chip">📄 {safe(short_doc)} · p.{c["page"]} · <span>{score_pct}%</span></div>'
                    citations_html = f'<div class="cite-row">{chips}</div>'

                st.markdown(f"""
                <div class="msg-ai">
                  <div class="av-ai">✦</div>
                  <div>
                    <div class="bubble-ai">{answer_text}{citations_html}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # Export
        if st.session_state.history:
            export_text = build_export(st.session_state.history, list(st.session_state.docs.keys()))
            st.download_button(
                "⬇ Export Conversation",
                data=export_text,
                file_name=f"lumina_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
            )

        # Query box
        with st.form("query_form", clear_on_submit=True):
            prompt = st.text_input(
                "✦ Ask a question",
                value=st.session_state.prefill,
                placeholder="What would you like to know about your document?",
            )
            submitted = st.form_submit_button("Send →", use_container_width=True)

        if submitted:
            question = prompt.strip()
            if not question:
                st.warning("Please type a question first.")
            elif not active_key_ok():
                st.error("Please add your Groq API key in the sidebar to start querying.")
            else:
                with st.spinner("Searching and generating answer…"):
                    results = semantic_search(
                        question,
                        st.session_state.all_chunks,
                        st.session_state.all_embeddings,
                        k=5,
                        doc_filter=st.session_state.doc_filter,
                    )
                    answer = get_answer(results, question, st.session_state.history)

                st.session_state.history.append({"q": question, "a": answer, "citations": results})
                st.session_state.prefill = ""
                st.rerun()

    # ======================================================================
    # QUIZ MODE
    # ======================================================================
    elif st.session_state.mode == "quiz":

        if not active_key_ok():
            st.error("Add your Groq API key in the sidebar to use Quiz mode.")

        # ── Setup screen ──────────────────────────────────────────────────
        elif not st.session_state.quiz_generated:
            st.markdown("""
            <div class="quiz-setup-card">
              <div class="summary-label">Quiz Mode</div>
              <div class="summary-text">
                Lumina will generate multiple-choice questions directly from your loaded document(s).
                Choose how many questions you want, then hit Generate to start.
                Each question shows the correct answer and an explanation after you respond.
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-header">✦ Number of Questions</div>', unsafe_allow_html=True)
            quiz_n = st.number_input(
                "n_questions", min_value=3, max_value=20,
                value=st.session_state.quiz_n, step=1,
                label_visibility="collapsed",
            )
            st.session_state.quiz_n = int(quiz_n)

            doc_names = list(st.session_state.docs.keys())
            if len(doc_names) > 1:
                st.markdown('<div class="section-header">✦ Quiz On</div>', unsafe_allow_html=True)
                quiz_doc_focus = st.selectbox(
                    "quiz_doc",
                    ["All documents"] + doc_names,
                    label_visibility="collapsed",
                )
            else:
                quiz_doc_focus = doc_names[0] if doc_names else "All documents"

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✦ Generate Quiz", use_container_width=False, key="gen_quiz"):
                if not doc_names:
                    st.warning("Upload a document first.")
                else:
                    if quiz_doc_focus == "All documents":
                        combined_text = "\n\n".join(m["full_text"] for m in st.session_state.docs.values())
                    else:
                        combined_text = st.session_state.docs[quiz_doc_focus]["full_text"]

                    with st.spinner(f"Generating {st.session_state.quiz_n} questions…"):
                        items = generate_quiz(combined_text, n=st.session_state.quiz_n)

                    st.session_state.quiz_items = items
                    st.session_state.quiz_index = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_done = False
                    st.session_state.quiz_generated = True
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_chosen = -1
                    st.rerun()

        # ── Results screen ────────────────────────────────────────────────
        elif st.session_state.quiz_done:
            total = len(st.session_state.quiz_items)
            score = st.session_state.quiz_score
            pct = int(100 * score / total) if total else 0
            grade = (
                "Excellent! 🏆" if pct >= 80 else
                "Good Job! 👍" if pct >= 60 else
                "Keep Studying 📚"
            )
            st.markdown(f"""
            <div class="score-box">
              <div class="score-grade">{grade}</div>
              <div class="score-big">{pct}%</div>
              <div class="score-sub">{score} / {total} correct</div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🔄 Retry Same Quiz", use_container_width=True):
                    st.session_state.quiz_index = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_done = False
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_chosen = -1
                    st.rerun()
            with c2:
                if st.button("🎲 New Quiz", use_container_width=True):
                    reset_quiz()
                    st.rerun()
            with c3:
                if st.button("💬 Back to Chat", use_container_width=True):
                    reset_quiz()
                    st.session_state.mode = "chat"
                    st.rerun()

        # ── Active question ───────────────────────────────────────────────
        else:
            items = st.session_state.quiz_items
            total = len(items)
            idx = st.session_state.quiz_index
            item = items[idx]
            pct_bar = int(100 * idx / total)

            # Progress header
            st.markdown(f"""
            <div class="quiz-header">
              <div class="quiz-header-top">
                <span class="quiz-title-label">✦ Quiz Mode</span>
                <span class="quiz-counter">Question {idx+1} of {total} &nbsp;·&nbsp; Score: {st.session_state.quiz_score}</span>
              </div>
              <div class="quiz-bar-bg">
                <div class="quiz-bar-fill" style="width:{pct_bar}%"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Question card
            st.markdown(f"""
            <div class="quiz-question-card">
              <div class="quiz-q-label">Question {idx+1}</div>
              <div class="quiz-q-text">{safe(item['q'])}</div>
            </div>
            """, unsafe_allow_html=True)

            answered = st.session_state.quiz_answered
            chosen = st.session_state.quiz_chosen
            correct_idx = item["answer"]

            if not answered:
                # Show clickable option buttons
                for oi, opt in enumerate(item["options"]):
                    label = f"{chr(65+oi)}.  {opt}"
                    if st.button(label, key=f"qopt_{idx}_{oi}", use_container_width=True):
                        st.session_state.quiz_answered = True
                        st.session_state.quiz_chosen = oi
                        if oi == correct_idx:
                            st.session_state.quiz_score += 1
                        st.rerun()
            else:
                # Show colour-coded results
                for oi, opt in enumerate(item["options"]):
                    if oi == correct_idx:
                        cls, marker = "correct", "✓ Correct"
                    elif oi == chosen:
                        cls, marker = "wrong", "✗ Your Answer"
                    else:
                        cls, marker = "neutral", ""
                    st.markdown(
                        f'<div class="quiz-opt {cls}">'
                        f'{chr(65+oi)}.  {safe(opt)}'
                        f'<span style="float:right;font-size:11px;opacity:0.85;">{marker}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                # Result + explanation
                result_cls = "quiz-result-correct" if chosen == correct_idx else "quiz-result-wrong"
                result_text = "Correct! 🎉" if chosen == correct_idx else (
                    f"Incorrect — correct answer: {item['options'][correct_idx]}"
                )
                explanation = safe(item.get("explanation", ""))
                st.markdown(f"""
                <div class="quiz-explanation">
                  <span class="{result_cls}">{result_text}</span>
                  {"<br><br>" + explanation if explanation else ""}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                next_label = "🏁 Finish Quiz" if idx + 1 >= total else "Next Question →"
                col_next, col_abandon = st.columns([2, 1])
                with col_next:
                    if st.button(next_label, use_container_width=True, key="next_q"):
                        if idx + 1 >= total:
                            st.session_state.quiz_done = True
                        else:
                            st.session_state.quiz_index += 1
                            st.session_state.quiz_answered = False
                            st.session_state.quiz_chosen = -1
                        st.rerun()
                with col_abandon:
                    if st.button("Abandon Quiz", use_container_width=True, key="abandon_quiz"):
                        reset_quiz()
                        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)