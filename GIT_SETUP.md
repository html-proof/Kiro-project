# 🚀 Git Setup & GitHub Push Guide

Complete guide to push your Musicly Backend to GitHub.

---

## ✅ Git Configuration (Already Done)

Your Git is configured with:
- **Email:** imeseban@gmail.com
- **Username:** html-proof
- **Repository:** https://github.com/html-proof/Kiro-project.git

---

## 🚀 Quick Push to GitHub

### Option 1: Use Push Script (Easiest)

**Windows:**
```bash
git-push.bat
```

**Linux/Mac:**
```bash
chmod +x git-push.sh
./git-push.sh
```

### Option 2: Manual Commands

```bash
# 1. Initialize Git (if not done)
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit: Complete Musicly Backend"

# 4. Set main branch
git branch -M main

# 5. Add remote
git remote add origin https://github.com/html-proof/Kiro-project.git

# 6. Push
git push -u origin main
```

---

## 📋 What Gets Pushed

### ✅ Included Files (50+ files)

**Code:**
- All Python files (30+)
- Configuration files
- Requirements.txt
- Procfile

**Documentation:**
- All .md files (18+)
- Setup guides
- API documentation

**Docker:**
- Dockerfile
- docker-compose.yml
- Docker scripts

**Firestore:**
- firestore.rules
- Deployment scripts

### ❌ Excluded Files (.gitignore)

**Secrets:**
- .env (your Firebase credentials)
- *firebase*.json files
- Service account keys

**Python:**
- __pycache__/
- *.pyc files
- Virtual environments

**IDE:**
- .vscode/
- .idea/
- .DS_Store

---

## 🔒 Security Check

Before pushing, verify these files are NOT included:

```bash
# Check what will be committed
git status

# Make sure these are NOT listed:
# - .env
# - *firebase*.json
# - Any files with credentials
```

**IMPORTANT:** Your `.env` file with Firebase credentials is protected by `.gitignore` and will NOT be pushed.

---

## 📝 Commit Message Guidelines

### Good Commit Messages

```bash
# Initial commit
git commit -m "Initial commit: Complete Musicly Backend"

# Feature additions
git commit -m "Add: Auto playlist generation feature"
git commit -m "Add: Docker support with compose files"

# Bug fixes
git commit -m "Fix: Redis connection timeout issue"
git commit -m "Fix: Firebase token verification"

# Updates
git commit -m "Update: API documentation"
git commit -m "Update: Firestore security rules"

# Refactoring
git commit -m "Refactor: Recommendation service for better performance"
```

---

## 🌿 Branch Strategy

### Main Branch (Production)

```bash
# Your main branch
git branch -M main
git push -u origin main
```

### Development Branch

```bash
# Create dev branch
git checkout -b development
git push -u origin development

# Switch between branches
git checkout main
git checkout development
```

### Feature Branches

```bash
# Create feature branch
git checkout -b feature/playlist-sharing
git push -u origin feature/playlist-sharing

# Merge to main
git checkout main
git merge feature/playlist-sharing
git push
```

---

## 🔄 Common Git Commands

### Check Status

```bash
# See what's changed
git status

# See what's staged
git diff --staged
```

### Add Files

```bash
# Add all files
git add .

# Add specific file
git add app/main.py

# Add specific folder
git add app/services/
```

### Commit

```bash
# Commit with message
git commit -m "Your message"

# Commit with detailed message
git commit -m "Title" -m "Detailed description"

# Amend last commit
git commit --amend -m "Updated message"
```

### Push

```bash
# Push to main
git push origin main

# Push to specific branch
git push origin development

# Force push (use carefully!)
git push -f origin main
```

### Pull

```bash
# Pull latest changes
git pull origin main

# Pull and rebase
git pull --rebase origin main
```

### View History

```bash
# View commit history
git log

# View compact history
git log --oneline

# View last 5 commits
git log -5
```

---

## 🔧 Fixing Common Issues

### Issue: "Repository already exists"

```bash
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/html-proof/Kiro-project.git

# Push
git push -u origin main
```

### Issue: "Failed to push - rejected"

```bash
# Pull first, then push
git pull origin main --rebase
git push origin main

# Or force push (if you're sure)
git push -f origin main
```

### Issue: "Accidentally committed .env"

```bash
# Remove from Git (keeps local file)
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from Git"

# Push
git push origin main
```

### Issue: "Wrong commit message"

```bash
# Change last commit message
git commit --amend -m "Correct message"

# Force push if already pushed
git push -f origin main
```

### Issue: "Need to undo last commit"

```bash
# Undo commit, keep changes
git reset --soft HEAD~1

# Undo commit, discard changes
git reset --hard HEAD~1
```

