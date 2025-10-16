# 💬 Chat with Data

> **An AI-powered Streamlit app that lets you chat with your CSV or Excel files using natural language — and automatically generates SQL queries and analysis results.**

---

## 🧠 Overview

**Chat with Data** transforms your data files into an interactive AI analyst.  
Simply upload a CSV or Excel file, type your question (e.g., *“What are the top 5 countries by total sales?”*), and the app uses a **LangChain-based AI agent** to:

- Understand your question  
- Generate the right SQL or Pandas query  
- Execute it directly on your uploaded dataset  
- Display results, summaries, and explanations  

No coding or query knowledge required — just chat with your data!

---

## ⚙️ How It Works

1. **Upload your CSV or Excel file**
2. The app **cleans and preprocesses** the data (`utils/file_processor.py`)  
3. The **AI Analyst Agent** (from `agent/main.py`) is initialized  
4. You **ask a question** about your data  
5. The agent:
   - Interprets your query  
   - Generates a SQL or Pandas query  
   - Executes it on your dataframe  
   - Returns both **results** and the **generated SQL code**

---

## 🧩 Key Features

✅ Upload and process **CSV or Excel** files  
✅ Chat with your data using **natural language**  
✅ Automatically generated **SQL queries**  
✅ View **data previews** and **results** in Streamlit  
✅ Works with **LangChain**, **Mistral**, or **any LLM backend**  
✅ Preprocessing handles:
   - Missing values (`NA`, `N/A`, `missing`)
   - Date column parsing
   - String cleaning (safe CSV formatting)

---

## 🧱 Project Structure

