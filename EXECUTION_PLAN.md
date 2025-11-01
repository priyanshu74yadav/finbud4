# FinBud: Complete Execution Plan & Setup Guide

## 📋 Overview
This guide will take you from zero to a working FinBud prototype in 48 hours. No prior knowledge of Pathway, MCP, or advanced Python required.

---

## 🎯 Phase 0: Environment Setup (Hours 0-2)

### Step 0.1: Install Python (30 minutes)

**What is Python?** The programming language we'll use for the backend.

1. Download Python 3.11+ from https://www.python.org/downloads/
2. During installation, CHECK "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```
   Should show: Python 3.11.x or higher

### Step 0.2: Install Node.js (20 minutes)

**What is Node.js?** JavaScript runtime needed for the React frontend and Office add-ins.

1. Download Node.js LTS from https://nodejs.org/
2. Install with default settings
3. Verify installation:
   ```bash
   node --version
   npm --version
   ```

### Step 0.3: Install Git (15 minutes)

**What is Git?** Version control to track code changes.

1. Download from https://git-scm.com/downloads
2. Install with default settings
3. Configure:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

### Step 0.4: Set Up Python Virtual Environment (15 minutes)

**What is a virtual environment?** Isolated space for Python packages to avoid conflicts.

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### Step 0.5: Install Pathway (20 minutes)

**What is Pathway?** Real-time data processing framework with streaming capabilities.

```bash
# Make sure venv is activated
pip install pathway

# Install additional dependencies
pip install pathway[all]
```

### Step 0.6: Install Python Libraries (20 minutes)

```bash
# Document processing
pip install PyMuPDF python-docx openpyxl pytesseract

# AI/ML libraries
pip install openai langchain sentence-transformers

# Web framework
pip install fastapi uvicorn python-multipart

# Utilities
pip install python-dotenv pydantic requests
```

### Step 0.7: Set Up OpenAI API Key (10 minutes)

**What is this?** Access to GPT-4 for AI reasoning.

1. Go to https://platform.openai.com/api-keys
2. Create account and generate API key
3. Create `.env` file in project root:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

### Step 0.8: Install 21st.dev Magic MCP (30 minutes)

**What is Magic MCP?** AI tool that generates React UI components from prompts.

1. Install uv (Python package manager):
   ```bash
   # Windows (PowerShell as Administrator)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Configure MCP in Kiro:
   - Your `.kiro/settings/mcp.json` should have:
   ```json
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

3. Restart Kiro or reconnect MCP servers from the MCP panel

### Step 0.9: Install Office Development Tools (Optional - 30 minutes)

**What is this?** Tools to build Excel/Word add-ins.

```bash
# Install Yeoman and Office generator
npm install -g yo generator-office
```

---

## 🏗️ Phase 1: Project Structure (Hours 2-3)

### Step 1.1: Create Project Folders

```
finbud/
├── backend/
│   ├── ingestion/          # Document parsers
│   ├── indexing/           # Pathway pipeline
│   ├── llm/                # GPT-4 integration
│   ├── api/                # FastAPI endpoints
│   └── data/
│       ├── documents/      # Uploaded docs
│       └── synonyms/       # Concept mappings
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Main pages
│   │   └── api/            # API calls
│   └── public/
├── office-addin/           # Excel/Word plugin
├── tests/                  # Unit tests
└── docs/                   # Documentation
```

### Step 1.2: Initialize Git Repository

```bash
git init
echo "venv/" > .gitignore
echo ".env" >> .gitignore
echo "node_modules/" >> .gitignore
echo "__pycache__/" >> .gitignore
git add .
git commit -m "Initial project structure"
```

---

## 🔧 Phase 2: Backend Development (Hours 3-18)

### Step 2.1: Document Ingestion Module (Hours 3-6)

**Goal:** Parse PDF, Word, Excel files into text.

**Files to create:**
- `backend/ingestion/pdf_parser.py`
- `backend/ingestion/word_parser.py`
- `backend/ingestion/excel_parser.py`
- `backend/ingestion/ocr_handler.py`

**Key concepts:**
- PyMuPDF extracts text from PDFs
- python-docx reads Word documents
- openpyxl handles Excel files
- Tesseract OCR for scanned images

**Test:** Upload a sample financial PDF and verify text extraction.

### Step 2.2: Synonym Database (Hours 6-8)

**Goal:** Store and manage financial term mappings.

**Files to create:**
- `backend/data/synonyms/financial_terms.json`
- `backend/synonyms/manager.py`

**Structure:**
```json
{
  "sales_tax": ["VAT", "GST", "Sales Tax", "Consumption Tax"],
  "revenue": ["Sales", "Gross Sales", "Total Revenue", "Turnover"],
  "profit": ["Net Income", "Earnings", "Bottom Line"]
}
```

**Test:** Add/update synonyms and verify they're saved.

### Step 2.3: Pathway Streaming Pipeline (Hours 8-12)

**Goal:** Build real-time index that updates when documents change.

