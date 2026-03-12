# 🎬 Frammer AI: Agentic SQL Analytics Bot

A high-performance Generative AI solution designed to transform natural language into actionable insights using video production metadata. This project was built for the GenAI Selection Task.

## 🚀 The Architecture
This project uses a **Compound AI System** approach:
- **Brain (LLM)**: Llama 3.3-70B (via Groq) for high-reasoning SQL generation.
- **Orchestration**: LangChain SQL Agent with a **Self-Correction Loop** (ReAct logic).
- **Data Layer**: PostgreSQL containerized via **Docker** for environment consistency.
- **Interface**: Streamlit for a clean, user-friendly data-chat experience.



## 🛠️ Tech Stack
- **Language**: Python 3.x
- **Agent Framework**: LangChain
- **Database**: PostgreSQL 15
- **Frontend**: Streamlit
- **Infrastructure**: Docker & Docker-Compose

## ⚡ Quick Start Guide

### 1. Prerequisites
Ensure you have **Docker Desktop** and **Python** installed.

### 2. Launch the Database
Start the containerized PostgreSQL instance:
```bash
docker-compose up -d