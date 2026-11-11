# Travel Planning Agent

A travel planning web application that generates personalized day-wise travel itineraries based on user preferences, budget, and trip duration.

The application uses Google Gemini API for itinerary generation and Open-Meteo API for destination weather information.

## Features

- Personalized travel planning
- AI-generated day-wise itineraries
- Destination weather information
- Travel budget and duration inputs
- Itinerary validation
- Responsive user interface
- Error handling for workflow failures

## Tech Stack

| Category | Technology |
|---|---|
| Frontend | React, JavaScript |
| Styling | Tailwind CSS |
| Backend | Python, Django |
| API Framework | Django REST Framework |
| Database | PostgreSQL (planned integration) |
| LLM | Google Gemini API |
| Weather API | Open-Meteo |
| Build Tool | Vite |

## Project Structure

```text
Travel-Planning-Agent/
│
├── backend/
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── workflow/
│   │   ├── planner.py
│   │   ├── executor.py
│   │   ├── weather.py
│   │   ├── llm_service.py
│   │   ├── validator.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── .env
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## AI Workflow

The application follows a multi-step AI workflow.

```text
       User Input
           |
           v
         Planner
           |
           v
         Executor
           |
      +----+----+
      |         |
      v         v
  Weather    Gemini
    API        API
      |         |
      +----+----+
           |
           v
   Itinerary Generation
           |
           v
       Validator
           |
           v
     Final Travel Plan
```

### Workflow Components

- **Planner:** Defines the tasks required to generate a travel plan.
- **Executor:** Coordinates the workflow execution.
- **Weather Service:** Retrieves destination weather information.
- **LLM Service:** Generates travel itineraries using Gemini API.
- **Validator:** Checks the generated itinerary structure and duration.

## Installation and Setup

### Prerequisites

- Python 3.10+
- Node.js and npm
- Google Gemini API key

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd Travel-Planning-Agent
```

### 2. Backend Setup

```bash
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

### 3. Configure Environment Variables

Create a `.env` file inside the `backend` directory.

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash
```

Replace the placeholder with your actual Gemini API key.

### 4. Frontend Setup

Open another terminal:

```bash
cd frontend

npm install

npm run dev
```

Open the application:

```text
http://localhost:5173
```

Backend:

```text
http://127.0.0.1:8000
```


## External APIs

- **Google Gemini API:** Used for generating personalized travel itineraries.
- **Open-Meteo API:** Used for retrieving destination weather information and geocoding.

## Project Status

Currently developed as a learning-focused MVP demonstrating multi-step AI workflows, API integration, structured output generation, and validation.

## Future Improvements

- PostgreSQL database integration
- Booking enquiry management
- Improved travel cost estimation
- Enhanced itinerary validation
- Deployment and production configuration

## License

This project is developed for educational and learning purposes.