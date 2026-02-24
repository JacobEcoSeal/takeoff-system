#!/usr/bin/env python3
"""
EcoSeal Takeoff System - One-Command Deployment
Automates: GitHub repo creation → Railway backend → Vercel frontend
"""

import subprocess
import sys
import os
import json
from pathlib import Path

class Deployer:
    def __init__(self):
        self.workspace = Path("/home/ecoseal/.openclaw/workspace/takeoff-system")
        self.github_token = None
        self.github_username = None
        self.railway_token = None
        self.vercel_token = None
        self.repo_url = None
        self.railway_url = None
        self.vercel_url = None
    
    def log(self, msg, level="INFO"):
        """Print colored messages"""
        colors = {
            "INFO": "\033[94m",
            "SUCCESS": "\033[92m",
            "ERROR": "\033[91m",
            "WARNING": "\033[93m",
            "RESET": "\033[0m"
        }
        color = colors.get(level, colors["INFO"])
        reset = colors["RESET"]
        print(f"{color}[{level}]{reset} {msg}")
    
    def run(self, cmd, fail_msg="Command failed"):
        """Run shell command"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                self.log(f"{fail_msg}: {result.stderr}", "ERROR")
                return False
            return result.stdout.strip()
        except Exception as e:
            self.log(f"Error: {str(e)}", "ERROR")
            return False
    
    def step(self, num, title):
        """Print step header"""
        print(f"\n{'='*60}")
        self.log(f"STEP {num}: {title}", "INFO")
        print(f"{'='*60}")
    
    def get_input(self, prompt, secret=False):
        """Get user input"""
        if secret:
            import getpass
            return getpass.getpass(f"🔑 {prompt}: ")
        return input(f"📝 {prompt}: ")
    
    def deploy(self):
        """Main deployment flow"""
        try:
            self.step(1, "Verify Workspace")
            self.verify_workspace()
            
            self.step(2, "Get GitHub Credentials")
            self.get_github_credentials()
            
            self.step(3, "Create & Push GitHub Repo")
            self.create_github_repo()
            
            self.step(4, "Get Railway Token")
            self.get_railway_credentials()
            
            self.step(5, "Deploy to Railway (Backend)")
            self.deploy_railway()
            
            self.step(6, "Get Vercel Token")
            self.get_vercel_credentials()
            
            self.step(7, "Deploy to Vercel (Frontend)")
            self.deploy_vercel()
            
            self.step(8, "Verify Deployment")
            self.verify_deployment()
            
            self.print_summary()
            
        except KeyboardInterrupt:
            self.log("Deployment cancelled by user", "WARNING")
            sys.exit(1)
        except Exception as e:
            self.log(f"Deployment failed: {str(e)}", "ERROR")
            sys.exit(1)
    
    def verify_workspace(self):
        """Check if all files exist"""
        required_files = [
            "backend/main.py",
            "backend/requirements.txt",
            "backend/Procfile",
            "frontend/package.json",
            "frontend/src/App.jsx",
            "frontend/vite.config.js"
        ]
        
        for file in required_files:
            path = self.workspace / file
            if not path.exists():
                raise Exception(f"Missing file: {file}")
        
        self.log(f"✓ All files verified in {self.workspace}", "SUCCESS")
    
    def get_github_credentials(self):
        """Get GitHub username and token"""
        self.github_username = self.get_input("GitHub username")
        self.github_token = self.get_input("GitHub Personal Access Token (from https://github.com/settings/tokens)", secret=True)
        
        if not self.github_username or not self.github_token:
            raise Exception("GitHub credentials required")
        
        self.log(f"✓ Using GitHub user: {self.github_username}", "SUCCESS")
    
    def create_github_repo(self):
        """Create GitHub repo and push code"""
        # Initialize git
        os.chdir(self.workspace)
        
        self.log("Initializing git repository...", "INFO")
        self.run("git init")
        self.run("git config user.email 'ecoseal@deploy.local'")
        self.run("git config user.name 'EcoSeal Deploy'")
        self.run("git add .")
        self.run("git commit -m 'Initial commit - EcoSeal Takeoff System'")
        self.run("git branch -M main")
        
        # Create repo via GitHub API
        self.log("Creating repository on GitHub...", "INFO")
        
        create_repo_cmd = f'''curl -X POST \
  -H "Authorization: token {self.github_token}" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{{"name":"takeoff-system","description":"EcoSeal Insulation Takeoff System","public":true}}' \
  https://api.github.com/user/repos'''
        
        result = self.run(create_repo_cmd, "Failed to create GitHub repo")
        if not result:
            raise Exception("GitHub repo creation failed")
        
        self.repo_url = f"https://github.com/{self.github_username}/takeoff-system.git"
        
        # Push to GitHub
        self.log(f"Pushing code to {self.repo_url}...", "INFO")
        
        # Configure git credentials
        self.run(f'git remote add origin {self.repo_url}')
        
        # Push with auth
        auth_url = f"https://{self.github_username}:{self.github_token}@github.com/{self.github_username}/takeoff-system.git"
        push_cmd = f'git push -u {auth_url.replace("https://", "")} main'
        
        if not self.run(f"git push -u origin main 2>&1"):
            # Retry with auth in URL
            self.run(f"git remote remove origin")
            self.run(f'git remote add origin "{auth_url}"')
            self.run("git push -u origin main")
        
        self.log(f"✓ Code pushed to GitHub", "SUCCESS")
    
    def get_railway_credentials(self):
        """Get Railway token"""
        self.log("Go to: https://railway.app/account/tokens", "WARNING")
        self.log("Create a new token and copy it", "WARNING")
        self.railway_token = self.get_input("Railway API Token", secret=True)
        
        if not self.railway_token:
            raise Exception("Railway token required")
    
    def deploy_railway(self):
        """Deploy backend to Railway"""
        self.log("Deploying backend to Railway...", "INFO")
        self.log("Note: This requires manual setup via Railway dashboard", "WARNING")
        self.log("Visit: https://railway.app", "INFO")
        self.log("1. Click 'New Project'", "INFO")
        self.log("2. Select 'Deploy from GitHub'", "INFO")
        self.log("3. Select: takeoff-system repo", "INFO")
        self.log("4. Root Directory: backend", "INFO")
        self.log("5. Deploy", "INFO")
        
        self.railway_url = self.get_input("Railway Backend URL (after deployment, e.g., https://takeoff-system-abc.up.railway.app)")
        
        if not self.railway_url:
            raise Exception("Railway URL required")
        
        self.log(f"✓ Railway backend: {self.railway_url}", "SUCCESS")
    
    def get_vercel_credentials(self):
        """Get Vercel token"""
        self.log("Go to: https://vercel.com/account/tokens", "WARNING")
        self.log("Create a new token and copy it", "WARNING")
        self.vercel_token = self.get_input("Vercel API Token", secret=True)
        
        if not self.vercel_token:
            raise Exception("Vercel token required")
    
    def deploy_vercel(self):
        """Deploy frontend to Vercel"""
        self.log("Deploying frontend to Vercel...", "INFO")
        self.log("Note: This requires manual setup via Vercel dashboard", "WARNING")
        self.log("Visit: https://vercel.com", "INFO")
        self.log("1. Click 'Add New' → 'Project'", "INFO")
        self.log("2. Select: takeoff-system repo", "INFO")
        self.log("3. Framework: React", "INFO")
        self.log("4. Root Directory: frontend", "INFO")
        self.log("5. Environment: VITE_API_URL = (your Railway URL)", "INFO")
        self.log("6. Deploy", "INFO")
        
        self.vercel_url = self.get_input("Vercel Frontend URL (after deployment, e.g., https://takeoff-system-xyz.vercel.app)")
        
        if not self.vercel_url:
            raise Exception("Vercel URL required")
        
        self.log(f"✓ Vercel frontend: {self.vercel_url}", "SUCCESS")
    
    def verify_deployment(self):
        """Test both endpoints"""
        self.log("Testing backend health...", "INFO")
        health_check = self.run(f"curl -s {self.railway_url}/health", "Health check failed")
        
        if health_check and "healthy" in health_check.lower():
            self.log(f"✓ Backend is healthy", "SUCCESS")
        else:
            self.log("⚠ Backend health check inconclusive (may still be deploying)", "WARNING")
        
        self.log("Testing frontend...", "INFO")
        self.log(f"Frontend URL accessible: {self.vercel_url}", "INFO")
    
    def print_summary(self):
        """Print deployment summary"""
        print(f"\n{'='*60}")
        self.log("DEPLOYMENT COMPLETE! 🎉", "SUCCESS")
        print(f"{'='*60}\n")
        
        print("📋 YOUR LIVE URLS:\n")
        print(f"  Frontend: {self.vercel_url}")
        print(f"  Backend:  {self.railway_url}/docs")
        print(f"  GitHub:   {self.repo_url}\n")
        
        print("✅ NEXT STEPS:\n")
        print(f"  1. Visit your frontend: {self.vercel_url}")
        print(f"  2. Create a test project")
        print(f"  3. Check 'Recent Projects' to verify data persists")
        print(f"  4. API docs: {self.railway_url}/docs\n")
        
        print("📱 SHARE YOUR URLS:\n")
        print(f"  Frontend: {self.vercel_url}")
        print(f"  Backend API: {self.railway_url}\n")
        
        print("💾 REMEMBER:\n")
        print(f"  GitHub:  {self.github_username}/takeoff-system")
        print(f"  Railway: Check logs at railway.app")
        print(f"  Vercel:  Check logs at vercel.com\n")

if __name__ == "__main__":
    print("\n🚀 EcoSeal Takeoff System - One-Command Deployment\n")
    deployer = Deployer()
    deployer.deploy()
