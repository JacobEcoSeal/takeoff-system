# Railway Backend Deployment (RECOMMENDED)

## Why Railway?
- ✅ Designed for Python apps (FastAPI works perfectly)
- ✅ Persistent filesystem (SQLite data persists)
- ✅ No cold start penalties
- ✅ Simple 1-click GitHub deployment
- ✅ Free tier available

## Step-by-Step

### 1. Deploy Backend to Railway

**Click this ONE link:**
```
https://railway.app/new?repo=https://github.com/JacobEcoSeal/takeoff-system&rootDirectory=backend
```

**What happens:**
- Railway recognizes the Python project
- Sees the `Procfile` and `requirements.txt`
- Auto-installs dependencies
- Deploys FastAPI app
- Assigns you a live URL (e.g., `https://takeoff-backend-prod-abc123.railway.app`)

**Wait 2-3 minutes.**

### 2. Get Your Backend URL

Once deployed, Railway shows your URL:
- Copy it (looks like: `https://takeoff-backend-prod-[random].railway.app`)
- Test it: `https://[your-url]/health` should return JSON

### 3. Update Frontend Environment Variable

**Method A: Via Git (Recommended for now)**

In `/workspace/takeoff-system/frontend/.env.production`:
```
VITE_API_URL=https://[your-railway-url]
```

Then:
```bash
git add frontend/.env.production
git commit -m "Update backend API URL to Railway"
git push origin main
```

Vercel will auto-redeploy within 1 minute.

**Method B: Via Vercel Dashboard (Better for production)**

1. Go to vercel.com → frontend project
2. Settings → Environment Variables
3. Add: `VITE_API_URL` = `https://[your-railway-url]`
4. Redeploy

### 4. Verify System Works

1. Open frontend: `https://frontend-self-seven-77.vercel.app`
2. Create a new project (give it a name)
3. Go to "Recent Projects" page
4. You should see your project listed with timestamp
5. Click on it - should show empty takeoffs list
6. **Success!** Your system is live.

## Database

Railway auto-provides filesystem storage. SQLite database file (`/tmp/takeoff.db`) will persist across requests.

For future scaling to PostgreSQL:
1. Add Postgres plugin in Railway dashboard
2. Get connection string
3. Set `DATABASE_URL` environment variable
4. Restart app

No code changes needed - our FastAPI app already supports both SQLite and PostgreSQL.

## Troubleshooting

**Backend returning errors?**
- Check Railway logs: railway.app dashboard → your project → Logs
- Most common: missing dependencies (should be auto-installed from requirements.txt)

**Frontend can't reach backend?**
- Verify VITE_API_URL is correct and matches your Railway URL
- Check browser console (F12 → Network tab) to see actual API calls
- CORS should work (FastAPI app allows all origins)

**Database file not persisting?**
- SQLite uses `/tmp/takeoff.db` which persists in Railway
- If data vanishes, check that app isn't crashing

## Next: Phase 2 (PDF Processing)

Once verified working:
- Add `/api/projects/{id}/upload-pdf` endpoint
- Integrate pdfplumber for vector extraction
- Implement scale detection
- Wire geometry calculations
- Build material quantity reports

---

**Time to live: ~10 minutes total**
1. Click Railway link: 1 min setup
2. Wait for deploy: 2-3 min
3. Update frontend URL: 2 min
4. Verify: 2 min
