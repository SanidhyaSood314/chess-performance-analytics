# ♟️ Chess Performance Analytics

A full-stack chess analytics web application that transforms raw game data into **actionable performance insights** using engine evaluation and behavioral pattern analysis.

---

## 🚀 Overview

Most chess tools analyze moves.

This project goes further — it analyzes the **player**.

It identifies:

* Where you make mistakes
* Which phase you struggle in
* What you should improve

👉 Turning raw engine evaluations into **coaching insights**

---

## ✨ Key Features

### 🔍 Game Analysis

* Upload PGN or fetch games from Chess.com
* Engine-powered evaluation using Stockfish
* Move classification:

  * Brilliant
  * Best
  * Great
  * Inaccuracy
  * Mistake
  * Blunder

---

### 📊 Performance Dashboard

* Win / Draw / Loss statistics
* Performance by color (White vs Black)
* Rating trends and opponent strength
* Time-based filtering (Today, Week, Month)

---

### 🧠 Intelligence Layer (Core Feature)

* Phase-wise accuracy:

  * Opening
  * Middlegame
  * Endgame
* Error pattern detection
* Player-specific analysis (only your moves)
* Insight generation:

  * Weakness identification
  * Error distribution

---

### 🎯 AI-like Coaching

* Personalized recommendations:

  * Tactical improvement
  * Phase-specific weaknesses
* Blunder pattern detection
* Actionable improvement suggestions

---

### 📈 Visualization

* Interactive chessboard
* Move navigation system
* Evaluation graph with proper move indexing
* Evaluation bar (real-time position strength)

---

### 🧾 Game Summary Report

* Auto-generated performance summary
* Combines:

  * Accuracy
  * Insights
  * Recommendations
* Provides a **clear takeaway for improvement**

---

## 🖥️ Tech Stack

* **Python**
* **Streamlit** (UI)
* **python-chess**
* **Stockfish** (engine)
* **Plotly** (visualizations)
* **Pandas**

---

## 🧠 Key Idea

Instead of just answering:

> “Was this move good or bad?”

This system answers:

> “Why are you losing, and how can you improve?”

---

## 📸 Screenshots

> Add screenshots here after running the app

Recommended:

* Dashboard
* Game Viewer
* Evaluation Graph
* Insights & Recommendations
* Game Summary

---

## ⚙️ How to Run

```bash
git clone https://github.com/your-username/chess-performance-analytics.git
cd chess-performance-analytics

pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
core/
  data/
  engine/
  analytics/
  intelligence/

services/
ui/
  components/
  views/

app.py
```

---

## 📌 Features Implemented

* PGN parsing
* Chess.com API integration
* Engine-based move evaluation
* Move classification system
* Accuracy calculation
* Player-specific analytics
* Phase-based performance analysis
* Insight generation engine
* Recommendation engine
* Game report generator

---

## 🚧 Future Improvements

* ECO-based opening detection
* Blunder heatmap visualization
* Player style classification
* Opening performance analytics
* Advanced coaching system

---

## 💡 Why This Project Matters

This project focuses on:

* **Data-driven decision making**
* **Behavioral pattern detection**
* **User-centric insights**
* **System design & architecture**

It bridges the gap between:

> raw analysis → meaningful improvement

---

## 🙌 Feedback

Feedback, suggestions, and improvements are welcome!

---
