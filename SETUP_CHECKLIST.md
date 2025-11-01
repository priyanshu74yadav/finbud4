# FinBud Setup Checklist

Use this as a quick reference while setting up your environment.

## ✅ Pre-Installation Checklist

### System Requirements

- [ ] Windows 10/11 (64-bit)
- [ ] At least 8GB RAM
- [ ] 10GB free disk space
- [ ] Internet connection

---

## 🔧 Installation Steps

### 1. Python Setup

```bash
# Download from: https://www.python.org/downloads/
# Version: 3.11 or higher
# ⚠️ IMPORTANT: Check "Add Python to PATH" during installation

# Verify:
python --version
pip --version
```

- [ ] Python installed
- [ ] Version 3.11+
- [ ] pip working

### 2. Node.js Setup

```bash
# Download from: https://nodejs.org/
# Choose: LTS version

# Verify:
```

- [ ] Node.js installed
- [ ] npm working

### 3. Git Setup

```bash
# Download from: https://git-scm.com/downloads

# Configure:
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Verify:
git --version
```

- [ ] Git installed
- [ ] Git configured

### 4. Create Project Folder

```bash
# Create and navigate to project
mkdir finbud
cd finbud
```

- [ ] Project folder created

### 5. Python Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Windows CMD)
venv\Scripts\activate

# Activate (Windows PowerShell)
venv\Scripts\Activate.ps1

# You should see (venv) in your prompt
```

- [ ] Virtual environment created
- [ ] Virtual environment activated

### 6. Install Python Packages

```bash
# Core framework
pip install pathway

# Document processing
pip install PyMuPDF python-docx openpyxl pytesseract pillow

# AI/ML
pip install openai langchain sentence-transformers transformers torch

# Web framework
pip install fastapi uvicorn python-multipart

# Utilities
pip install python-dotenv pydantic requests aiofiles

# Save requirements
pip freeze > requirements.txt
```

- [ ] Pathway installed
- [ ] Document libraries installed
- [ ] AI libraries installed
- [ ] Web framework installed
- [ ] requirements.txt created

### 7. OpenAI API Key

```bash
# 1. Go to: https://platform.openai.com/api-keys
# 2. Sign up / Log in
# 3. Create new API key
# 4. Copy the key (starts with sk-)

# Create .env file in project root
echo OPENAI_API_KEY=sk-your-key-here > .env
```

- [ ] OpenAI account created
- [ ] API key generated
- [ ] .env file created

### 8. Install uv (for Magic MCP)

```powershell
# Open PowerShell as Administrator
# Run:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify:
uv --version
uvx --version
```

- [ ] uv installed
- [ ] uvx working

### 9. Configure Magic MCP in Kiro

```json
// File: .kiro/settings/mcp.json
{
  "mcpServers": {
    "magic-mcp": {
      "command": "uvx",
      "args": ["21st-dev-magic-mcp"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

- [ ] mcp.json configured
- [ ] Kiro restarted / MCP reconnected

### 10. Install Office Development Tools (Optional)

```bash
# Install globally
npm install -g yo generator-office

# Verify:
yo --version
```

- [ ] Yeoman installed
- [ ] Office generator installed

### 11. Install Tesseract OCR (for scanned documents)

```bash
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install with default settings
# Note the installation path (e.g., C:\Program Files\Tesseract-OCR)

# Add to PATH or set in code:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

- [ ] Tesseract installed
- [ ] Path configured

---

## 🧪 Verification Tests

### Test Python Environment

```bash
# Activate venv first!
python -c "import pathway; print('Pathway OK')"
python -c "import fitz; print('PyMuPDF OK')"
python -c "import docx; print('python-docx OK')"
python -c "import openpyxl; print('openpyxl OK')"
python -c "import openai; print('OpenAI OK')"
python -c "import fastapi; print('FastAPI OK')"
```

- [ ] All imports successful

### Test OpenAI API

```python
# test_openai.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Say 'API working!'"}]
)
print(response.choices[0].message.content)
```

```bash
python test_openai.py
```

- [ ] OpenAI API working

### Test Magic MCP

```bash
# In Kiro, open chat and type:
# "Generate a simple React button component"
# Should see Magic MCP respond with code
```

- [ ] Magic MCP responding

---

## 📁 Project Structure Setup

```bash
# Create folder structure
mkdir backend
mkdir backend\ingestion
mkdir backend\indexing
mkdir backend\llm
mkdir backend\api
mkdir backend\data
mkdir backend\data\documents
mkdir backend\data\synonyms

mkdir frontend
mkdir office-addin
mkdir tests
mkdir docs

# Create initial files
type nul > backend\__init__.py
type nul > backend\ingestion\__init__.py
type nul > backend\indexing\__init__.py
type nul > backend\llm\__init__.py
type nul > backend\api\__init__.py

# Create .gitignore
echo venv/ > .gitignore
echo .env >> .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
echo node_modules/ >> .gitignore
echo .DS_Store >> .gitignore
echo *.log >> .gitignore

# Initialize git
git init
git add .
git commit -m "Initial project structure"
```

- [ ] Folders created
- [ ] **init**.py files created
- [ ] .gitignore created
- [ ] Git initialized

---

## 🎯 Quick Start Commands

### Start Backend Development

```bash
# Activate venv
venv\Scripts\activate

# Run FastAPI server
cd backend
uvicorn api.main:app --reload
```

### Start Frontend Development

```bash
# In new terminal
cd frontend
npm start
```

### Run Tests

```bash
# Activate venv
venv\Scripts\activate

# Run pytest
pytest tests/
```

---

## 🆘 Common Issues & Solutions

### Issue: "python not found"

**Solution:** Reinstall Python, ensure "Add to PATH" is checked

### Issue: "pip not found"

**Solution:** Use `python -m pip install` instead of `pip install`

### Issue: "venv\Scripts\activate not working"

**Solution:**

- CMD: Use `venv\Scripts\activate.bat`
- PowerShell: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` first

### Issue: "uvx not found"

**Solution:**

- Restart terminal after installing uv
- Check PATH includes uv installation directory

### Issue: "OpenAI API error"

**Solution:**

- Verify API key in .env file
- Check you have credits in OpenAI account
- Ensure .env is in project root

### Issue: "Import pathway fails"

**Solution:**

- Ensure venv is activated
- Reinstall: `pip install --upgrade pathway`

### Issue: "Magic MCP not responding"

**Solution:**

- Check mcp.json syntax
- Restart Kiro
- View MCP logs in Kiro's MCP panel

---

## 📞 Getting Help

If stuck:

1. Check error message carefully
2. Search error in documentation
3. Ask Kiro: "I'm getting error X, how do I fix it?"
4. Check GitHub issues for the specific library

---

## ✨ You're Ready!

Once all checkboxes are complete, you're ready to start building FinBud!

**Next step:** Open `EXECUTION_PLAN.md` and begin Phase 1: Project Structure
