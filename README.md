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

## 🧠 System Architecture & Multi-Agent Workflow

```text
┌────────────────────────────────────────────────────────┐
│                   User Travel Request                  │
│       Destination • Budget • Duration • Travelers      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
               ┌────────────────────────┐
               │    AI Task Planner     │
               │ (Workflow Coordinator) │
               └────────────┬───────────┘
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
   ┌───────────────────┐         ┌───────────────────┐
   │   Weather Agent   │         │   RAG Pipeline    │
   │   (Open-Meteo)    │         │  (pgvector Store) │
   │ Geocoding & Temp  │         │ Semantic Chunks   │
   └─────────┬─────────┘         └─────────┬─────────┘
             │                             │
             └──────────────┬──────────────┘
                            │ Augmented Context
                            ▼
               ┌────────────────────────┐
               │  Google Gemini Engine  │
               │ (Grounded Synthesis)   │
               └────────────┬───────────┘
                            │ Structured JSON
                            ▼
               ┌────────────────────────┐
               │  Validation Guardrail  │
               │ Duration & Schema Check│
               └────────────┬───────────┘
                            │ Validated Plan
                            ▼
┌────────────────────────────────────────────────────────┐
│                 Modern React Dashboard                 │
│      Day-by-Day Itinerary • Weather Cards • Budget     │
└────────────────────────────────────────────────────────┘
```

### Detailed Workflow Stages:
1. **Dynamic Task Planning (`planner.py`):** Decomposes the user's travel request into an execution plan of sequential and parallel tasks.
2. **Parallel Context Gathering:**
   - **Weather Agent (`weather.py`):** Automatically geocodes the destination into latitude/longitude coordinates and fetches real-time temperature, wind speed, and weather condition codes from the Open-Meteo API.
   - **RAG Retrieval Engine (`retrieval_service.py`):** Converts the trip request into a semantic query embedding, matches against PostgreSQL `pgvector`, and retrieves top-$k$ relevant destination knowledge chunks.
3. **Context-Grounded LLM Synthesis (`llm_service.py`):** Assembles the user details, live weather conditions, and retrieved travel knowledge into a structured prompt processed by Google Gemini.
4. **Deterministic Validation Guardrails (`validator.py`):** An independent programmatic validator inspects the itinerary to guarantee the number of generated days exactly equals user duration and required time slots (morning, afternoon, evening) are populated.

---

## 🛡️ Hallucination Prevention Strategy

LLMs are prone to hallucinating non-existent attractions, fictional travel spots, and unrealistic timings. This project implements a **three-tier anti-hallucination system**:

1. **RAG Grounding via `pgvector`:** Instead of allowing the model to generate itineraries purely from pre-training memory, the prompt is grounded in verified, curated travel knowledge (e.g., local guides, timing rules, real attractions) retrieved from PostgreSQL using 3072-dimensional vector embeddings.
2. **Strict Schema Constraints:** Uses Google Gemini's native structured outputs (`response_mime_type="application/json"` with strict `response_schema`), preventing the model from hallucinating invalid formats, missing day structures, or malformed JSON.
3. **Deterministic Programmatic Verification:** The output is passed through an independent Python validator (`validator.py`) before reaching the user. Any mismatch between requested duration and generated days is immediately flagged.

---

## 🔄 Resilience & Fallback Mechanisms

The system is built to gracefully handle external API failures, missing data, and unexpected user inputs without crashing:

- **🌦️ Weather Service Fallback:** If the Open-Meteo API or geocoding fails (e.g., remote locations, network outage), the workflow does **not** fail. It captures a graceful warning notice and allows itinerary generation to proceed with standard seasonal assumptions.
- **🔍 Multi-Tier Destination Matching Fallback:**
  - *Tier 1 (Exact):* Case-insensitive exact match (`destination__iexact`).
  - *Tier 2 (Split):* If the user enters a composite name like `"Munnar, Kerala"`, the system splits the string and queries primary city `"Munnar"`.
  - *Tier 3 (Contains):* Case-insensitive substring match (`destination__icontains`) as a final database lookup.
- **📐 Semantic Relevance Cutoff Fallback:** The vector retriever calculates Cosine Distance and filters with `distance <= 0.7`. If no chunks meet this relevance threshold (preventing irrelevant knowledge contamination), it falls back cleanly with `"No relevant travel knowledge found"`, enabling generalized AI synthesis.
- **🛡️ Validation Failure Fallback:** If generated data fails structural or duration integrity, the API returns a structured `HTTP 422 Unprocessable Entity` detailing the specific failure stage rather than delivering broken data to the frontend.

---

## 🛠️ Tech Stack

| Layer | Technology | Details |
|---|---|---|
| **Frontend** | React 19, Vite, JavaScript | Responsive single-page UI |
| **Styling** | Tailwind CSS | Modern card-based UI with responsive grids |
| **Backend** | Python 3.10+, Django 5+ | RESTful API orchestration backend |
| **API Framework** | Django REST Framework (DRF) | JSON API endpoints with CORS support |
| **Database & Vector** | PostgreSQL + `pgvector` | Relational storage & Cosine similarity vector search |
| **LLM & Embeddings** | Google Gemini (`gemini-2.5-flash`) | Context-augmented synthesis & vector embeddings |
| **External APIs** | Open-Meteo API | Free geocoding and live meteorological data |

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
│   │   ├── executor.py           # Multi-agent orchestrator & fallback handler
│   │   ├── weather.py            # Geocoding & Open-Meteo weather client
│   │   ├── document_loader.py    # Raw text and guide document loader
│   │   ├── chunking.py           # Document segmentation & text chunking
│   │   ├── embedding_service.py  # Google Gemini vector embedding generator
│   │   ├── ingest.py             # Vector database ingestion pipeline
│   │   ├── retrieval_service.py  # Multi-tier vector search (CosineDistance <= 0.7)
│   │   ├── llm_service.py        # Gemini itinerary generation with schema enforcement
│   │   ├── validator.py          # Deterministic structural and duration validator
│   │   ├── views.py              # API view endpoints & error handling
│   │   ├── urls.py               # Workflow API routes
│   │   └── knowledge/            # Curated destination guides
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

- **Python 3.10+**
- **Node.js 18+ & npm**
- **PostgreSQL** with `pgvector` extension
- **Google Gemini API Key**

---

### 1. Database Setup

Ensure PostgreSQL is running with the `pgvector` extension enabled:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

### 2. Backend Setup

1. **Activate virtual environment & install dependencies:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**  
   Create a `.env` file in the `backend/` directory:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   DB_PASSWORD=your_postgres_password
   ```

3. **Run Migrations & Start Server:**
   ```bash
   python manage.py makemigrations workflow
   python manage.py migrate
   python manage.py runserver
   ```
   *Backend runs at `http://127.0.0.1:8000`.*

---

### 3. Frontend Setup

1. **Install dependencies & launch dev server:**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```
   *Frontend runs at `http://localhost:5173`.*

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

## 🎓 Academic / Educational Project

This project is developed for educational and academic learning purposes.
