### WERAH - Job Platform

- This repository contains the backend source code for the "Intelligent Matchmaker," an advanced, scalable job platform designed to solve the "cold start" problem and provide a revolutionary experience for both candidates and recruiters.

1. The Vision: From "Dumb List" to "Smart Matchmaker"

1.1. The Problem

- Standard job boards are inefficient.

- For Recruiters: They are flooded with hundreds of unqualified resumes (the "Resume Flood").

- For Candidates: They submit applications into a "black hole" with no feedback.

  1.2. The Solution

- The "Intelligent Matchmaker" is a decoupled, asynchronous, and AI-powered platform designed to:

* Solve the "Cold Start": Automatically scrapes and aggregates external job postings to provide immediate value to candidates.

* Automate Curation: Uses AI to parse candidate resumes, extract skills, and algorithmically rank applicants for recruiters.

* Provide Feedback: Creates a transparent Application Tracking System (ATS) that notifies candidates of their status.

2. Key Features

## MVP (Minimum Viable Product)

- User Roles: Candidate and Recruiter roles.

- Company Profiles: Recruiters can create and manage their Company profile.

- Job Posting (Internal): Recruiters can post JobPostings.

- Core Application System: Candidates can apply for internal jobs, creating an Application record.

- Simple Job List & Filter: A public, searchable list of all jobs using basic Django icontains filtering.

- Job Scraper (Cold Start): A scheduled Celery Beat task that scrapes external job sites daily, populating the database.

- External Apply: Scraped jobs redirect candidates to the original external_url to apply.

## "Revolutionary" Features (Full Vision)

- AI Resume Parser: On signup, a candidate's resume is put into a Celery/Redis queue. A worker then parses the PDF/DOCX, extracts skills using NLP (spaCy), and auto-populates their CandidateProfile.

- Elasticsearch Engine: All JobPostings are indexed in Elasticsearch, enabling lightning-fast, typo-tolerant, and faceted search.

- AI Match Score: The system automatically generates a match_score for every Application by comparing candidate skills to job requirements.

- Automated ATS: Recruiters see applicants ranked by match_score. When they change an applicant's status, a Celery task automatically sends a notification email to the candidate.
