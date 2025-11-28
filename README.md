### WERAH - A Job Platform Backend

- A production-grade, distributed backend system designed to solve the recruitment "Cold Start" problem and the "Application Black Hole."

📖 Project Overview

- The Intelligent Matchmaker is not just a CRUD job board. It is a decoupled, asynchronous platform engineered to automate the recruitment lifecycle.

- Unlike traditional platforms, this system proactively aggregates data and provides intelligent feedback:

- Automated Ingestion: Uses a background scraper ecosystem (Celery + Redis) to populate the database with jobs from external sources, solving the marketplace "Cold Start" problem.

- Intelligent Ranking: Implements a dynamic Match Score Algorithm that calculates the compatibility between a candidate's skills and a job's requirements in real-time.

- Resilient Architecture: Built on a distributed Docker architecture with strict health checks, rate limiting middleware, and CI/CD pipelines.

🏗️ System Architecture

The project follows a micro-service-like architecture within a monolith, orchestrated via Docker Compose.

## Key Components

1. Web API (Django REST Framework): Handles HTTP requests, authentication (JWT), and business logic.
2. Database (PostgreSQL): Persistent storage for Users, Profiles, Jobs, and Applications.
3. Message Broker (Redis): Handles communication between the Web API and background workers.
4. Task Queue (Celery Worker): Executes heavy tasks (Emailing, Resume Parsing, Scraping) asynchronously to keep the API response time low (<100ms).
5. Scheduler (Celery Beat): Triggers the Job Scraper every 24 hours to fetch fresh data.

🚀 Key Features

🛡️ Security & Performance

1. Custom Rate Limiting Middleware: Implements a Fixed Window algorithm using Redis to throttle abusive IP addresses (100 req/min).
2. JWT Authentication: Custom login endpoints returning Access/Refresh tokens and role-based redirects.
3. Email Verification: Secure, token-based account activation flow.
4. Container Healthchecks: Docker services wait for the Database to be fully ready (pg_isready) before starting, preventing race conditions.

🧩 Core Business Logic

1. Role-Based Access Control (RBAC): Distinct permissions for Candidates vs Recruiters.
2. Recruiters manage Companies and Jobs.
3. Candidates manage Profiles and Applications.
4. The Match Score: When a recruiter views applicants, the system calculates a percentage score (0-100%) based on the intersection of Job.required_skills and Candidate.skills.

5. Automated Scraper: A background task parses external job boards (e.g., MyJobMag) and intelligently creates Company and JobPosting records.

🛠️ Tech Stack

- Language: Python 3.11
- Framework: Django 5, Django REST Framework
- Database: PostgreSQL 15
- Async Queue: Celery 5, Redis 7

# Documentation: (Swagger/OpenAPI 3.0)

# DevOps: Docker, Docker Compose, GitHub Actions (CI)

# Testing: Django Test Framework (Unit & Integration)

⚡ Getting Started (Local Setup)

- Since this project relies on a complex infrastructure (Redis, Workers, DB), it is fully containerized for easy setup.

# Prerequisites

- Docker & Docker Compose installed.
- Git.

1. Clone the Repository

git clone [https://github.com/Pascal7601/alx-project-nexus.git](https://github.com/Pascal7601/alx-project-nexus.git)
cd alx-project-nexus

2. Configure Environment

- Create a .env file in the root directory:

3. Build & Run

- Run the application stack. This will build the images, apply database migrations, and start all 5 services.
- docker-compose up --build

- Wait until you see Container web Started in the logs.

📖 API Documentation

- The API is fully documented using Swagger (OpenAPI 3.0).

- Ensure the server is running (docker-compose up).

# Visit: http://127.0.0.1:8000/swagger/

You can interact with every endpoint directly from the browser.

🧪 Testing & CI/CD

# The project includes a robust suite of Unit and Integration tests covering:

- User Registration Signals.
- Permission Enforcement (e.g., Candidates cannot post jobs).
- Application Flow Constraints (No duplicate applications).

# To run tests locally inside Docker:

# docker-compose exec web python manage.py test

## Continuous Integration:

- A GitHub Actions workflow (.github/workflows/ci.yml) automatically spins up ephemeral Postgres and Redis containers to lint and test the code on every Push/PR to the main branch.

📂 Project Structure

.
├── .github/workflows/ # CI/CD Pipeline configuration
├── core/ # Project Settings, Middleware, Root URLs
├── users/ # Custom User Model, Auth, Signals
├── jobs/ # Job Logic, Scraper, Celery Tasks
├── applications/ # Application Logic, Match Score
├── skills/ # Skills/Tags Management
├── docker-compose.yml # Infrastructure Orchestration
└── Dockerfile # Python Environment Definition
