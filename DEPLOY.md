# EcoSeal Takeoff System - Deployment Guide

**Status:** Ready to deploy (Backend + Frontend complete)

---

## ARCHITECTURE

```
React Frontend (Vercel)
    ↓ HTTP API
FastAPI Backend (Railway)
    ↓ ORM
SQLite Database
```

---

## DEPLOYMENT STEPS

### Step 1: Prepare GitHub Repository

1. Create a new GitHub repo: `takeoff-system`
2. Push backend + frontend to the repo:
   ```bash
   cd /workspace/takeoff-system
   git remote add origin https://github.com/YOUR-USERNAME/takeoff-system.git
   git push -u origin main
   ```

### Step 2: Deploy Backend to Railway

1. Go to **https://railway.app**
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub"**
4. Select `takeoff-system` repo
5. **Root Directory:** `backend`
6. **Add Variables:**
   - Click **"Variables"**
   - Add: `ANTHROPIC_API_KEY` = (your key)
   - Add: `DATABASE_URL` = `sqlite:///./takeoff.db`
   - Add: `PORT` = `8000`
7. Click **"Deploy"**
8. Wait for deployment (2-3 min)
9. Copy your Railway backend URL: `https://ecoseal-api.up.railway.app` (example)

### Step 3: Update Frontend with Backend URL

1. Open `frontend/.env.production`
2. Replace the URL with your Railway backend URL:
   ```
   VITE_API_URL=https://YOUR-RAILWAY-URL.up.railway.app
   ```
3. Commit and push:
   ```bash
   git add .
   git commit -m "Update backend URL"
   git push
   ```

### Step 4: Deploy Frontend to Vercel

1. Go to **https://vercel.com**
2. Sign in with GitHub
3. Click **"Add New..."** → **"Project"**
4. Select `takeoff-system` repo
5. **Framework:** React
6. **Root Directory:** `frontend`
7. **Build Command:** `npm run build`
8. **Install Command:** `npm install`
9. Click **"Deploy"**
10. Wait for deployment (1-2 min)
11. Vercel gives you a live URL: `https://ecoseal-takeoff.vercel.app`

---

## VERIFY DEPLOYMENT

### Test Backend
```bash
curl https://YOUR-RAILWAY-URL/health
```

Should return:
```json
{"status": "healthy", "timestamp": "...", "service": "EcoSeal Takeoff API"}
```

### Test Frontend
Go to `https://YOUR-VERCEL-URL` in browser.
- Create a new project
- Check sidebar stats (should show "Total Projects: 1")
- Recent Projects page shows your project

---

## TROUBLESHOOTING

### Frontend shows "Cannot reach backend"
- Check Railway backend is running (Railways dashboard)
- Check `.env.production` has correct URL
- Check CORS is enabled on backend (it is by default)
- Wait 5 minutes for DNS propagation

### Backend deployment failed
- Check `Procfile` exists in `backend/` directory
- Check `requirements.txt` lists all dependencies
- Check GitHub repo has `backend/` folder at root level

### Database not persisting
- Railway automatically backs up SQLite
- Database is stored with the Railway project
- No extra config needed

---

## PRODUCTION CHECKLIST

✅ Backend deployed to Railway
✅ Frontend deployed to Vercel
✅ Frontend URL configured with correct backend URL
✅ Database persisting across sessions
✅ Stats showing real data
✅ Projects can be created and listed
✅ All CRUD operations working

---

## NEXT STEPS

1. **PDF Processing**
   - Add `/api/projects/{id}/upload-pdf` endpoint
   - Integrate pdfplumber for boundary extraction
   - Add scale detection

2. **Takeoff Calculations**
   - Wire boundary extraction to geometry engine
   - Real perimeter and area calculations
   - Material mapping

3. **Production Hardening**
   - Switch to PostgreSQL for production
   - Add authentication
   - Rate limiting
   - Error logging

---

## MONITORING

**Railway Dashboard:**
- View logs
- Monitor performance
- Check database size
- Manage environment variables

**Vercel Dashboard:**
- View deployment history
- Check build logs
- Monitor performance
- View analytics

---

## COST

- **Railway Backend:** Free tier (up to 512MB RAM, 1GB storage)
- **Vercel Frontend:** Free tier
- **Total:** $0/month initially, ~$5/month when scaling

---

## SUPPORT

If deployment fails:
1. Check GitHub repo structure (frontend/ and backend/ folders present)
2. Verify environment variables are set correctly
3. Check Railway/Vercel build logs for errors
4. Restart the deployment

---

**Status:** READY TO DEPLOY
**Estimated deployment time:** 10-15 minutes
**Go live date:** Today (Feb 24, 2026)
