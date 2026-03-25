# Architecture Decision Records (ADR)

This file documents the major architectural decisions made for the **GymGenie** project.

---

## ADR 1: Choose Frontend Framework

**Date:** March 2026
**Status:** Accepted

### Decision
We will use **React** combined with **TypeScript** and built using **Vite**.

### Rationale
- **React** is ideal for complex, state-heavy dashboards (which the CRM entails).
- **TypeScript** ensures type safety across large data models (Members, Workouts, Diets, Products), drastically reducing runtime errors.
- **Vite** drastically improves developer experience with instant HMR (Hot Module Replacement) compared to Webpack or Create React App.
- The use-case specifies a web application accessed heavily on mobile phones; React components are modular and easily styled for mobile-first responsiveness.

---

## ADR 2: Choose Backend Framework

**Date:** March 2026
**Status:** Accepted

### Decision
We will use **FastAPI** with **Python**.

### Rationale
- Python is highly versatile and handles backend logic, data processing, and future AI LLM integrations seamlessly.
- FastAPI is lightning fast, asynchronous by default, and automatically generates interactive Swagger API documentation.
- The speed of development and built-in data validation using Pydantic pairs perfectly with a TypeScript frontend.

---

## ADR 3: Choose Primary Database

**Date:** March 2026
**Status:** Accepted

### Decision
We will use **PostgreSQL**.

### Rationale
- GymGenie has highly relational data: `Gyms` -> `Members` -> `Workout Logs` -> `Diet Plans`. Relational databases (SQL) are strictly better than NoSQL (like MongoDB) for this paradigm.
- PostgreSQL handles multi-tenancy (multiple gyms with isolated scopes) securely and performantly using heavily indexed foreign keys (`gym_id`).
- It allows for complex CRM queries out of the box (e.g., finding members without a workout in the last 7 days).

---

## ADR 4: Authentication Strategy

**Date:** March 2026
**Status:** Accepted

### Decision
We will implement dual authentication: **Google OAuth 2.0** alongside traditional **Email/Password** (JWT).

### Rationale
- **Google OAuth** lowers the barrier to entry significantly. Members hate creating passwords; one-click login improves gym member activation metrics.
- Traditional JWT is maintained as a fallback for users who prefer strict anonymity or do not have Google accounts.
- Role-Based Access Control (RBAC) will be injected into the JWT payload to separate Members from Trainers and Owners across the application boundaries.

---

## ADR 5: AI Logic Implementation

**Date:** March 2026
**Status:** Accepted

### Decision
Begin with **Rule-Based AI Algorithms**, moving to **LLM Integration (Groq)** in Phase 2.

### Rationale
- Diet calculations (BMR formulas, macroscopic splits) and basic workout pairings are finite mathematical constraints. A rule-based algorithm ensures 100% accuracy and immediate response times at zero cost.
- Once the core logic proves stable, incorporating an LLM (like LLaMA via Groq) will elevate the text response ("Here is why this workout helps you...") without risking the mathematical foundation.
