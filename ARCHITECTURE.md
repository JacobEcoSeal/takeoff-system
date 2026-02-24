# EcoSeal Takeoff System - Architecture

## System Overview

```
Frontend (React)
    ↓
API (FastAPI)
    ↓
Database (SQLite)
```

---

## Current Status

### ✅ DONE (Feb 24, 2026)

1. **HTML Interface** (Static mockup)
   - All 7 steps functional
   - Live at: https://takeoff-system.vercel.app
   - File: `index.html`

2. **FastAPI Backend** (NEW)
   - SQLite database
   - Real persistent data
   - API endpoints for projects, takeoffs, settings
   - Real statistics (not mocked)
   - File: `backend/main.py`

### ⏳ NEXT (This Week)

1. **React Frontend**
   - Connected to API endpoints
   - Pull real project data
   - Create/edit/delete projects
   - View real takeoff history
   - Real statistics from `/api/stats`

2. **PDF Processing**
   - Vector extraction (pdfplumber)
   - Scale detection
   - Boundary extraction
   - Geometry calculations

3. **Deployment**
   - Backend → Railway
   - Frontend → Vercel
   - Database → SQLite (managed via backend)

---

## File Structure

```
/workspace/takeoff-system/
├── index.html (old static interface)
├── backend/
│   ├── main.py (FastAPI app with database)
│   ├── requirements.txt
│   ├── .env.example
│   ├── README.md
│   └── __init__.py
├── ARCHITECTURE.md (this file)
└── .git/
```

---

## Database

**SQLite** (`takeoff.db`)

Tables:
- `projects` (name, date, notes, status, created_at, updated_at)
- `takeoffs` (project_id, level, wall_type, material, quantity, unit, assembly, r_value, perimeter, height, confidence, created_at)
- `settings` (key, value, updated_at)

---

## API Endpoints

### Projects
```
POST   /api/projects                    → Create project
GET    /api/projects                    → List all projects
GET    /api/projects/{id}               → Get project
PUT    /api/projects/{id}               → Update project
DELETE /api/projects/{id}               → Delete project
```

### Takeoffs
```
POST   /api/projects/{id}/takeoffs      → Create takeoff item
GET    /api/projects/{id}/takeoffs      → List takeoff items
DELETE /api/projects/{id}/takeoffs/{id} → Delete takeoff item
```

### Settings
```
POST   /api/settings                    → Update setting
GET    /api/settings/{key}              → Get setting
```

### Stats (Real Data)
```
GET    /api/stats                       → Real system statistics
GET    /health                          → Health check
```

---

## Key Design Decisions

1. **SQLite, not PostgreSQL**
   - Simpler deployment
   - File-based, no external service needed
   - Sufficient for current scale

2. **FastAPI, not Flask**
   - Type safety (Pydantic)
   - Auto-generated docs (/docs)
   - Better async support

3. **Stateless API**
   - Frontend makes all requests
   - No session state on backend
   - Easy to scale

4. **Real Data, No Mocks**
   - Every endpoint hits the database
   - Stats are calculated from actual data
   - No fake numbers

---

## Next: React Frontend

Frontend will:
- Fetch real project list from `/api/projects`
- Create projects via `POST /api/projects`
- Display real stats from `/api/stats`
- Show actual takeoff history
- Integrate with PDF processing

---

## Deployment Plan

### Backend (FastAPI)
1. Push to GitHub
2. Connect Railway to GitHub repo
3. Railway auto-deploys on push
4. Database stored with Railway project

### Frontend (React)
1. Update API URL to Railway backend
2. Push to GitHub
3. Connect Vercel to GitHub repo
4. Vercel auto-deploys on push

---

## Cost

- **Railway Backend:** $5-10/month (free tier available)
- **Vercel Frontend:** Free
- **Database:** Included with Railway
- **Total:** ~$5/month (optional paid tier)

---

## Security Notes

- SQLite for local dev only
- Production: Use PostgreSQL
- API keys stored in Railway environment variables
- CORS enabled for development (restrict in production)

---

## Progress Timeline

- **Feb 24 (Today):** Backend structure + API ✅
- **Feb 25 (Tomorrow):** React frontend + database integration
- **Feb 26-27:** PDF processing endpoints
- **Feb 28:** Full system integration + testing
