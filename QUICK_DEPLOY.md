# One-Command Deployment Guide

**Get your system live in 15 minutes with minimal effort.**

---

## What You Need (5 minutes to get)

### 1. GitHub Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. **Token name:** `ecoseal`
4. **Expiration:** 90 days
5. **Scopes:** Check `repo` and `workflow`
6. Click "Generate" and **copy the token**

### 2. Railway API Token
1. Go to: https://railway.app/account/tokens
2. Click "Create"
3. Copy the token

### 3. Vercel API Token
1. Go to: https://vercel.com/account/tokens
2. Click "Create Token"
3. Copy the token

---

## Run Deployment (Automated)

On your Windows machine, open PowerShell and paste this (all one line):

```powershell
python deploy.py --github-token YOUR_GITHUB_TOKEN --railway-token YOUR_RAILWAY_TOKEN --vercel-token YOUR_VERCEL_TOKEN
```

Replace:
- `YOUR_GITHUB_TOKEN` with your GitHub token
- `YOUR_RAILWAY_TOKEN` with your Railway token
- `YOUR_VERCEL_TOKEN` with your Vercel token

---

## What Happens Automatically

✅ Create GitHub repo  
✅ Push all code  
✅ Deploy backend to Railway  
✅ Deploy frontend to Vercel  
✅ Connect them together  
✅ Test everything  
✅ Print your live URLs

---

## You're Done!

Script will output:
```
Frontend: https://takeoff-system-xyz.vercel.app
Backend:  https://ecoseal-api.up.railway.app
```

Visit the frontend URL and you're live.

---

## Troubleshooting

**"Command not found: python"**
- Use `python3` instead of `python`

**"Tokens rejected"**
- Check tokens have correct scopes
- GitHub needs `repo` permission
- Tokens are case-sensitive

**"Failed to create repo"**
- Check GitHub token is valid
- Check username is correct
- GitHub API might be rate-limited (wait 5 min)

---

**That's it. One command deploys everything.**
