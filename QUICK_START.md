# Quick Start - Deploy Backend in 5 Minutes

## Step 1: Click to Deploy (2 min)

```
https://railway.app/new?repo=https://github.com/JacobEcoSeal/takeoff-system&rootDirectory=backend
```

1. Click the link above
2. Sign in with GitHub (you're already connected)
3. Railway will ask to confirm
4. Click "Deploy"
5. Watch the progress bar (2-3 minutes)
6. When done, you'll see: "Deployment successful"

## Step 2: Get Your URL (1 min)

After deployment:
1. Click "View Logs" or go to dashboard
2. Look for the URL (something like: `https://takeoff-backend-prod-xyz.railway.app`)
3. **Copy this URL** (you'll need it next)

## Step 3: Update Frontend (2 min)

```bash
cd /workspace/takeoff-system/frontend

# Edit .env.production - change line 1 to:
VITE_API_URL=https://[paste-your-railway-url]

# Example:
# VITE_API_URL=https://takeoff-backend-prod-abc123.railway.app

# Then push to GitHub:
git add .env.production
git commit -m "Connect to Railway backend"
git push origin main
```

Vercel will auto-redeploy in 30 seconds.

## Step 4: Test It Works (1 min)

1. Open: `https://frontend-self-seven-77.vercel.app`
2. Click "New Takeoff"
3. Enter any project name
4. Click "Next" → go through all steps → "Save"
5. Go to "Recent Projects" tab
6. **See your project = SUCCESS** ✅

---

## If Something Goes Wrong

### "Connection refused" or "Cannot reach backend"
**Fix:** Check your VITE_API_URL in .env.production
- Make sure it's: `https://[railway-url]` (NOT localhost)
- No trailing slash
- Redeploy frontend: `git push origin main`

### "Database: error" on health check
**Fix:** Restart Railway
- Railway dashboard → Click your project → Restart

### "Stats show 0 after creating project"
**Fix:** Refresh the page
- Frontend caches stats. Create project, then refresh page.

---

## Verify Everything

Test these three things:

### 1. Health Check
```bash
curl https://[your-railway-url]/health
# Should return JSON with "status": "healthy"
```

### 2. API Works
```bash
curl https://[your-railway-url]/api/projects
# Should return [] (empty list) or your projects
```

### 3. Frontend
- Open Vercel URL
- Create a project
- See it in "Recent Projects"
- Stats increment

---

## You're Done When:

✅ Railway backend is deployed  
✅ Frontend .env.production updated with Railway URL  
✅ Frontend shows projects in "Recent Projects"  
✅ Stats update when you create projects  
✅ No errors in frontend (F12 console)  
✅ `/health` returns database status  

---

## Next Steps

**After system is live:**
1. Test with real data for a day
2. Get feedback from team
3. Plan Phase 2 (PDF processing)

**Email campaign:**
- Resume after system is verified working
- Round 2 emails are ready (11 TIER 1 builders)

---

**Questions?** Check CURRENT_STATUS.md or IMPROVEMENTS.md
