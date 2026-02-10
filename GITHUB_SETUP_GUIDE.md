# GitHub Setup Guide for Musicly Backend

## Quick Push to GitHub

### Option 1: Using the Script (Easiest)

```bash
# Run the automated script
PUSH_TO_GITHUB.bat
```

The script will:
1. Initialize git repository (if needed)
2. Add GitHub remote
3. Check for sensitive files
4. Commit all changes
5. Push to GitHub

### Option 2: Manual Setup

#### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `musicly-backend`
3. Description: "Advanced music streaming backend with ML recommendations"
4. Choose Public or Private
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

#### Step 2: Initialize Git (if not already done)

```bash
cd musicly-backend
git init
```

#### Step 3: Add Remote

```bash
# Replace with your actual repository URL
git remote add origin https://github.com/YOUR_USERNAME/musicly-backend.git
```

#### Step 4: Add and Commit Files

```bash
# Add all files (sensitive files are excluded by .gitignore)
git add .

# Commit
git commit -m "feat: Complete Musicly backend with advanced features"
```

#### Step 5: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

## Authentication

### Using HTTPS (Recommended)

When pushing, you'll be prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your GitHub password)

#### Creating a Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "Musicly Backend"
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as your password when pushing

### Using SSH (Alternative)

If you prefer SSH:

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add SSH key to GitHub
# Copy the public key
cat ~/.ssh/id_ed25519.pub

# Add it to GitHub Settings → SSH and GPG keys → New SSH key

# Change remote to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/musicly-backend.git
```

## What Gets Pushed

### ✅ Included Files
- All Python source code
- Configuration files (requirements.txt, Procfile, etc.)
- Documentation (README, guides, etc.)
- Docker files
- Scripts (.bat, .sh files)

### ❌ Excluded Files (by .gitignore)
- `.env` (environment variables)
- `venv/` (virtual environment)
- `*firebase-adminsdk*.json` (Firebase credentials)
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)
- `.DS_Store`, `.idea/`, `.vscode/` (IDE files)

## Repository Structure on GitHub

```
musicly-backend/
├── .github/
│   └── workflows/          # GitHub Actions (optional)
├── app/
│   ├── firebase/
│   ├── firestore/
│   ├── redis/
│   ├── routes/
│   ├── services/
│   └── utils/
├── client-utils/
├── docs/
├── .gitignore
├── requirements.txt
├── Procfile
├── README.md
└── ... (other files)
```

## Setting Up GitHub Actions (Optional)

Create `.github/workflows/deploy.yml` for automatic deployment:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: musicly-backend
```

## Protecting Sensitive Data

### Before Pushing

1. **Check .gitignore**
   ```bash
   cat .gitignore
   ```

2. **Verify no sensitive files will be committed**
   ```bash
   git status
   ```

3. **Check what will be pushed**
   ```bash
   git diff --cached
   ```

### If You Accidentally Committed Secrets

```bash
# Remove file from git history
git rm --cached .env
git rm --cached app/*firebase-adminsdk*.json

# Commit the removal
git commit -m "Remove sensitive files"

# Force push (if already pushed)
git push -f origin main

# Then regenerate your secrets!
```

## Collaborating

### Adding Collaborators

1. Go to repository Settings → Collaborators
2. Click "Add people"
3. Enter GitHub username or email
4. Choose permission level

### Branch Protection

1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date

## Cloning on Another Machine

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/musicly-backend.git
cd musicly-backend

# Create .env file
cp .env.example .env
# Edit .env with your values

# Add Firebase credentials
# Download from Firebase Console and place in app/

# Install dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run the server
python start.py
```

## Troubleshooting

### Push Rejected

```bash
# Pull latest changes first
git pull origin main --rebase

# Then push
git push origin main
```

### Authentication Failed

- Make sure you're using a Personal Access Token, not your password
- Check token has correct permissions
- Token might have expired - generate a new one

### Large Files

If you have large files (>100MB):

```bash
# Use Git LFS
git lfs install
git lfs track "*.model"
git add .gitattributes
git commit -m "Add Git LFS"
```

### Wrong Remote URL

```bash
# Check current remote
git remote -v

# Change remote URL
git remote set-url origin https://github.com/YOUR_USERNAME/musicly-backend.git
```

## Best Practices

1. **Commit Often**: Make small, focused commits
2. **Write Good Messages**: Use conventional commits
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `refactor:` for code refactoring
3. **Use Branches**: Create feature branches for new work
4. **Pull Before Push**: Always pull latest changes before pushing
5. **Review Changes**: Use `git diff` before committing

## Example Workflow

```bash
# Create feature branch
git checkout -b feature/new-recommendation-algorithm

# Make changes
# ... edit files ...

# Check what changed
git status
git diff

# Add and commit
git add app/services/recommendation_service.py
git commit -m "feat: improve recommendation algorithm accuracy"

# Push feature branch
git push origin feature/new-recommendation-algorithm

# Create Pull Request on GitHub
# After review and approval, merge to main
```

## Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
