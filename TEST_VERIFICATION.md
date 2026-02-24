# Test Verification Guide

**Purpose:** Systematic verification that all components work correctly after Railway deployment

---

## Pre-Deployment Verification (Local)

### ✅ Code Quality
- [x] Backend main.py compiles without syntax errors
- [x] Frontend jsx compiles without syntax errors
- [x] All dependencies listed in requirements.txt
- [x] All npm dependencies listed in package.json

### ✅ API Endpoints (14 total)
**Projects:**
- [x] POST /api/projects (create)
- [x] GET /api/projects (list)
- [x] GET /api/projects/{id} (get one)
- [x] PUT /api/projects/{id} (update)
- [x] DELETE /api/projects/{id} (delete)

**Takeoffs:**
- [x] POST /api/projects/{id}/takeoffs (create)
- [x] GET /api/projects/{id}/takeoffs (list)
- [x] DELETE /api/projects/{id}/takeoffs/{id} (delete)

**Settings:**
- [x] POST /api/settings (update)
- [x] GET /api/settings/{key} (get)

**System:**
- [x] GET /api/stats (statistics)
- [x] GET /health (health check)
- [x] GET / (root)
- [x] @app.middleware("http") (request logging)

### ✅ Database Schema
- [x] ProjectDB table (projects)
- [x] TakeoffDB table (takeoffs)
- [x] SettingsDB table (settings)
- [x] Auto-creation on startup via Base.metadata.create_all()

### ✅ Input Validation
- [x] ProjectCreate validates name (not empty, < 255 chars)
- [x] ProjectCreate validates date format (ISO 8601)
- [x] TakeoffItem validates quantities (positive numbers)
- [x] TakeoffItem validates confidence (GREEN/YELLOW/RED)

### ✅ Error Handling
- [x] create_project: try/except with rollback
- [x] create_takeoff: try/except with rollback
- [x] get_stats: try/except with error response
- [x] health_check: handles database connection errors

### ✅ Frontend Integration
- [x] API client uses axios
- [x] API_URL configured via VITE_API_URL env var
- [x] All API methods exported correctly
- [x] Frontend calls loadProjects() on mount
- [x] Frontend calls loadStats() on mount
- [x] Stats display parsed correctly (nested structure)

---

## Post-Deployment Verification (After Railway Deploy)

### ✅ Step 1: Backend Health Check

**Action:** Run this command:
```bash
curl https://[railway-url]/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-24T15:00:00",
  "service": "EcoSeal Takeoff API",
  "database": "connected",
  "version": "1.0.0"
}
```

**Status Checks:**
- [ ] HTTP 200 status code
- [ ] "status": "healthy" (yes/no)
- [ ] "database": "connected" (not "error")
- [ ] Timestamp is current (within last 1 minute)

**If Failed:**
- Check Railway logs for error messages
- Verify requirements.txt was installed
- Restart Railway deployment

---

### ✅ Step 2: API List Projects (Empty)

**Action:**
```bash
curl https://[railway-url]/api/projects
```

**Expected Response:**
```json
[]
```

**Status Checks:**
- [ ] HTTP 200 status code
- [ ] Returns empty array (no projects yet)

**If Failed:**
- Check that database was created
- Check Railway logs for database errors

---

### ✅ Step 3: Frontend Connection

**Action:**
1. Open https://frontend-self-seven-77.vercel.app
2. Check browser console (F12 → Console tab)

**Expected:**
- Page loads without errors
- No red error messages in console
- Sidebar shows "Total Projects: 0"

**Status Checks:**
- [ ] Page loads (< 3 seconds)
- [ ] No console errors
- [ ] Stats show 0 projects
- [ ] "New Takeoff" button clickable

**If Failed:**
- Check that VITE_API_URL is set in Vercel environment
- Check that frontend .env.production has correct Railway URL
- Verify Vercel has redeployed after env change

---

### ✅ Step 4: Create a Project (End-to-End)

**Action:**
1. Click "New Takeoff" button
2. Enter project name: "Test Project 1"
3. Keep default date
4. Click "Next" button
5. Continue through all steps
6. On final step, click "✓ Save to Database"

**Expected:**
- No error messages
- Alert appears: "Takeoff saved!"
- Button text changes to "Creating..." then back

**Status Checks:**
- [ ] Form accepts input
- [ ] Create button is clickable
- [ ] Network request succeeds (check F12 → Network)
- [ ] API response is 200/201
- [ ] Project appears in Recent Projects tab

