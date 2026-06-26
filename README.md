# 🛡️ GARUDA AI — Intelligent Conversational Crime Intelligence & Analytics Platform

> **AI Camp Hackathon 2026 | Track A: Rapid Application Prototyping**  
> **Solo Submission** | GCP Project: `aicamp26062026`

---

## 🎯 Problem Statement

Design and develop an Intelligent Conversational AI and Crime Analytics Platform that enables investigators, analysts, and policymakers to interact with crime database using natural language queries, while providing advanced analytical capabilities grounded in criminology and sociological insights.

---

## 🏆 Solution Overview

**GARUDA AI** is a full-stack crime intelligence platform built on Google Cloud that combines:

1. **Conversational AI** (English + Kannada) powered by Gemini 2.0 Flash
2. **Criminal Network Visualization** with graph-based relationship mapping
3. **Crime Trend Analytics** with criminological theory grounding
4. **Predictive MO Pattern Matching** for proactive law enforcement

---

## ✨ Key Features

### 🎙️ 1. Conversational Crime Intelligence
- Natural language queries in **English and ಕನ್ನಡ (Kannada)**
- Automatic NL-to-SQL translation via Gemini
- Context-aware follow-up conversations
- **Voice input** (Web Speech API - STT)
- **Voice output** (Browser TTS)
- **PDF export** of conversation history
- Criminological analysis with every response

### 🕸️ 2. Criminal Network & Relationship Analysis
- Interactive network graph (Plotly + NetworkX)
- Suspect → FIR → Victim → Gang → Financial Account mapping
- Organized crime group detection
- Suspicious financial flow tracking (UPI, NEFT, Hawala, Crypto)
- Repeat offender identification

### 📊 3. Crime Pattern & Trend Analysis
- Crime type distribution analysis
- Geographic hotspot identification
- Event/festival-based crime spike detection
- Monthly trend lines by crime category
- Time-of-day analysis (Routine Activity Theory)
- Socioeconomic correlation (Strain Theory validation)
- Neighborhood × Crime Type heatmap

### 🕵️ 4. MO Pattern Matcher & Predictive Intel
- Active case MO comparison against full database
- Serial crime pattern identification
- Suspect profiling and gang attribution
- Criminology-grounded prevention strategies
- Risk scoring for neighborhoods

---

## 🧠 Criminological Frameworks Applied

| Theory | Application |
|--------|-------------|
| **Strain Theory** (Merton) | Poverty/unemployment correlation with crime rates |
| **Routine Activity Theory** | Event-based crime spikes, time-of-day patterns |
| **Social Disorganization** | Low patrol density + few youth centers = crime clusters |
| **Differential Association** | Gang network analysis, repeat offender patterns |

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────┐
│                  GARUDA AI Platform                  │
├────────────────────────────────────────────────────┤
│  Frontend: Streamlit         │
│  AI Engine: Vertex AI Gemini 2.0 Flash              │
│  Database: SQLite (Synthetic Karnataka Crime Data)  │
│  Visualization: Plotly + NetworkX                   │
│  Voice: Web Speech API (STT + TTS)                  │
│  Export: FPDF2 (PDF Reports)                        │
├────────────────────────────────────────────────────┤
│  Deployment: Google Cloud Run                       │
│  Build: Cloud Build (from source)                   │
│  Region: us-central1                                │
│  Project: aicamp26062026                            │
└────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment (One Command)

### Prerequisites
- Google Cloud SDK (`gcloud`) installed and authenticated
- Project `aicamp26062026` with billing enabled

### Deploy to Cloud Run

```bash
# Windows
deploy.bat

# Linux/Mac
chmod +x deploy.sh && ./deploy.sh
```

### Or manually:
```bash
gcloud config set project aicamp26062026

gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com aiplatform.googleapis.com

gcloud run deploy garuda-ai-crime-platform \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars "GCP_PROJECT=aicamp26062026,GCP_LOCATION=us-central1" \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300
```

### Post-deployment: Grant Vertex AI access
```bash
gcloud projects add-iam-policy-binding aicamp26062026 \
    --member="serviceAccount:907061055748-compute@developer.gserviceaccount.com" \
    --role="roles/aiplatform.user"
```

---

## 📁 Project Structure

```
├── app.py                    # Main Streamlit application (complete platform)
├── generate_crime_data.py    # Synthetic crime database generator
├── crime_database.db         # SQLite database (auto-generated)
├── requirements.txt          # Python dependencies
├── Dockerfile                # Cloud Run container definition
├── deploy.sh                 # Linux/Mac deployment script
├── deploy.bat                # Windows deployment script
└── README.md                 # This file
```

---

## 📊 Synthetic Data Summary

| Entity | Count | Description |
|--------|-------|-------------|
| FIRs | 120 | Crime incidents (Jan-Jun 2026) |
| Offenders | 20 | Criminal profiles with gang affiliations |
| Victims | 15 | Diverse victim profiles |
| Neighborhoods | 12 | Bangalore areas with socioeconomic data |
| Financial Transactions | 50+ | Suspicious money flows |
| Crime Types | 8 | Burglary, Robbery, Narcotics, Assault, Cyber Fraud, Extortion, Vehicle Theft, Murder |
| Gangs | 3 | Majestic Boys, Cyber Syndicate 404, Kalyan Nagar Syndicate |

---

## 🔑 Technology Stack

- **Frontend**: Streamlit 1.35+ with custom CSS (glassmorphism dark theme)
- **AI/ML**: Google Vertex AI (Gemini 2.0 Flash) for NL-to-SQL + Analysis
- **Database**: SQLite with relational schema
- **Visualization**: Plotly (charts) + NetworkX (graph analysis)
- **Voice**: Web Speech API (browser-native, no API keys needed)
- **PDF**: FPDF2 for report generation
- **Deployment**: Google Cloud Run (serverless containers)
- **Analytics**: Pandas, NumPy, scikit-learn, statsmodels

---

## 🎤 Demo Queries to Try

**English:**
- "Show all cyber fraud cases in Koramangala"
- "Which gang has the highest average risk score?"
- "List all cold cases with loss above 5 lakh"
- "Find crimes during IPL matches"
- "Who are the repeat offenders in Majestic area?"

**ಕನ್ನಡ (Kannada):**
- "ಮೆಜೆಸ್ಟಿಕ್‌ನಲ್ಲಿ ಎಷ್ಟು ಸುಲಿಗೆ ಪ್ರಕರಣಗಳಿವೆ?"
- "ಯಾವ ಆರೋಪಿಗಳು ಪುನರಾವರ್ತಿತ ಅಪರಾಧಿಗಳು?"
- "ಕೊರಮಂಗಲದಲ್ಲಿ ಸೈಬರ್ ವಂಚನೆ ತೋರಿಸಿ"

---

## 📜 License

Built for AI Camp Hackathon 2026. For demonstration and educational purposes.

---

*Built with ❤️ using Google Cloud Vertex AI | AI Camp 2026*