**What is Pathway doing?**
- Watches for new documents
- Splits text into chunks
- Creates vector embeddings (numerical representations)
- Builds searchable index (vector + keyword search)
- Updates automatically when data changes

**Files to create:**
- `backend/indexing/pathway_pipeline.py`
- `backend/indexing/embeddings.py`
- `backend/indexing/hybrid_search.py`

**Key Pathway concepts:**
```python
import pathway as pw

# Define data source (watches folder)
documents = pw.io.fs.read(
    path="backend/data/documents/",
    format="binary",
    mode="streaming"
)

# Process documents
chunks = documents.select(
    text=pw.apply(extract_text, pw.this.data)
)

# Create embeddings
embedded = chunks.select(
    vector=pw.apply(embed_text, pw.this.text)
)

# Build index
index = embedded.build_index()
```

**Test:** Add a document, verify it appears in index within 200ms.

### Step 2.4: LLM Integration (Hours 12-16)

**Goal:** Use GPT-4 to answer queries with retrieved context.

**What happens in a query?**
1. User asks: "What is our Q3 revenue?"
2. Expand with synonyms: ["revenue", "sales", "turnover"]
3. Search index for relevant chunks
4. Send to GPT-4: "Based on these documents, answer..."
5. GPT-4 returns structured answer with sources

**Files to create:**
- `backend/llm/query_engine.py`
- `backend/llm/prompt_templates.py`
- `backend/llm/response_parser.py`

**Prompt template example:**
```
You are a financial analyst assistant. Based on the following documents:

{retrieved_chunks}

Answer this question: {user_query}

Use these synonym mappings: {synonyms}

Provide:
1. Direct answer in standardized terms
2. Source citations [doc_id, page]
3. Confidence level
```

**Test:** Query "sales tax" and verify it finds "VAT" documents.

### Step 2.5: FastAPI Backend (Hours 16-18)

**Goal:** Create REST API for frontend to call.

**Endpoints needed:**
- POST `/query` - Submit question, get answer
- GET `/synonyms` - List all term mappings
- POST `/synonyms` - Add/update mapping
- POST `/upload` - Upload document
- GET `/documents` - List uploaded docs

**Files to create:**
- `backend/api/main.py`
- `backend/api/routes.py`
- `backend/api/models.py`

**Test:** Use Postman or curl to test each endpoint.

---

## 🎨 Phase 3: Frontend Development (Hours 18-32)

### Step 3.1: React App Setup (Hours 18-20)

**What is React?** JavaScript library for building user interfaces.

```bash
cd frontend
npx create-react-app . --template typescript
npm install axios react-query @radix-ui/react-dialog tailwindcss
```

### Step 3.2: Configure Tailwind CSS (Hours 20-21)

**What is Tailwind?** Utility-first CSS framework for styling.

```bash
npx tailwindcss init -p
```

Configure `tailwind.config.js` for 21st.dev components.

### Step 3.3: Use Magic MCP to Generate Components (Hours 21-26)

**How to use Magic MCP in Kiro:**

1. Open Kiro chat
2. Type prompts like:
   - "Create a query input component with submit button"
   - "Generate a data table for displaying financial results"
   - "Build a synonym editor form with add/delete"

3. Magic MCP will generate React code
4. Copy into your `frontend/src/components/` folder

**Components needed:**
- `QueryPanel.tsx` - Input box for questions
- `ResultsTable.tsx` - Display answers with sources
- `SynonymManager.tsx` - Edit term mappings
- `DocumentUploader.tsx` - Upload files
- `ExportButton.tsx` - Download results

**Test:** Run `npm start` and verify UI loads.

### Step 3.4: Connect Frontend to Backend (Hours 26-28)

**Files to create:**
- `frontend/src/api/client.ts` - API calls
- `frontend/src/hooks/useQuery.ts` - React hooks

```typescript
// Example API call
export async function submitQuery(question: string) {
  const response = await fetch('http://localhost:8000/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  return response.json();
}
```

**Test:** Submit query from UI, verify answer appears.

### Step 3.5: Polish UI (Hours 28-32)

- Add loading states
- Error handling
- Responsive design
- Export functionality (CSV/Excel)

---

## 📊 Phase 4: Office Add-in (Hours 32-38)

### Step 4.1: Generate Add-in Project (Hours 32-33)

```bash
cd office-addin
yo office
```

Choose:
- Project type: Excel Add-in
- Script type: JavaScript
- Name: FinBud

### Step 4.2: Build Taskpane UI (Hours 33-36)

**What is a taskpane?** Side panel in Excel/Word where your UI appears.

Copy your web UI components into the add-in:
- Query input
- Results display
- Insert into spreadsheet button

**Files to modify:**
- `office-addin/src/taskpane/taskpane.html`
- `office-addin/src/taskpane/taskpane.js`

### Step 4.3: Excel Integration (Hours 36-38)

**Key Office.js APIs:**

```javascript
// Write to Excel
Excel.run(async (context) => {
  const sheet = context.workbook.worksheets.getActiveWorksheet();
  const range = sheet.getRange("A1:C10");
  range.values = resultsData;
  await context.sync();
});
```