**If Failed:**
- Check console for CORS errors
- Check API URL is correct
- Verify backend is running (check /health)

---

### ✅ Step 5: Verify Data Persists

**Action:**
1. Go to "Recent Projects" tab
2. Look for "Test Project 1" in the list

**Expected:**
- Project name appears in table
- Created date matches today
- Status shows "draft"

**Status Checks:**
- [ ] Project appears in list
- [ ] Date is correct
- [ ] All columns populated
- [ ] Multiple projects can be created

---

### ✅ Step 6: Verify Stats Update

**Action:**
1. Look at sidebar stats
2. Should show "Total Projects: 1"
3. Create another project
4. Refresh page (F5)
5. Stats should now show "Total Projects: 2"

**Expected:**
- Stats increment after each project
- Stats persist after page refresh

**Status Checks:**
- [ ] Initial stats: 1 project
- [ ] After creating 2nd: stats show 2 projects
- [ ] After refresh: stats still show 2 projects
- [ ] No "undefined" values

**If Failed:**
- Check that /api/stats returns correct structure
- Verify frontend parses nested stats (projects.total)
- Refresh browser cache (Ctrl+Shift+R)

---

### ✅ Step 7: Check Database Directly

**Action:** (For verification, not required for users)
```bash
curl https://[railway-url]/api/projects
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "name": "Test Project 1",
    "date": "2026-02-24T00:00:00",
    "notes": null,
    "status": "draft",
    "created_at": "2026-02-24T15:XX:XX.XXXXX",
    "updated_at": "2026-02-24T15:XX:XX.XXXXX"
  },
  {
    "id": 2,
    "name": "Test Project 2",
    ...
  }
]
```

**Status Checks:**
- [ ] Correct number of projects
- [ ] All fields populated
- [ ] Timestamps are reasonable
- [ ] IDs increment sequentially

---

### ✅ Step 8: Check Logs

**Action:**
1. Go to Railway dashboard
2. Select your project
3. Click "Logs" tab
4. Look for request logs

**Expected Output:**
```
GET /api/projects - Status: 200
POST /api/projects - Status: 201
GET /api/stats - Status: 200
GET /health - Status: 200
```

**Status Checks:**
- [ ] Logs appear in real-time
- [ ] Status codes are 2xx (successful)
- [ ] No 5xx errors
- [ ] Requests match API calls you made

**If Errors:**
- [ ] 400 errors: invalid input (check form validation)
- [ ] 404 errors: resource not found (shouldn't happen)
- [ ] 500 errors: server error (check exception details in logs)

---

## Troubleshooting Matrix

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Cannot reach backend" | VITE_API_URL wrong | Update .env.production, push to GitHub |
| "Database: error" | DB not initialized | Restart Railway |
| Stats show 0 after create | Cache/timing issue | Refresh page (F5) |
| "CORS error" | Frontend/backend mismatch | Verify URLs match exactly |
| No logs in Railway | App crashed | Check startup logs, fix error |
| Projects don't appear in list | API call failed | Check Network tab in F12, check response |

---

## Success Checklist

System is working when ALL of these are true:

- [ ] `/health` returns 200 with "database": "connected"
- [ ] `/api/projects` returns empty array initially
- [ ] Frontend loads without console errors
- [ ] Can create a project via frontend
- [ ] Project appears in "Recent Projects" tab
- [ ] Stats increment when creating projects
- [ ] Stats persist after page refresh
- [ ] Railway logs show incoming requests
- [ ] No error messages in browser console
- [ ] No 5xx errors in Railway logs

---

## Acceptance Criteria

**Phase 1 MVP is complete when:**

1. ✅ Frontend loads at Vercel URL
2. ✅ Backend responds at Railway URL
3. ✅ Create project flow works end-to-end
4. ✅ Data persists in database
5. ✅ Stats update correctly
6. ✅ No errors in logs
7. ✅ Health check passes

**If all 7 are true, system is READY FOR PHASE 2.**

---

## Next: Phase 2 Setup

After verifying all the above:

1. Document any issues found
2. Plan Phase 2 (PDF processing)
3. Begin PDF upload endpoint
4. No code changes needed to current system

---

**Updated:** Feb 24, 2026  
**Status:** Ready for Railway Deployment  
**Testing Duration:** ~15 minutes
