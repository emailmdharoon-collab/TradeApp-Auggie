# Quick Reference Guide - TradeApp-Auggie

## 🔗 Important Links

- **Repository:** https://github.com/emailmdharoon-collab/TradeApp-Auggie
- **CI/CD Dashboard:** https://github.com/emailmdharoon-collab/TradeApp-Auggie/actions
- **Issues:** https://github.com/emailmdharoon-collab/TradeApp-Auggie/issues
- **Commits:** https://github.com/emailmdharoon-collab/TradeApp-Auggie/commits/main

---

## 🚀 Common Git Commands

### Daily Workflow

```powershell
# Check status
git status

# Pull latest changes
git pull origin main

# Add changes
git add .

# Commit changes
git commit -m "Your descriptive message here"

# Push to GitHub
git push origin main
```

### Working with Branches

```powershell
# Create new branch
git checkout -b feature/your-feature-name

# Switch to existing branch
git checkout main

# List all branches
git branch -a

# Delete local branch
git branch -d feature/your-feature-name

# Push branch to GitHub
git push origin feature/your-feature-name
```

### Viewing History

```powershell
# View commit history
git log --oneline

# View changes in last commit
git show

# View changes not yet committed
git diff

# View staged changes
git diff --staged
```

---

## 📦 Environment Setup Commands

### First Time Setup (New Machine)

```powershell
# Clone repository
git clone https://github.com/emailmdharoon-collab/TradeApp-Auggie.git
cd TradeApp-Auggie

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
copy .env.template .env
# Edit .env with your API credentials

# Verify setup
python config.py
```

### Daily Development

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Update dependencies (if requirements.txt changed)
pip install -r requirements.txt --upgrade

# Run application (when ready)
streamlit run app.py
```

---

## 🧪 Testing Commands

### Module Testing

```powershell
# Test database module
python modules/database.py

# Test indicators module
python modules/indicators.py

# Test strategy module
python modules/strategy.py

# Test data fetcher
python modules/data_fetcher.py
```

### Running Tests (Future)

```powershell
# Run all tests
pytest

# Run specific test file
pytest tests/test_basic.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=modules tests/
```

---

## 📝 Dependency Management

### Adding New Dependencies

```powershell
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Or manually add to requirements.txt (preferred)
# Then install
pip install -r requirements.txt
```

### Updating Dependencies

```powershell
# Update specific package
pip install --upgrade package-name

# Update all packages (careful!)
pip install --upgrade -r requirements.txt

# Check outdated packages
pip list --outdated
```

---

## 🔍 Checking CI/CD Status

### Via GitHub Web Interface

1. Go to: https://github.com/emailmdharoon-collab/TradeApp-Auggie/actions
2. See all workflow runs
3. Click on any run to see details
4. Green checkmark = passed, Red X = failed

### Via Git Command Line

```powershell
# View recent commits with status
git log --oneline --decorate

# The commit will show CI status on GitHub
```

---

## 🐛 Troubleshooting

### Virtual Environment Issues

```powershell
# Deactivate current environment
deactivate

# Delete and recreate venv
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Git Issues

```powershell
# Discard local changes
git restore .

# Unstage files
git restore --staged .

# Reset to last commit (careful!)
git reset --hard HEAD

# Pull with rebase (if conflicts)
git pull --rebase origin main
```

### Dependency Issues

```powershell
# Clear pip cache
pip cache purge

# Reinstall all dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## 📊 Project Status Checks

### Quick Health Check

```powershell
# Check Python version
python --version

# Check installed packages
pip list

# Check git status
git status

# Check remote repository
git remote -v

# Check current branch
git branch
```

### Verify Everything Works

```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Test imports
python -c "import streamlit; import pandas; import numpy; import fyers_apiv3; print('All imports successful!')"

# Test configuration
python config.py

# Test database
python modules/database.py
```

---

## 🎯 Development Workflow

### Feature Development

1. **Create feature branch**
   ```powershell
   git checkout -b feature/new-feature
   ```

2. **Make changes and test**
   ```powershell
   # Edit files
   python modules/your_module.py  # Test
   ```

3. **Commit changes**
   ```powershell
   git add .
   git commit -m "Add new feature: description"
   ```

4. **Push to GitHub**
   ```powershell
   git push origin feature/new-feature
   ```

5. **Create Pull Request on GitHub**
   - Go to repository
   - Click "Pull requests" → "New pull request"
   - Select your branch
   - Create PR

6. **Wait for CI to pass**
   - GitHub Actions will run automatically
   - Fix any issues if CI fails

7. **Merge to main**
   - Click "Merge pull request" on GitHub
   - Delete feature branch

---

## 🔐 Security Best Practices

### Never Commit These Files:
- ❌ `.env` (contains API credentials)
- ❌ `*.key`, `*.pem` (private keys)
- ❌ `credentials.json` (API credentials)
- ❌ Any file with passwords or secrets

### Always Check Before Committing:
```powershell
# Review what will be committed
git status
git diff

# Make sure .env is not staged
git status | Select-String ".env"
```

---

## 📚 Useful Resources

### Documentation
- **Python:** https://docs.python.org/3/
- **Streamlit:** https://docs.streamlit.io/
- **Pandas:** https://pandas.pydata.org/docs/
- **Fyers API:** https://myapi.fyers.in/docs/

### Git & GitHub
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf
- **GitHub Actions:** https://docs.github.com/en/actions

### Project Files
- `README.md` - Project overview
- `PROGRESS.md` - Development progress
- `DAY1_COMPLETION_SUMMARY.md` - Day 1 summary
- `GITHUB_ENHANCEMENTS_SUMMARY.md` - CI/CD setup details

---

## 💡 Tips

1. **Commit Often:** Small, frequent commits are better than large ones
2. **Descriptive Messages:** Write clear commit messages
3. **Test Before Push:** Always test your changes locally first
4. **Pull Before Push:** Always pull latest changes before pushing
5. **Use Branches:** Create feature branches for new work
6. **Check CI:** Always verify CI passes after pushing

---

**Last Updated:** 2025-09-30  
**Version:** 1.0

