# Integration Guide: Connecting Frontend to Backend

This guide shows you how to connect the Next.js frontend to your FastAPI backend.

## Quick Start (Both Running Locally)

### Step 1: Start the Backend

```bash
# From the project root
cd /path/to/outbreaks

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start FastAPI server
python -m src.api.server
```

Backend will run at: `http://localhost:8000`

### Step 2: Start the Frontend

```bash
# Open a new terminal
cd /path/to/outbreaks/frontend

# Install dependencies (first time only)
npm install

# Start Next.js dev server
npm run dev
```

Frontend will run at: `http://localhost:3000`

### Step 3: Test the Connection

1. Open `http://localhost:3000`
2. Select a country and disease
3. Click "Analyze"

Currently, the frontend uses mock data. Follow the steps below to connect to the real backend.

---

## Connecting to Real Backend API

### Option 1: Quick Integration (Recommended for Testing)

Update the home page to use real API:

**File**: `frontend/src/app/page.tsx`

```typescript
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import PageContainer from "@/components/PageContainer";
import DropdownSelect from "@/components/DropdownSelect";
import PrimaryButton from "@/components/PrimaryButton";
import { getCountries, getDiseases, analyzeDisease } from "@/lib/api";

export default function Home() {
  const router = useRouter();
  const [country, setCountry] = useState("");
  const [disease, setDisease] = useState("");
  const [loading, setLoading] = useState(false);

  // Fetch from API instead of using static data
  const [countries, setCountries] = useState<string[]>([]);
  const [diseases, setDiseases] = useState<string[]>([]);

  useEffect(() => {
    async function fetchOptions() {
      try {
        const [countriesData, diseasesData] = await Promise.all([
          getCountries(),
          getDiseases(),
        ]);
        setCountries(countriesData);
        setDiseases(diseasesData);
      } catch (error) {
        console.error("Failed to fetch options:", error);
        // Fallback to mock data on error
        setCountries(["India", "United States", "Canada"]);
        setDiseases(["COVID-19", "Influenza"]);
      }
    }
    fetchOptions();
  }, []);

  const handleAnalyze = async () => {
    if (!country || !disease) return;

    setLoading(true);

    try {
      // Call real API
      const result = await analyzeDisease({
        country,
        disease,
        data_source: "owid",
      });

      // Store in sessionStorage to access on results page
      sessionStorage.setItem("analysisResult", JSON.stringify(result));

      // Navigate to results
      router.push(`/results?country=${country}&disease=${disease}`);
    } catch (error) {
      console.error("Analysis failed:", error);
      alert("Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageContainer className="min-h-[calc(100vh-8rem)]">
      <div className="text-center max-w-4xl mx-auto mb-16">
        <h1 className="text-hero text-white mb-6">
          Analyze Disease Trends & Detect Outbreak Signals
        </h1>
        <p className="text-subtitle text-slate-300 max-w-3xl mx-auto">
          Select a disease and country to view anomalies, forecasts, and
          AI-generated explanations.
          <br />
          Our system analyzes historical data to identify potential outbreak
          signals.
        </p>
      </div>

      <div className="max-w-4xl mx-auto">
        <div className="card p-12">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <DropdownSelect
              label="Country"
              value={country}
              onChange={setCountry}
              options={countries}
              placeholder="Select a country"
            />

            <DropdownSelect
              label="Disease"
              value={disease}
              onChange={setDisease}
              options={diseases}
              placeholder="Select a disease"
            />
          </div>

          <PrimaryButton
            onClick={handleAnalyze}
            loading={loading}
            disabled={!country || !disease}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </PrimaryButton>
        </div>
      </div>
    </PageContainer>
  );
}
```

**File**: `frontend/src/app/results/page.tsx`

```typescript
"use client";

import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import PageContainer from "@/components/PageContainer";
import CaseTrendChart from "@/components/CaseTrendChart";
import SummaryStatBlock from "@/components/SummaryStatBlock";
import AIExplanationPanel from "@/components/AIExplanationPanel";
import { AnalysisResult } from "@/types";
import {
  TrendingUp,
  AlertTriangle,
  Activity,
  Calendar,
} from "lucide-react";

function ResultsContent() {
  const searchParams = useSearchParams();
  const country = searchParams.get("country") || "Canada";
  const disease = searchParams.get("disease") || "Tuberculosis";

  const [data, setData] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get from sessionStorage (set on home page after API call)
    const storedResult = sessionStorage.getItem("analysisResult");
    if (storedResult) {
      setData(JSON.parse(storedResult));
      setLoading(false);
    }
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-slate-400">Loading results...</div>
      </div>
    );
  }

  return (
    <PageContainer>
      <div className="mb-8">
        <h1 className="text-section text-white mb-2">
          Analysis Results: {disease} in {country}
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2">
          <CaseTrendChart
            data={data.cleaned_data}
            anomalies={data.anomalies}
            forecast={data.forecast}
          />
        </div>

        <div className="space-y-4">
          <div className="card p-6">
            <h3 className="text-white text-xl font-semibold mb-6">
              Summary Statistics
            </h3>

            <div className="space-y-4">
              <SummaryStatBlock
                icon={TrendingUp}
                label="Recent Trend"
                value={
                  data.summary_stats.trend.charAt(0).toUpperCase() +
                  data.summary_stats.trend.slice(1)
                }
                variant={
                  data.summary_stats.trend === "increasing"
                    ? "warning"
                    : "default"
                }
              />

              <SummaryStatBlock
                icon={AlertTriangle}
                label="Anomalies Detected"
                value={data.anomaly_stats.total_anomalies}
                variant="danger"
              />

              <SummaryStatBlock
                icon={Activity}
                label="Forecast Direction"
                value={
                  data.forecast_stats.trend.charAt(0).toUpperCase() +
                  data.forecast_stats.trend.slice(1)
                }
                variant={
                  data.forecast_stats.trend === "increasing"
                    ? "success"
                    : "default"
                }
              />

              <SummaryStatBlock
                icon={Calendar}
                label="Last Updated"
                value={new Date().toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                  year: "numeric",
                })}
                variant="default"
              />
            </div>
          </div>
        </div>
      </div>

      <AIExplanationPanel explanation={data.ai_explanation} />
    </PageContainer>
  );
}

export default function ResultsPage() {
  return (
    <Suspense
      fallback={
        <PageContainer>
          <div className="flex items-center justify-center min-h-[400px]">
            <div className="text-slate-400">Loading results...</div>
          </div>
        </PageContainer>
      }
    >
      <ResultsContent />
    </Suspense>
  );
}
```

