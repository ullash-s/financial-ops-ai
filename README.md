# 💼 AI-Powered Financial Operations System

An intelligent back-office automation platform that simulates how AI can 
streamline financial asset recovery operations.

Built with Python, Streamlit, Pandas, and Plotly.

---

## 🚀 Live Demo

> Run locally or via GitHub Codespaces (see setup below)

---

## 📌 Features

### 📊 Business Dashboard
- Real-time KPI metrics (total owed, recovered, recovery rate)
- Interactive charts: case status breakdown, recovery by industry
- Full case management table

### 🧾 Invoice Processor
- Upload plain text invoices
- Automatically extracts: client name, invoice number, dates, amount, status
- Displays structured output instantly
- Rule-based extraction (upgradeable to LLM)

### 🤖 AI Decision Agent
- Analyzes every case and recommends the next best action
- Actions include: Escalate, Send Final Notice, Schedule Call, Close, Monitor
- Urgency scoring: Critical / High / Low / None
- Single-case deep dive with full reasoning

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core language |
| Streamlit | Web UI framework |
| Pandas | Data manipulation |
| Plotly | Interactive charts |
| Regex | Invoice field extraction |

---

## ⚙️ Setup & Run

### Option 1: GitHub Codespaces (Recommended)
1. Click the green **Code** button on this repo
2. Select **Codespaces** → **Create codespace on main**
3. Wait for setup, then run:
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Option 2: Local Setup
```bash
git clone https://github.com/YOUR_USERNAME/financial-ops-ai.git
cd financial-ops-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure
```
financial-ops-ai/
├── app.py                        # Main Streamlit app
├── requirements.txt              # Dependencies
├── data/
│   ├── cases.csv                 # Sample recovery cases
│   └── invoices.csv              # Sample invoices
├── modules/
│   ├── dashboard.py              # Analytics dashboard
│   ├── invoice_processor.py      # Invoice extraction engine
│   └── decision_agent.py         # AI recommendation engine
└── assets/
    └── sample_invoice.txt        # Sample invoice for testing
```

---

## 💡 Architecture Decisions

- **Rule-based first**: The decision agent and invoice processor use 
  deterministic logic before AI — showing engineering judgment over hype
- **Modular design**: Each feature is an independent module, 
  mirroring real team structures
- **Simulated data**: CSV-based data layer makes the project portable 
  and easy to extend to a real database

---

## 🔮 Future Improvements

- [ ] Connect OpenAI API for LLM-powered invoice extraction
- [ ] Add PostgreSQL database backend
- [ ] User authentication system
- [ ] Email alert system for critical cases
- [ ] Export reports to PDF

---

## 👤 Author

Built as a portfolio project to demonstrate AI engineering, 
data automation, and full-stack Python development skills.
