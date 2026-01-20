# AI Interview Assistant

A full-stack AI-powered application to help software engineers **analyze resumes**, **generate interview questions**, and **create study plans**. Built with **FastAPI** (backend), **React** (frontend), and **OpenRouter GPT-4o-mini** AI.

---

## Features

- **Generate Interview Questions**  
  Ask for technical, behavioral, and system design questions for any topic.

- **Analyze Resume**  
  AI evaluates your resume and returns strengths, weaknesses, suggestions, and a score.

- **Generate Study Plan**  
  Create a daily study plan with actionable tips based on your goal.

- **Production-ready Backend**  
  - Handles invalid AI output safely  
  - Retries AI calls automatically  
  - Defaults returned on failure → no 500 errors  

- **Frontend-ready**  
  - React forms for all three routes  
  - Displays AI output neatly  
  - Handles errors gracefully  

---

## Tech Stack

- **Backend:** FastAPI, Pydantic, Uvicorn, OpenRouter GPT API  
- **Frontend:** React, Vite, JavaScript  
- **AI Provider:** OpenRouter (GPT-4o-mini)  

---

## Project Structure

ai-interview-assistant/
├─ backend/
│ ├─ main.py # FastAPI app
│ ├─ agent.py # AI agents setup
│ ├─ models.py # Pydantic models
│ └─ venv/ # optional virtual environment
├─ frontend/
│ ├─ package.json
│ ├─ src/
│ │ ├─ App.jsx
│ │ ├─ api.js # API helper
│ │ └─ Forms.jsx # All three forms
│ └─ public/
│ └─ index.html


