# 🤖 AI Career Copilot

> An AI-powered resume analysis and career guidance platform that helps users identify their strengths, discover skill gaps, build personalized learning roadmaps, and prepare for technical interviews.

---

## 📌 Overview

**AI Career Copilot** is a web-based career assistance platform designed to help students and job seekers understand how well their resume aligns with their target career role.

Users can either paste their resume or upload a **PDF/DOCX** file and specify the role they want to target.

The application processes the resume and uses **Google Gemini AI** to generate a personalized career analysis containing:

- Relevant skills
- Missing skills
- Personalized learning roadmap
- Technical interview questions

The generated reports are stored in **TiDB Cloud**, allowing users to access their previous analyses through the History section.

---

## ✨ Features

### 🔐 User Authentication

- User signup and login
- Session-based authentication
- Personalized dashboard
- Logout functionality

### 📄 Resume Upload & Processing

Users can provide their resume through:

- Resume text
- PDF upload
- DOCX upload

The application automatically extracts text from uploaded documents before sending it for AI analysis.

### 🧠 AI Resume Analysis

The AI evaluates the resume according to the user's target role and generates:

#### Relevant Skills
Identifies skills from the resume that are useful for the selected career path.

#### Missing Skills
Identifies important skills that the user should develop for the target role.

#### Personalized Roadmap
Creates a learning roadmap focused on the identified skill gaps.

#### Interview Questions
Generates technical interview questions relevant to the target role.

---

## 🎯 Role-Based Analysis

The analysis changes according to the user's target role.

For example, the same resume can be evaluated for:

- Software Development Engineer
- Backend Developer
- Python Developer
- Data Analyst
- Data Scientist

This makes the system more useful than a generic resume checker.

---

## 📚 Analysis History

Every successful resume analysis is stored in the database.

Users can revisit their previous reports through the **History** section.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │        User         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Flask Web App    │
                    │                     │
                    │ Authentication      │
                    │ Dashboard           │
                    │ History             │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Resume Processing   │
                    │                     │
                    │ PDF → PyPDF2        │
                    │ DOCX → python-docx  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Google Gemini    │
                    │     AI Analysis     │
                    └──────────┬──────────┘
                               │
                               ▼
                ┌────────────────────────────┐
                │   Personalized Report      │
                │                            │
                │ • Relevant Skills          │
                │ • Missing Skills           │
                │ • Learning Roadmap         │
                │ • Interview Questions      │
                └──────────────┬─────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     TiDB Cloud      │
                    │   MySQL Database    │
                    │                     │
                    │ Users + Reports     │
                    └─────────────────────┘
