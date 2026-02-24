# EcoSeal Takeoff System - Backend

**FastAPI + SQLite backend with real persistent data**

---

## Architecture

- **API:** FastAPI (Python)
- **Database:** SQLite (persistent storage)
- **Models:** SQLAlchemy ORM
- **Validation:** Pydantic

---

## Database Schema

### Projects
- `id` (int, primary key)
- `name` (string)
- `date` (datetime)
- `notes` (string)
- `status` (draft, in_progress, complete)
- `created_at` (datetime)
- `updated_at` (datetime)

### Takeoffs
- `id` (int, primary key)
- `project_id` (int, foreign key)
- `level` (string)
- `wall_type` (string)
- `material_type` (string)
- `quantity` (float)
- `unit` (string)
- `assembly` (string)
- `r_value` (string)
- `perimeter_ft` (float)
- `height_ft` (float)
- `confidence` (GREEN, YELLOW, RED)
- `created_at` (datetime)

### Settings
- `id` (int, primary key)
- `key` (string, unique)
- `value` (string)
- `updated_at` (datetime)

---

## API Endpoints

### Projects
- `POST /api/projects` → Create project
- `GET /api/projects` → List all projects
- `GET /api/projects/{id}` → Get project
- `PUT /api/projects/{id}` → Update project
- `DELETE /api/projects/{id}` → Delete project

### Takeoffs
- `POST /api/projects/{id}/takeoffs` → Create takeoff
- `GET /api/projects/{id}/takeoffs` → List takeoffs
- `DELETE /api/projects/{id}/takeoffs/{takeoff_id}` → Delete takeoff

### Settings
- `POST /api/settings` → Update setting
- `GET /api/settings/{key}` → Get setting

### Stats (Real Data)
- `GET /api/stats` → Get real system statistics
- `GET /health` → Health check

---

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

Server runs on `http://localhost:8000`

**API Docs:** `http://localhost:8000/docs`

---

## Deployment

### Railway (recommended)

1. Connect GitHub repo
2. Select `backend` directory as root
3. Set environment variables in Railway
4. Deploy

Backend URL: `https://yourapp.up.railway.app`

---

## Next Steps

1. ✅ Backend structure (DONE)
2. ⏳ Frontend (React) connected to API
3. ⏳ PDF processing endpoints
4. ⏳ Real takeoff calculations
