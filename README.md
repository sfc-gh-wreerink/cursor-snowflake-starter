# * PLEASE FORK *
# Cursor Snowflake Starter 🚀

This lightweight starter repo helps Snowflake Solutions Engineers build fast, repeatable demos and POCs using CursorAI and Streamlit.

Use the built-in Snowflake extension in CursorAI to authenticate and run SQL files interactively—no setup or Python connection code required.

---

## 🧠 What This Repo Includes

- ✅ Example SQL query to test your Snowflake connection
- ✅ Streamlit app for interactive frontend testing (optional)
- ✅ `requirements.txt` for demo Streamlit usage

---

## ⚙️ Prerequisites

- [CursorAI](https://cursor.com/en/downloads) installed
- A Snowflake account with credentials ready
- (Optional) Python 3.8+ if running the Streamlit app

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_ORG/cursor-snowflake-starter.git
cd cursor-snowflake-starter
```

### 2. Open in CursorAI and Sign In

- Install the Snowflake extension in Cursor (if not already installed)
- Sign in to your Snowflake account using the extension (bottom bar)
- Open `demo/example_query.sql` and run it

---

---

## ▶️ Optional: Run the Streamlit Demo App

If you'd like to explore building a frontend around your queries:

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file in the base of your repo

```bash
cp .env.example .env
```

Fill in your Snowflake credentials.

### 4. Load your environment variables

```bash
export $(cat .env | xargs)  # for Unix/macOS
```

### 5. Then run the app

```bash
streamlit run app/app.py
```

---

## 📂 Repo Structure

```
cursor-snowflake-starter/
├── README.md
├── requirements.txt
├── demo/
│   └── example_query.sql       # Sample SQL to test Snowflake
├── app/
│   └── app.py                  # Optional Streamlit UI
```

---

## 💬 Need Help?

- 📘 [Cursor IDE at Snowflake](https://snowflakecomputing.atlassian.net/wiki/spaces/EN/pages/4344021006/Cursor+IDE+at+Snowflake)
- 🎓 [CursorAI Training](https://docs.google.com/document/d/1Ab4ztdl-pVPxKMjYLIWLNDAYmkSKa_wzZKPCVCmDUPs/edit?tab=t.0)
- 💬 Slack: `#cursor-se`

---

## 💡 Happy demoing!