---

## 📊 Repository Structure on GitHub

```
Kiro-project/
├── .github/              (optional - CI/CD workflows)
├── app/                  (Python backend code)
├── docs/                 (optional - documentation)
├── .dockerignore
├── .env.example          (template for .env)
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── firestore.rules
├── Procfile
├── README.md
├── requirements.txt
└── [All other files]
```

---

## 🚀 After Pushing to GitHub

### 1. Verify on GitHub

Visit: https://github.com/html-proof/Kiro-project

Check:
- [ ] All files are there
- [ ] .env is NOT visible
- [ ] README.md displays correctly
- [ ] No secrets exposed

### 2. Set Up GitHub Actions (Optional)

Create `.github/workflows/deploy.yml` for CI/CD

### 3. Add Repository Description

On GitHub:
1. Go to repository settings
2. Add description: "Musicly Backend - Spotify-like music streaming API"
3. Add topics: python, fastapi, firebase, redis, youtube, music-streaming

### 4. Enable GitHub Pages (Optional)

For documentation hosting

### 5. Set Up Branch Protection

Protect main branch:
1. Settings → Branches
2. Add rule for `main`
3. Require pull request reviews
4. Require status checks

---

## 🔐 Environment Variables for Deployment

### Railway Deployment

When deploying to Railway:

1. **Don't commit .env to GitHub**
2. **Add environment variables in Railway dashboard:**
   - FIREBASE_SERVICE_ACCOUNT_JSON
   - REDIS_URL (auto-created)
   - ALLOWED_ORIGINS
   - APP_ENV

### GitHub Secrets (for CI/CD)

Add secrets in GitHub:
1. Settings → Secrets and variables → Actions
2. Add:
   - FIREBASE_SERVICE_ACCOUNT_JSON
   - RAILWAY_TOKEN (if using Railway)

---

## 📝 .gitignore Explained

Your `.gitignore` protects:

```gitignore
# Secrets (NEVER commit these!)
.env
*firebase*.json
firebase-key.json
serviceAccountKey.json

# Python
__pycache__/
*.pyc
venv/

# IDE
.vscode/
.idea/
.DS_Store

# Logs
*.log
```

---

## 🔄 Keeping Repository Updated

### Regular Updates

```bash
# 1. Make changes to code
# 2. Check what changed
git status

# 3. Add changes
git add .

# 4. Commit
git commit -m "Update: Description of changes"

# 5. Push
git push origin main
```

### Pull Latest Changes

```bash
# If working with team
git pull origin main
```

---

## 👥 Collaborating

### Add Collaborators

1. Go to: https://github.com/html-proof/Kiro-project/settings/access
2. Click "Add people"
3. Enter GitHub username
4. Choose permission level

### Clone Repository

Others can clone:
```bash
git clone https://github.com/html-proof/Kiro-project.git
cd Kiro-project
```

---

## 📚 Git Best Practices

### ✅ DO:

1. **Commit often** - Small, focused commits
2. **Write clear messages** - Describe what and why
3. **Pull before push** - Avoid conflicts
4. **Use branches** - For features and fixes
5. **Review before commit** - Check `git status`

### ❌ DON'T:

1. **Don't commit secrets** - Use .gitignore
2. **Don't commit large files** - Use Git LFS if needed
3. **Don't force push** - Unless you're sure
4. **Don't commit generated files** - Like __pycache__
5. **Don't commit .env** - Use .env.example instead

---

## 🎯 Quick Reference

```bash
# Setup
git init
git remote add origin https://github.com/html-proof/Kiro-project.git

# Daily workflow
git status
git add .
git commit -m "Message"
git push origin main

# Branching
git checkout -b feature-name
git checkout main
git merge feature-name

# Undo
git reset --soft HEAD~1  # Undo commit, keep changes
git reset --hard HEAD~1  # Undo commit, discard changes

# View
git log --oneline
git diff
git status
```

---

## 🔗 Useful Links

- **Your Repository:** https://github.com/html-proof/Kiro-project
- **Git Documentation:** https://git-scm.com/doc
- **GitHub Guides:** https://guides.github.com
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf

---

## ✅ Checklist Before First Push

- [ ] Git configured (email & username)
- [ ] .gitignore in place
- [ ] .env NOT in Git
- [ ] All code files added
- [ ] Documentation complete
- [ ] README.md updated
- [ ] Secrets removed from code
- [ ] Commit message written
- [ ] Ready to push!

---

**Your repository is ready to push! 🚀**

Use: `git-push.bat` (Windows) or `git-push.sh` (Linux/Mac)

Or run the manual commands above.