### Option 2: React Context (Recommended for Production)

For better state management, create a context:

**File**: `frontend/src/context/AnalysisContext.tsx`

```typescript
"use client";

import { createContext, useContext, useState, ReactNode } from "react";
import { AnalysisResult } from "@/types";

interface AnalysisContextType {
  result: AnalysisResult | null;
  setResult: (result: AnalysisResult) => void;
  countries: string[];
  setCountries: (countries: string[]) => void;
  diseases: string[];
  setDiseases: (diseases: string[]) => void;
}

const AnalysisContext = createContext<AnalysisContextType | null>(null);

export function AnalysisProvider({ children }: { children: ReactNode }) {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [countries, setCountries] = useState<string[]>([]);
  const [diseases, setDiseases] = useState<string[]>([]);

  return (
    <AnalysisContext.Provider
      value={{ result, setResult, countries, setCountries, diseases, setDiseases }}
    >
      {children}
    </AnalysisContext.Provider>
  );
}

export function useAnalysis() {
  const context = useContext(AnalysisContext);
  if (!context) {
    throw new Error("useAnalysis must be used within AnalysisProvider");
  }
  return context;
}
```

Then wrap your app in `layout.tsx`:

```typescript
import { AnalysisProvider } from "@/context/AnalysisContext";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen flex flex-col`}>
        <AnalysisProvider>
          <Navbar />
          <main className="flex-1">{children}</main>
          <Footer />
        </AnalysisProvider>
      </body>
    </html>
  );
}
```

---

## Environment Setup

### Development

Create `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production

Update environment variables in your deployment platform:

**Vercel:**
```bash
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

**Netlify:**
```bash
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

---

## Testing the Integration

### 1. Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy"}`

### 2. Test API Endpoints

**Get diseases:**
```bash
curl http://localhost:8000/api/diseases
```

**Get countries:**
```bash
curl http://localhost:8000/api/countries
```

**Analyze (with sample CSV):**
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

### 3. Test from Frontend

1. Open browser console (F12)
2. Navigate to `http://localhost:3000`
3. Check for CORS errors
4. Monitor network tab when clicking "Analyze"

---

## Common Issues & Solutions

### CORS Errors

**Problem:** `Access-Control-Allow-Origin` error

**Solution:** Update backend `src/api/server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Connection Refused

**Problem:** Frontend can't connect to backend

**Solution:**
1. Ensure backend is running: `http://localhost:8000`
2. Check `.env.local` has correct URL
3. Restart Next.js dev server after changing env vars

### Data Not Loading

**Problem:** API returns 404 or 500

**Solution:**
1. Check backend logs for errors
2. Verify data source exists (CSV file or OWID access)
3. Check request payload matches API schema

---

## Deployment Checklist

### Backend (FastAPI)

- [ ] Update CORS origins to include production frontend URL
- [ ] Set up environment variables
- [ ] Deploy to cloud (Heroku, AWS, GCP, etc.)
- [ ] Test `/health` endpoint
- [ ] Enable HTTPS

### Frontend (Next.js)

- [ ] Update `NEXT_PUBLIC_API_URL` to production backend
- [ ] Test build locally: `npm run build && npm start`
- [ ] Deploy to Vercel/Netlify
- [ ] Test all pages in production
- [ ] Enable caching

---

## Performance Tips

### Backend

1. **Add Redis caching** for repeated queries
2. **Implement rate limiting** to prevent abuse
3. **Use async endpoints** for long-running analyses
4. **Add database** for storing results

### Frontend

1. **Enable SWR or React Query** for data caching
2. **Lazy load heavy components** (charts)
3. **Implement loading states** everywhere
4. **Add error boundaries**

---

## Next Steps

1. **Add authentication** (JWT tokens)
2. **Implement user accounts** (save analyses)
3. **Add real-time updates** (WebSockets)
4. **Create email alerts** for high-risk detections
5. **Build admin dashboard**

---

Need help? Check the individual READMEs:
- Backend: `/README.md`
- Frontend: `/frontend/README.md`
