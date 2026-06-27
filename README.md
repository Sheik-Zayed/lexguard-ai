# 🛡️ LexGuard AI
### AI-Powered Legal Intelligence & Risk Detection Platform for Indian Law

---

## 📌 Overview

**LexGuard AI** is a production-style AI-powered Legal Intelligence Platform designed specifically for Indian law. It helps users analyze legal documents, identify risky contract clauses, retrieve relevant legal cases, obtain AI-assisted legal guidance, connect with verified lawyers, and access emergency legal protection features.

The platform combines **Artificial Intelligence**, **Natural Language Processing (NLP)**, **Retrieval-Augmented Generation (RAG)**, and **Full-Stack Web Development** to simplify legal understanding for everyone.

---

## ✨ Features

### 📄 AI Document Risk Analyzer
- Upload PDF legal documents
- Automatic clause extraction
- Risk classification (High, Medium, Low)
- AI-powered recommendations

---

### ⚖️ AI Legal Advisor
- Interactive legal chatbot
- Retrieval-Augmented Generation (RAG)
- Context-aware legal responses
- Supports Indian legal references

---

### 📚 Past Case Finder
- Search 300+ landmark Indian legal cases
- TF-IDF similarity search
- Keyword-based fallback search
- Relevant case recommendations

---

### 👨‍⚖️ Lawyer Connect
- Verified advocate directory
- Search by:
  - City
  - Specialization
  - Rating
- Contact through:
  - Phone
  - Email
  - WhatsApp

---

### 🚨 Protect Me (Emergency SOS)

Emergency legal protection feature:

- One-click SOS
- Voice activated emergency
- Live GPS tracking
- Automatic audio recording
- Twilio SMS alerts
- Evidence collection

---

### 📊 Dashboard

Personal analytics dashboard including:

- Risk distribution charts
- Uploaded documents
- Emergency history
- User activity

---

### 🔐 Authentication & Admin Panel

- Secure Login & Registration
- Password hashing using bcrypt
- Session Management
- Role-Based Access Control
- Admin dashboard
- Lawyer management system

---

# 🏗️ System Architecture

```
                User
                  │
                  ▼
        Flask Web Application
                  │
 ┌────────────────┼────────────────┐
 │                │                │
 ▼                ▼                ▼
Authentication   AI Services     Database
                 │               (MySQL)
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
Document     RAG Chat     Case Search
Analysis      System        Engine
      │
      ▼
Risk Detection

```

---

# 🛠️ Tech Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- Chart.js

## Backend

- Python
- Flask
- SQLAlchemy

## Database

- MySQL
- SQLite (Development)

## AI & Machine Learning

- OpenAI / Gemini
- LangChain
- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity

## External APIs

- Twilio API

## Utilities

- PyPDF2
- bcrypt
- Flask-Login

---

# 📂 Project Structure

```
LexGuard-AI
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── utils/
│   ├── auth/
│   └── config/
│
├── database/
│
├── legal_corpus/
│
├── static/
│
├── templates/
│
├── uploads/
│
├── run.py
├── wsgi.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/your-username/LexGuard-AI.git

cd LexGuard-AI
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=lexguard_db
DB_USER=root
DB_PASSWORD=password

SECRET_KEY=your_secret_key

GEMINI_API_KEY=your_api_key

TWILIO_SID=your_sid
TWILIO_AUTH=your_auth
TWILIO_PHONE=your_twilio_number
SOS_TARGET_PHONE=recipient_number
```

---

## Run the Application

```bash
python run.py
```

Open:

```
http://127.0.0.1:5000
```

---

# 📡 REST API

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/upload-document` | Analyze uploaded document |
| POST | `/api/legal-query` | Ask AI legal questions |
| POST | `/api/find-cases` | Search legal cases |
| POST | `/api/find-lawyers` | Search lawyers |
| POST | `/api/send-alert` | Send emergency alert |
| POST | `/api/save-audio` | Upload SOS recording |
| POST | `/api/sync-location` | Update GPS location |
| GET | `/api/dashboard-stats` | Dashboard analytics |

---

# 📸 Screenshots

> Add screenshots here after deployment.

### Home Page

```
screenshots/home.png
```

### Dashboard

```
screenshots/dashboard.png
```

### Document Analysis

```
screenshots/document-analysis.png
```

### AI Legal Advisor

```
screenshots/chatbot.png
```

---

# 🎯 Future Improvements

- Semantic Search using FAISS
- ChromaDB Integration
- OCR Support
- Docker Deployment
- CI/CD Pipeline
- Multilingual Support
- Voice Legal Assistant
- Mobile Application
- AI Case Prediction
- Advanced Analytics

---

# 📚 Learning Outcomes

This project demonstrates practical experience with:

- Full-Stack Development
- REST API Design
- Authentication
- Database Design
- Retrieval-Augmented Generation (RAG)
- AI Integration
- Machine Learning
- Natural Language Processing
- PDF Processing
- Cloud-ready Architecture

---

# ⚠️ Disclaimer

LexGuard AI is developed for educational and informational purposes only.

The AI-generated responses, legal analysis, and recommendations should **not** be considered professional legal advice. Always consult a qualified legal practitioner for legal decisions.

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Developer

**Sheik Zayed**

🎓 B.Tech Artificial Intelligence & Data Science

💼 Full Stack Developer | AI Enthusiast | Machine Learning

### Connect with me

- GitHub: https://github.com/Sheik-Zayed
- LinkedIn: https://www.linkedin.com/in/sheikzayed06/

---

⭐ If you found this project useful, don't forget to **Star** the repository.
