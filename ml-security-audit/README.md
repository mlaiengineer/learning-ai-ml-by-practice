# ML Security Audit 🔐

## Overview
A hands-on security audit of a deliberately vulnerable Machine Learning codebase.
The goal was to identify, understand, and fix common security vulnerabilities found in real-world ML systems.

---

## Vulnerabilities Identified & Fixed

| # | Vulnerability | Risk Level | Fix Applied |
|---|--------------|------------|-------------|
| 1 | Hardcoded Credentials | 🔴 Critical | Moved to `.env` file using `python-dotenv` |
| 2 | Unsafe Pickle Loading | 🔴 Critical | Replaced with safe `JSON` loading |
| 3 | No Input Validation | 🟠 High | Added type, size and value checks |
| 4 | Weak MD5 Hashing | 🟠 High | Replaced with `SHA256 + salt + pbkdf2_hmac` |
| 5 | No Access Control | 🟠 High | Added authorized users list |
| 6 | Insecure Model Saving | 🟠 High | Used `joblib` with `HMAC` integrity signature |
| 7 | No Logging or Monitoring | 🟡 Medium | Added full audit trail using `logging` |

---

## Key Concepts Learned

- **Hardcoded Credentials** — Never store passwords or API keys directly in code
- **Pickle Deserialization** — Pickle can execute arbitrary code, always prefer JSON for untrusted data
- **Input Validation** — Always validate data type, size, and content before processing
- **Cryptographic Hashing** — MD5 is broken, use SHA256 with salt and multiple iterations
- **Access Control** — Restrict sensitive operations to authorized users only
- **Model Integrity** — Use HMAC signatures to detect tampering with saved models
- **Audit Logging** — Always maintain a trail of who did what and when

---

## Project Structure
```
ml-security-audit/
│
├── vulnerable_ml_code.py    # Fixed secure version of the ML code
├── .env                     # Secret credentials (never shared)
├── README.md                # This file
└── ml_audit.log             # Generated log file after running
```

---

## Tools & Libraries Used

| Tool | Purpose |
|------|---------|
| `python-dotenv` | Secure credential loading |
| `hashlib` | Cryptographic hashing |
| `hmac` | Model integrity verification |
| `joblib` | Secure model serialization |
| `logging` | Audit trail and monitoring |
| `scikit-learn` | ML model (LogisticRegression) |

---

## How To Run
```bash
# 1. Install dependencies
pip install python-dotenv scikit-learn joblib numpy

# 2. Create your .env file
echo "DB_PASSWORD=yourpassword" > .env
echo "API_KEY=yourapikey" >> .env

# 3. Run the secure code
python vulnerable_ml_code.py
```

---

## What I Learned
Security in ML systems is just as important as model accuracy.
A vulnerable ML system can expose sensitive data, allow model poisoning,
and create serious risks for any real-world application.

---

*Part of my [learning-ai-ml-by-practice](https://github.com/mlaiengineer/learning-ai-ml-by-practice) journey* 🚀
