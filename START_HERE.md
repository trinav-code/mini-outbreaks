# 🚀 Quick Start Guide - Mini Outbreak Detector

Welcome! This guide will get both your backend AND frontend running in 5 minutes.

## What You Have

✅ **Backend (FastAPI)**: ML-powered outbreak detection API
✅ **Frontend (Next.js)**: Beautiful, pixel-perfect web interface

---

## Option 1: Quick Demo (No Setup Required)

### Test Frontend Only (With Mock Data)

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` - Works immediately with sample data!

---

## Option 2: Full Stack (Backend + Frontend)

### Step 1: Start Backend (Terminal 1)

```bash
# From project root
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python -m src.api.server
```

✅ Backend running at `http://localhost:8000`

### Step 2: Start Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend running at `http://localhost:3000`

### Step 3: Test

1. Open `http://localhost:3000`
2. Select "India" and "COVID-19"
3. Click "Analyze"
4. See results!

---

## Folder Structure

```
outbreaks/
│
├── 📁 Backend Files
│   ├── src/              ← Python code
│   ├── data/             ← Disease data
│   ├── requirements.txt  ← Python dependencies
│   └── README.md         ← Backend docs
│
├── 📁 frontend/          ← Next.js app
│   ├── src/
│   │   ├── app/          ← Pages
│   │   ├── components/   ← UI components
│   │   └── lib/          ← API service
│   ├── package.json
│   └── README.md         ← Frontend docs
│
└── 📄 Documentation
    ├── INTEGRATION_GUIDE.md   ← How to connect frontend to backend
    ├── FRONTEND_SUMMARY.md    ← What was built
    └── START_HERE.md          ← This file
```

---

## API Endpoints (Backend)

Once backend is running:

**Interactive Docs:**
- `http://localhost:8000/docs` - Swagger UI (try it out!)

**Endpoints:**
- `GET /api/diseases` - List diseases
- `GET /api/countries` - List countries
- `POST /api/analyze` - Analyze data

**Example API Call:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "country": "India",
    "disease": "COVID-19",
    "data_source": "csv",
    "csv_filename": "sample_disease_data.csv"
  }'
```

---

## Frontend Pages

**Home** (`/`)
- Hero section
- Country + Disease dropdowns
- Analyze button

**Results** (`/results`)
- Interactive chart
- Summary statistics
- AI explanation

---

## Connecting Frontend to Backend

### Currently: Frontend uses mock data

### To connect to real backend:

**1. Create `.env.local` in frontend folder:**
```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

**2. Follow integration guide:**
See `INTEGRATION_GUIDE.md` for detailed steps.

---

## Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Fix:**
```bash
pip install -r requirements.txt
```

### Frontend won't start

**Error:** `command not found: npm`

**Fix:** Install Node.js from https://nodejs.org

### CORS Error

**Error:** `Access-Control-Allow-Origin`

**Fix:** Backend already has CORS enabled. Make sure:
1. Backend is running
2. `.env.local` has correct URL

### Port Already in Use

**Error:** `Port 8000 already in use`

**Fix:**
```bash
# Kill process on port
# Mac/Linux:
lsof -ti:8000 | xargs kill

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## Development Workflow

### Making Changes to Backend

1. Edit Python files in `src/`
2. Server auto-reloads
3. Test at `http://localhost:8000/docs`

### Making Changes to Frontend

1. Edit files in `frontend/src/`
2. Changes appear instantly (hot reload)
3. View at `http://localhost:3000`

---

## Testing Checklist

### Backend

- [ ] `http://localhost:8000/health` returns `{"status":"healthy"}`
- [ ] `http://localhost:8000/docs` shows Swagger UI
- [ ] Can analyze sample data

### Frontend

- [ ] Home page loads
- [ ] Dropdowns populate
- [ ] Analyze button works
- [ ] Results page shows chart

---

## Project Highlights

**Backend:**
- ✅ Z-score anomaly detection
- ✅ Isolation Forest ML model
- ✅ Prophet forecasting
- ✅ AI-generated explanations
- ✅ REST API with FastAPI

**Frontend:**
- ✅ Pixel-perfect design
- ✅ Responsive layout
- ✅ Interactive charts
- ✅ TypeScript type safety
- ✅ Tailwind CSS styling

---

## Sample Data

**Included:** `data/raw/sample_disease_data.csv`
- 90 days of COVID-19 data for India
- Contains 3 anomaly spikes
- Ready to analyze

---

## Next Steps

### Beginner Path

1. ✅ Run frontend with mock data
2. ✅ Explore the UI
3. ✅ Run backend
4. ✅ Connect them together
5. ✅ Deploy both!

### Advanced Path

1. ✅ Add authentication
2. ✅ Connect to real OWID data
3. ✅ Add database for caching
4. ✅ Implement email alerts
5. ✅ Build admin dashboard

---

## Documentation Index

| File | Purpose |
|------|---------|
| `README.md` | Backend documentation |
| `frontend/README.md` | Frontend documentation |
| `INTEGRATION_GUIDE.md` | Connect frontend to backend |
| `FRONTEND_SUMMARY.md` | What was built in frontend |
| `START_HERE.md` | This file - quick start |

---

## Common Commands

### Backend

```bash
# Start server
python -m src.api.server

# Run in Jupyter
jupyter notebook notebooks/exploration.ipynb
```

### Frontend

```bash
# Development
npm run dev

# Production build
npm run build
npm start

# Install new package
npm install <package-name>
```

---

## Getting Help

### Check Logs

**Backend:**
- Look at terminal output
- Logs show in console

**Frontend:**
- Browser console (F12)
- Terminal output

### Documentation

- Backend: `README.md`
- Frontend: `frontend/README.md`
- Integration: `INTEGRATION_GUIDE.md`

---

## Deployment

### Free Options

**Backend:**
- Heroku (Free tier)
- Railway (Free tier)
- Render (Free tier)

**Frontend:**
- Vercel (Free for hobby)
- Netlify (Free for personal)
- GitHub Pages (Static only)

See individual READMEs for deployment instructions.

---

## Success!

If you see this, you're ready:

✅ Backend running at `:8000`
✅ Frontend running at `:3000`
✅ API docs accessible
✅ UI loads correctly
✅ Sample analysis works

**You now have a full-stack outbreak detection system!** 🎉

---

## Questions?

1. Check the documentation files
2. Review error messages carefully
3. Ensure all dependencies installed
4. Check that ports aren't in use

**Everything should "just work" out of the box!**

---

Made with ❤️ for public health.
Happy outbreak detecting! 🦠📊🤖