**Test:** Sideload add-in in Excel, submit query, verify data insertion.

---

## 🧪 Phase 5: Integration & Testing (Hours 38-46)

### Step 5.1: End-to-End Testing (Hours 38-42)

**Test scenarios:**
1. Upload financial PDF → Verify indexed
2. Query "revenue" → Get results with sources
3. Add synonym "Turnover" = "Revenue" → Query again, verify change
4. Export results to CSV → Verify format
5. Use Excel add-in → Verify data insertion

### Step 5.2: Performance Optimization (Hours 42-44)

- Measure query latency (target: <2 seconds)
- Optimize chunk sizes
- Cache embeddings
- Add loading indicators

### Step 5.3: Bug Fixes (Hours 44-46)

- Handle edge cases (empty queries, no results)
- Fix UI glitches
- Improve error messages

---

## 🚀 Phase 6: Deployment & Documentation (Hours 46-48)

### Step 6.1: Containerize Backend (Hours 46-47)

Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
```

### Step 6.2: Documentation (Hours 47-48)

Create:
- `README.md` - Setup instructions
- `API_DOCS.md` - Endpoint documentation
- `USER_GUIDE.md` - How to use FinBud

### Step 6.3: Demo Preparation

Prepare demo showing:
1. Live query with real-time results
2. Synonym editing with immediate effect
3. Excel add-in usage
4. Export functionality

---

## 📚 Key Concepts Explained

### What is RAG (Retrieval-Augmented Generation)?
Instead of relying only on LLM's training data, we:
1. Retrieve relevant documents from our index
2. Feed them to the LLM as context
3. LLM generates answer based on actual data

### What is Hybrid Search?
Combines two search methods:
- **Vector search:** Finds semantically similar text (understands meaning)
- **BM25 (keyword search):** Finds exact term matches
- Together: More accurate results

### What is Streaming/Live Updates?
Traditional systems: Rebuild entire index when data changes
Pathway: Updates only changed parts in real-time (<200ms)

### What is MCP (Model Context Protocol)?
Standard way for AI tools to communicate. Magic MCP lets Kiro generate UI code.

---

## 🆘 Troubleshooting

### Python Issues
- "python not found" → Reinstall, check PATH
- "pip not found" → Use `python -m pip` instead
- Import errors → Activate venv first

### Pathway Issues
- Slow indexing → Reduce chunk size
- Memory errors → Process fewer documents at once
- Connection errors → Check Pathway version compatibility

### Frontend Issues
- "npm not found" → Reinstall Node.js
- Build errors → Delete node_modules, run `npm install` again
- CORS errors → Configure FastAPI CORS middleware

### MCP Issues
- Magic not responding → Restart Kiro, reconnect MCP
- uvx not found → Reinstall uv
- Generation errors → Simplify prompt, be more specific

---

## 📊 Progress Tracking

Use this checklist:

**Setup (Hours 0-2)**
- [ ] Python installed
- [ ] Node.js installed
- [ ] Virtual environment created
- [ ] Pathway installed
- [ ] OpenAI API key configured
- [ ] Magic MCP configured

**Backend (Hours 2-18)**
- [ ] Document parsers working
- [ ] Synonym database created
- [ ] Pathway pipeline running
- [ ] LLM integration complete
- [ ] FastAPI endpoints tested

**Frontend (Hours 18-32)**
- [ ] React app created
- [ ] UI components generated
- [ ] Connected to backend
- [ ] Export functionality working

**Office Add-in (Hours 32-38)**
- [ ] Add-in project created
- [ ] Taskpane UI built
- [ ] Excel integration working

**Testing (Hours 38-46)**
- [ ] End-to-end tests passing
- [ ] Performance optimized
- [ ] Bugs fixed

**Deployment (Hours 46-48)**
- [ ] Backend containerized
- [ ] Documentation complete
- [ ] Demo ready

---

## 🎯 Success Criteria

By hour 48, you should have:
1. ✅ Working web app where users can query financial terms
2. ✅ Real-time synonym updates reflected in queries
3. ✅ Excel add-in that inserts results into spreadsheets
4. ✅ Source citations for all answers
5. ✅ Export functionality (CSV/Excel)
6. ✅ Sub-2-second query responses
7. ✅ Documentation for setup and usage

---

## 📖 Learning Resources

- **Pathway:** https://pathway.com/developers/documentation
- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/learn
- **Office Add-ins:** https://learn.microsoft.com/en-us/office/dev/add-ins/
- **21st.dev:** https://21st.dev/docs

---

## 💡 Tips for Success

1. **Start simple:** Get basic version working before adding features
2. **Test frequently:** Don't wait until the end to test
3. **Use AI tools:** Let Kiro generate boilerplate code
4. **Ask for help:** Use Kiro chat when stuck
5. **Version control:** Commit after each working feature
6. **Take breaks:** 48 hours is intense, pace yourself

---

**Ready to start? Let's begin with Phase 0: Environment Setup!**
