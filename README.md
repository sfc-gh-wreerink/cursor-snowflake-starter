# Cursor Snowflake Starter 🚀

This lightweight starter repo helps Snowflake Solutions Engineers build fast, repeatable demos and POCs using CursorAI and Streamlit.

You'll connect to Snowflake via the Python connector, run a basic query, and launch a simple UI to test SQL on your own account.

---

## 🧠 What This Repo Includes

- ✅ Snowflake connector boilerplate (`snowflake-connector-python`)
- ✅ Example query script (`example_query.py`)
- ✅ Streamlit app for interactive SQL testing
- ✅ `.env` template for secure configuration
- ✅ `requirements.txt` for quick virtualenv setup

---

## ⚙️ Prerequisites

- Python 3.8 or higher
- Access to a Snowflake account
- [CursorAI](https://cursor.com/en/downloads) installed (or use your preferred IDE)

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_ORG/cursor-snowflake-starter.git
cd cursor-snowflake-starter
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

```bash
cp .env.example .env
```

Then fill in your Snowflake credentials in `.env`.

---

### 5. Test the Snowflake connection

```bash
python demo/example_query.py
```

---

## ▶️ Run the Streamlit Demo App

```bash
streamlit run app/app.py
```

---

## 💡 Happy demoing!
