# 🌍 Autonomous AI Travel Planning Agent (Agentic RAG)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-19+-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-4169E1?style=flat&logo=postgresql&logoColor=white)](https://github.com/pgvector/pgvector)
[![Google Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-8E75C2?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4+-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

An end-to-end **Agentic AI Travel Planning System** that autonomously constructs personalized, day-by-day travel itineraries tailored to user budget, trip duration, starting location, and traveler count.

The system combines **multi-agent orchestration**, real-time **weather forecasting**, and an integrated **Retrieval-Augmented Generation (RAG)** pipeline backed by **PostgreSQL (`pgvector`)** and **Google Gemini** models with strict deterministic validation guardrails.

---

## 🌟 Key Features

- **🤖 Multi-Step Agentic Workflow:** Decouples travel planning into discrete, coordinated tasks: planning, weather analysis, context retrieval, itinerary synthesis, and validation.
- **🔍 Vector RAG Pipeline:** Semantic search over curated destination knowledge bases (e.g., Munnar, Wayanad guides) using high-dimensional embeddings and Cosine Distance filtering.
- **⚡ Vector Storage with `pgvector`:** PostgreSQL native vector extension storing 3072-dimensional document embeddings for sub-second similarity lookups.
- **🌦️ Real-Time Weather Intelligence:** Integrated destination geocoding and live meteorological data retrieval via Open-Meteo API.
- **🛡️ Deterministic Validation Guardrails:** Programmatic verification layer ensuring itineraries match user duration, budget constraints, and valid schema structures.
- **💻 Modern React Interface:** Clean, intuitive UI built with React, Vite, and Tailwind CSS featuring interactive trip request forms, animated loading states, and structured itinerary cards.

---

## 🧠 System Architecture & Workflow

```text
               User Travel Request
          (Destination, Budget, Duration)
                        │
                        ▼
               ┌─────────────────┐
               │  Agent Planner  │
               └────────┬────────┘
                        │
       ┌────────────────┴────────────────┐
       ▼                                 ▼
┌──────────────┐               ┌───────────────────┐
│ Weather Task │               │   RAG Pipeline    │
│ (Open-Meteo) │               │(PostgreSQL/pgvector│
└──────┬───────┘               └─────────┬─────────┘
       │ Live Forecast Data              │ Relevant Chunks
       └────────────────┬────────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │  Gemini Service │
               │ (LLM Synthesis) │
               └────────┬────────┘
                        │ Structured JSON Output
                        ▼
               ┌─────────────────┐
               │    Validator    │
               │  (Guardrails)   │
               └────────┬────────┘
                        │ Validated Travel Plan
                        ▼
               Frontend Dashboard
          (Interactive Day-wise UI)
```

---

## 🛠️ Tech Stack

| Layer | Technology | Details |
|---|---|---|
| **Frontend** | React 19, Vite, JavaScript | Single-page responsive UI |
| **Styling** | Tailwind CSS | Modern typography and responsive layout |
| **Backend** | Python 3.10+, Django 5+ | Robust RESTful application backend |
| **API Framework** | Django REST Framework (DRF) | JSON API endpoints with CORS support |
| **Database & Vector** | PostgreSQL + `pgvector` | Relational storage & Cosine similarity vector search |
| **LLM & Embeddings** | Google Gemini (`gemini-2.5-flash`) | Context synthesis and document embeddings |
| **External APIs** | Open-Meteo API | Geocoding and real-time weather forecasts |

---

## 📂 Project Structure

```text
Travel-Planning-Agent/
├── backend/
│   ├── config/
│   │   ├── settings.py           # Django configuration & DB setup
│   │   ├── urls.py               # Root URL routing
│   │   └── wsgi.py
│   ├── workflow/
│   │   ├── models.py             # TravelKnowledge model with VectorField
│   │   ├── planner.py            # Workflow task decomposition
│   │   ├── executor.py           # Multi-agent orchestrator
│   │   ├── weather.py            # Geocoding & Open-Meteo weather client
│   │   ├── document_loader.py    # Raw text and guide document loader
│   │   ├── chunking.py           # Document segmentation & text chunking
│   │   ├── embedding_service.py  # Google Gemini vector embedding generator
│   │   ├── ingest.py             # Vector database ingestion pipeline
│   │   ├── retrieval_service.py  # Semantic vector similarity search (CosineDistance)
│   │   ├── llm_service.py        # Gemini itinerary generation with schema enforcement
│   │   ├── validator.py          # Deterministic structural and duration validator
│   │   ├── views.py              # API view endpoints
│   │   ├── urls.py               # Workflow API routes
│   │   └── knowledge/            # Destination guides & curated travel context
│   │       ├── munnar_guide.txt
│   │       └── wayanad_guide.txt
│   ├── manage.py
│   ├── requirements.txt
│   └── .env                      # Environment secrets (API keys, DB credentials)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # Main application component & itinerary view
│   │   ├── main.jsx              # React DOM root
│   │   └── index.css             # Tailwind CSS directives
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- **Python 3.10+**
- **Node.js 18+ & npm**
- **PostgreSQL 15+** with the **`pgvector`** extension installed
- A **Google Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/))

---

### 1. Database Setup (PostgreSQL with `pgvector`)

Start PostgreSQL and execute the following commands in `psql`:

```sql
CREATE DATABASE travel_agent;
CREATE USER travel_user WITH PASSWORD 'your_password';
ALTER ROLE travel_user SET client_encoding TO 'utf8';
ALTER ROLE travel_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE travel_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE travel_agent TO travel_user;

-- Connect to the database and enable pgvector
\c travel_agent;
CREATE EXTENSION IF NOT EXISTS vector;
```

---

### 2. Backend Setup

1. **Navigate to the backend directory and activate a virtual environment:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**  
   Create a `.env` file in the `backend/` directory:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   DB_PASSWORD=your_postgres_password
   ```

4. **Run Migrations:**
   ```bash
   python manage.py makemigrations workflow
   python manage.py migrate
   ```

5. **Start the Django Development Server:**
   ```bash
   python manage.py runserver
   ```
   *The backend will be available at `http://127.0.0.1:8000`.*

---

### 3. Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd ../frontend
   ```

2. **Install Node modules:**
   ```bash
   npm install
   ```

3. **Launch the development server:**
   ```bash
   npm run dev
   ```
   *The frontend application will be running at `http://localhost:5173`.*

---

## 📡 API Documentation

### 1. Health Check
`GET /api/`

**Response:**
```json
{
  "message": "Travel Planning Agent API is running",
  "status": "success"
}
```

---

### 2. Generate Travel Itinerary
`POST /api/generate-trip/`

**Request Headers:**
```http
Content-Type: application/json
```

**Request Body:**
```json
{
  "starting_location": "Kochi",
  "destination": "Munnar",
  "budget": 15000,
  "duration": 3,
  "travelers": 2
}
```

**Sample Response:**
```json
{
  "success": true,
  "plan": [
    "Check destination weather forecast",
    "Retrieve relevant destination travel knowledge",
    "Generate day-wise travel itinerary using Gemini",
    "Validate itinerary duration and feasibility"
  ],
  "weather": {
    "temperature": 18.5,
    "description": "Partly Cloudy",
    "windspeed": 7.2
  },
  "itinerary": {
    "trip_title": "3-Day Scenic Escape to Munnar",
    "destination": "Munnar",
    "duration_days": 3,
    "estimated_cost_inr": 14200,
    "days": [
      {
        "day": 1,
        "theme": "Arrival & Tea Plantations",
        "morning": "Drive from Kochi to Munnar, check-in, visit Cheeyappara Waterfalls.",
        "afternoon": "Tour the KDHP Tea Museum and explore tea processing.",
        "evening": "Sunset walk through Blossom Hydel Park."
      },
      {
        "day": 2,
        "theme": "Wildlife & Scenic Peaks",
        "morning": "Morning safari at Eravikulam National Park (spot the Nilgiri Tahr).",
        "afternoon": "Boating at Mattupetty Dam and Echo Point.",
        "evening": "Traditional Kathakali and Kalaripayattu cultural performance."
      },
      {
        "day": 3,
        "theme": "Panoramic Views & Return",
        "morning": "Sunrise at Top Station overlooking the Western Ghats.",
        "afternoon": "Souvenir shopping for fresh tea, spices, and homemade chocolates.",
        "evening": "Departure journey back to Kochi."
      }
    ]
  },
  "warnings": []
}
```

---

## 📊 Git Workflow & Branching Strategy

The repository follows a clean **Feature Branching Strategy** ensuring modularity and reviewable development:

- `main`: Production-ready, validated code branch.
- `feature/planner-and-llm`: Core task planning logic and Gemini execution service.
- `feature/frontend-react`: React UI, form controls, and responsive styling.
- `feature/documentation`: Project specifications and developer documentation.
- `feature/context-and-database`: PostgreSQL database schema and context injection.
- `feature/rag-pipeline`: Text chunking, Gemini vector embeddings, and `pgvector` Cosine similarity search.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
