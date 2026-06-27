# LexGuard AI 🛡️

**production-style SaaS legal intelligence platform for Indian law.**

Built with: Flask · MySQL · SQLAlchemy · TF-IDF RAG · Flask-Login · Chart.js

---

## Features

| Feature | Description |
|---|---|
| 📄 Document Scanner | Upload PDF contracts, get clause-by-clause risk analysis (HIGH/MEDIUM/LOW) with fix suggestions |
| ⚖️ Legal Advisor | RAG-based IPC retrieval — ask any legal question, get relevant penal code sections + practical advice |
| 📚 Case Matcher | Search 15+ landmark Supreme Court cases with year/court filters |
| 👨‍⚖️ Lawyer Connect | Browse verified Indian lawyers by city, specialization, and rating |
| 🚨 Emergency Mode | One-tap SOS with GPS location via Twilio SMS + audio evidence recording |
| 📊 Dashboard | Documents analyzed, risk distribution Chart.js doughnut, recent activity |
| 🔐 Auth | Register/login with bcrypt passwords, Flask-Login sessions, RBAC roles |

---

## Project Structure

```
lexguard-ai/
├── app/
│   ├── __init__.py          # Flask factory
│   ├── routes/              # Blueprint route handlers
│   ├── services/            # Business logic layer
│   ├── models/              # SQLAlchemy ORM models
│   ├── auth/                # RBAC decorators
│   ├── utils/               # PDF extractor, risk analyzer, IPC retriever
│   └── config/              # Settings (dev/prod)
├── database/
│   └── seed.py              # Seed lawyers + legal cases
├── legal_corpus/
│   └── ipc_sections.json    # 51 IPC + special law sections (RAG corpus)
├── templates/               # Jinja2 HTML templates
├── static/css/ + js/        # Premium dark-theme SaaS UI
├── uploads/                 # Uploaded PDFs and audio evidence
├── .env                     # Environment variables (never commit!)
├── requirements.txt
├── run.py                   # Production entry point
└── Dockerfile
```

---

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Edit .env with your actual values:
DB_HOST=localhost
DB_PORT=3306
DB_NAME=lexguard_db
DB_USER=root
DB_PASSWORD=your_password
SECRET_KEY=your-secret-key-here
TWILIO_SID=...
TWILIO_AUTH=...
TWILIO_PHONE=+1...
SOS_TARGET_PHONE=+91...
```

### 3. Create MySQL Database
```sql
CREATE DATABASE lexguard_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Run the App (auto-creates tables)
```bash
python run.py
```

### 5. Seed Sample Data
```bash
python database/seed.py
```

Open: http://127.0.0.1:5000

---

## Docker Deployment
```bash
docker build -t lexguard-ai .
docker run -p 5000:5000 --env-file .env lexguard-ai
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/upload-document` | Upload + analyze PDF |
| POST | `/api/legal-query` | IPC retrieval legal advice |
| POST | `/api/find-cases` | Case similarity search |
| POST | `/api/find-lawyers` | Lawyer directory filter |
| POST | `/api/send-alert` | Emergency SOS SMS |
| POST | `/api/save-audio` | Upload audio evidence |

---

## Legal Disclaimer

This system is for **educational and informational purposes only**. It does not provide legal advice. Always consult a licensed lawyer for legal matters.