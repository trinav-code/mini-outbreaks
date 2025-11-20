# 📤 Upload to GitHub - Step by Step Guide

This guide will help you upload your Mini Outbreak Detector to GitHub.

## Prerequisites

- [ ] GitHub account (create free at https://github.com/signup)
- [ ] Git installed on your computer

### Check if Git is installed:

```bash
git --version
```

If you see a version number (like `git version 2.x.x`), you're good!

If not, install Git:
- **Mac**: `brew install git` or download from https://git-scm.com
- **Windows**: Download from https://git-scm.com
- **Linux**: `sudo apt-get install git`

---

## Step 1: Create GitHub Repository

### Option A: Using GitHub Website (Easier)

1. Go to https://github.com
2. Click the **"+"** button (top right)
3. Click **"New repository"**
4. Fill in:
   - **Repository name**: `mini-outbreak-detector`
   - **Description**: `ML-powered disease outbreak detection system with Next.js frontend`
   - **Visibility**: Choose **Public** or **Private**
   - ⚠️ **DO NOT** check "Initialize with README" (we already have one)
   - ⚠️ **DO NOT** add .gitignore or license yet
5. Click **"Create repository"**

✅ Keep this page open - you'll need the URL!

---

## Step 2: Prepare Your Project

### Navigate to your project folder:

```bash
cd /Users/trinav/personal/outbreaks
```

### Make sure you're in the right place:

```bash
pwd
```

Should show: `/Users/trinav/personal/outbreaks`

---

## Step 3: Initialize Git

```bash
git init
```

You should see: `Initialized empty Git repository`

---

## Step 4: Add All Files

```bash
git add .
```

This stages all your files for commit.

### Check what will be committed:

```bash
git status
```

You should see a list of files in green. If you see files you DON'T want (like `node_modules/`, `venv/`, `__pycache__/`), they'll be ignored by your .gitignore files.

---

## Step 5: Make Your First Commit

```bash
git commit -m "Initial commit: Mini Outbreak Detector with backend and frontend"
```

✅ This creates a snapshot of your project!

---

## Step 6: Connect to GitHub

Copy the commands from your GitHub repository page. They look like this:

```bash
git remote add origin https://github.com/YOUR-USERNAME/mini-outbreak-detector.git
git branch -M main
git push -u origin main
```

**Replace `YOUR-USERNAME` with your actual GitHub username!**

### Example:

```bash
git remote add origin https://github.com/johndoe/mini-outbreak-detector.git
git branch -M main
git push -u origin main
```

---

## Step 7: Enter GitHub Credentials

When prompted:

**Username**: Your GitHub username
**Password**: Your Personal Access Token (NOT your GitHub password)

### Don't have a Personal Access Token?

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `Mini Outbreak Detector`
4. Select scopes:
   - ✅ `repo` (all repo permissions)
5. Click **"Generate token"**
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this as your password when pushing

---

## Step 8: Verify Upload

Go to your GitHub repository page:

`https://github.com/YOUR-USERNAME/mini-outbreak-detector`

You should see all your files! 🎉

---

## Troubleshooting

### Problem: "fatal: not a git repository"

**Solution**: Make sure you ran `git init` first

### Problem: "src refspec main does not match any"

**Solution**: Make sure you made a commit first with `git commit`

### Problem: "remote origin already exists"

**Solution**: Remove it and re-add:
```bash
git remote remove origin
git remote add origin YOUR-GITHUB-URL
```

### Problem: "Permission denied"

**Solution**: Use a Personal Access Token instead of password (see Step 7)

---

## Future Updates (After Initial Upload)

When you make changes to your code:

```bash
# 1. Check what changed
git status

# 2. Add changed files
git add .

# 3. Commit with a message
git commit -m "Description of what you changed"

# 4. Push to GitHub
git push
```

### Example workflow:

```bash
# Made changes to frontend
git add frontend/
git commit -m "Updated chart colors"
git push

# Made changes to backend
git add src/
git commit -m "Fixed anomaly detection bug"
git push
```

---

## Useful Git Commands

```bash
# See status
git status

# See commit history
git log

# See what changed
git diff

# Undo changes (before commit)
git checkout -- filename

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

## Add a Nice README Header

Make your GitHub page look professional! Add this to the top of your `README.md`:

```markdown
# 🦠 Mini Outbreak Detector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)

> ML-powered infectious disease outbreak detection and forecasting system

[Live Demo](https://your-demo-url.com) | [Documentation](./INTEGRATION_GUIDE.md) | [Report Bug](https://github.com/YOUR-USERNAME/mini-outbreak-detector/issues)

---
```

Then commit and push:

```bash
git add README.md
git commit -m "Add header badges to README"
git push
```

---

## Protect Sensitive Files

Make sure these are in your `.gitignore`:

```
# Python
venv/
__pycache__/
*.pyc
.env

# Node.js
node_modules/
.next/
.env.local

# Data (optional - keep raw sample data)
data/processed/*.csv
!data/raw/sample_*.csv
```

The `.gitignore` files are already set up correctly!

---

## Add Topics to Your Repo

On GitHub:
1. Go to your repository
2. Click ⚙️ next to "About"
3. Add topics:
   - `machine-learning`
   - `disease-detection`
   - `fastapi`
   - `nextjs`
   - `outbreak-detection`
   - `public-health`
   - `data-science`
   - `typescript`
   - `tailwindcss`

---

## Share Your Work!

### Add to your GitHub profile:

1. Go to https://github.com/YOUR-USERNAME
2. Click "Edit profile"
3. Pin this repository (star icon on repo page)

### Share the link:

```
https://github.com/YOUR-USERNAME/mini-outbreak-detector
```

### Add screenshots:

Create a `screenshots/` folder and add images:

```bash
mkdir screenshots
# Add your Figma screenshots here
git add screenshots/
git commit -m "Add project screenshots"
git push
```

Update README to show them:

```markdown
## Screenshots

![Home Page](./screenshots/home.png)
![Results](./screenshots/results.png)
```

---

## Complete Checklist

- [ ] Created GitHub account
- [ ] Installed Git
- [ ] Created new repository on GitHub
- [ ] Initialized git locally (`git init`)
- [ ] Added files (`git add .`)
- [ ] Made first commit (`git commit`)
- [ ] Connected to GitHub (`git remote add`)
- [ ] Pushed to GitHub (`git push`)
- [ ] Verified files appear on GitHub
- [ ] Added topics/tags
- [ ] Added screenshots (optional)
- [ ] Pinned to profile (optional)

---

## Next Steps

After uploading:

1. ✅ Add a license (MIT recommended)
2. ✅ Add a CONTRIBUTING.md file
3. ✅ Set up GitHub Pages for docs
4. ✅ Add GitHub Actions for CI/CD
5. ✅ Create releases/tags

---

## Need Help?

- GitHub Docs: https://docs.github.com
- Git Basics: https://git-scm.com/book/en/v2

---

**You're ready to upload! Start with Step 1.** 🚀
