# GymGenie 🧞‍♂️

*"Slow is smooth, smooth is fast."*

GymGenie is a comprehensive, multi-tenant fitness web application featuring a built-in Customer Relationship Management (CRM) system. It acts as a Digital Personal Trainer for gym members while empowering gym owners and trainers with actionable insights and management tools.

## 🌟 Key Features

### For Members
- **AI-Generated Plans:** Personalized workout and diet plans based on health goals (Lose/Gain/Maintain).
- **Workout Tracking:** Log sets, reps, weights, and visually track progress.
- **Product Catalog:** Browse gym-specific protein supplements and fitness gear.

### For Trainers
- **Member CRM:** Detailed profiles of assigned members, tracking adherence and consistency.
- **Alerts:** Get auto-notified when a member is at risk of churning or stalling in their goals.

### For Gym Owners
- **Multi-Gym Support:** Complete data isolation for different physical gym locations.
- **Analytics Dashboard:** Monitor member retention, popular workouts, and product sales.
- **Trainer Management:** Assign trainers to specific members and oversee performance.

## 🏗️ Tech Stack

- **Frontend:** React + TypeScript + Vite (Mobile-first design)
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (with SQLAlchemy and Alembic)
- **Authentication:** Google OAuth 2.0 + JWT Email/Password Auth

## 📁 Production Folder Structure

```
gymgenie/
├── frontend/                 # React + TypeScript (Vite)
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── api/              # Axios API client functions
│   │   ├── components/       # Reusable UI components (buttons, modals)
│   │   ├── context/          # React Context (Auth, Theme)
│   │   ├── hooks/            # Custom React hooks
│   │   ├── pages/            # Top-level page components
│   │   ├── styles/           # CSS modules / styling operations
│   │   ├── types/            # TypeScript interfaces and types
│   │   └── utils/            # Helper functions
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                  # FastAPI (Python)
│   ├── app/
│   │   ├── main.py           # Application entry point
│   │   ├── config.py         # Environment configuration
│   │   ├── database.py       # DB connection
│   │   ├── models/           # SQLAlchemy ORM Models
│   │   ├── schemas/          # Pydantic schemas (Request/Response)
│   │   ├── routers/          # API Endpoints by resource
│   │   ├── services/         # Business & AI logic layer
│   │   ├── middleware/       # Custom middleware (Role-based guards)
│   │   └── utils/            # Shared utilities (Hashing, JWT)
│   ├── alembic/              # Database migration scripts
│   ├── requirements.txt
│   └── .env                  # Local secrets (Not in version control)
│
├── skills/                   # Project documentation architecture and logic guides
├── ADR.md                    # Architecture Decision Records
└── README.md                 # This file
```

## 🚀 Getting Started

*(Instructions will be populated here once the frontend and backend bootstrapping is complete in the upcoming execution phase).*
