# Mini Outbreak Detector - Frontend

A pixel-perfect Next.js + Tailwind CSS frontend for the Mini Outbreak Detector system.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Charts**: Recharts
- **Icons**: Lucide React

## Quick Start

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Visit `http://localhost:3000`

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout with Navbar/Footer
│   │   ├── page.tsx            # Home page
│   │   ├── results/
│   │   │   └── page.tsx        # Results page
│   │   └── globals.css         # Global styles
│   │
│   ├── components/
│   │   ├── Navbar.tsx          # Top navigation
│   │   ├── Footer.tsx          # Footer with links
│   │   ├── PageContainer.tsx   # Page wrapper
│   │   ├── DropdownSelect.tsx  # Custom dropdown
│   │   ├── PrimaryButton.tsx   # CTA button
│   │   ├── CaseTrendChart.tsx  # Main chart component
│   │   ├── SummaryStatBlock.tsx # Stat card
│   │   └── AIExplanationPanel.tsx # AI explanation
│   │
│   ├── lib/
│   │   └── sampleData.ts       # Mock data for development
│   │
│   └── types/
│       └── index.ts            # TypeScript interfaces
│
├── tailwind.config.ts          # Tailwind configuration
└── package.json
```

## Design System

### Colors

```typescript
// Background
navy-900: #0F172A
navy-800: #1E293B
navy-700: #334155

// Text
slate-200: #E2E8F0 (body)
slate-300: #CBD5E1 (headings)
slate-400: #94A3B8 (muted)

// Accent
emerald: #10B981 (primary)

// Status
danger: #EF4444 (red)
warning: #F59E0B (orange)
success: #10B981 (green)
```

### Typography

- **Hero**: 3.5rem, font-semibold
- **Section**: 2.5rem, font-semibold
- **Subtitle**: 1.125rem, font-normal
- **Body**: 1rem

### Spacing

- Card padding: `p-12` (3rem)
- Section gaps: `gap-8` (2rem)
- Component gaps: `gap-4` (1rem)

### Border Radius

- Cards: `12px`
- Inputs: `8px`

## Connecting to Backend API

### 1. Create API Service

Create `src/lib/api.ts`:

```typescript
import { AnalyzeRequest, AnalysisResult } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function analyzeDisease(
  request: AnalyzeRequest
): Promise<AnalysisResult> {
  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error("Analysis failed");
  }

  return response.json();
}

export async function getCountries(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/countries`);
  return response.json();
}

export async function getDiseases(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/diseases`);
  return response.json();
}
```

### 2. Update Home Page

Replace the mock `handleAnalyze` in `src/app/page.tsx`:

```typescript
import { analyzeDisease } from "@/lib/api";

const handleAnalyze = async () => {
  if (!country || !disease) return;

  setLoading(true);

  try {
    const result = await analyzeDisease({
      country,
      disease,
      data_source: "owid",
    });

    // Store result in state or context
    // Then navigate to results
    router.push(`/results?country=${country}&disease=${disease}`);
  } catch (error) {
    console.error("Analysis failed:", error);
    // Show error to user
  } finally {
    setLoading(false);
  }
};
```

### 3. Update Results Page

Replace `SAMPLE_ANALYSIS` with real data:

```typescript
import { analyzeDisease } from "@/lib/api";
import { useEffect, useState } from "react";

const [data, setData] = useState<AnalysisResult | null>(null);

useEffect(() => {
  async function fetchData() {
    const result = await analyzeDisease({
      country,
      disease,
      data_source: "owid",
    });
    setData(result);
  }
  fetchData();
}, [country, disease]);
```

### 4. Environment Variables

Create `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production:

```bash
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

### 5. Enable CORS on Backend

Your FastAPI backend already has CORS enabled. Ensure it allows your frontend domain:

```python
# In src/api/server.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## State Management (Optional)

For larger apps, consider adding:

### React Context

```typescript
// src/context/AnalysisContext.tsx
"use client";

import { createContext, useContext, useState } from "react";
import { AnalysisResult } from "@/types";

const AnalysisContext = createContext<{
  result: AnalysisResult | null;
  setResult: (result: AnalysisResult) => void;
} | null>(null);

export function AnalysisProvider({ children }: { children: React.ReactNode }) {
  const [result, setResult] = useState<AnalysisResult | null>(null);

  return (
    <AnalysisContext.Provider value={{ result, setResult }}>
      {children}
    </AnalysisContext.Provider>
  );
}

export const useAnalysis = () => {
  const context = useContext(AnalysisContext);
  if (!context) throw new Error("useAnalysis must be used within AnalysisProvider");
  return context;
};
```

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Docker

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

### Environment Variables in Production

Set these in your deployment platform:
- `NEXT_PUBLIC_API_URL`: Your backend API URL

## Customization

### Updating Colors

Edit `tailwind.config.ts`:

```typescript
colors: {
  emerald: {
    DEFAULT: "#YOUR_COLOR",
  },
}
```

### Adding Pages

Create new pages in `src/app/`:

```typescript
// src/app/about/page.tsx
export default function AboutPage() {
  return <div>About Page</div>;
}
```

### Custom Components

Follow the existing component patterns in `src/components/`.

## Development Tips

1. **Hot Reload**: Changes auto-refresh in dev mode
2. **Type Safety**: TypeScript catches errors before runtime
3. **Linting**: Run `npm run lint` to check code quality
4. **Tailwind IntelliSense**: Install VS Code extension for autocomplete

## Troubleshooting

### CORS Errors

Ensure your backend allows requests from `http://localhost:3000`.

### Chart Not Rendering

Check that `recharts` is installed: `npm install recharts`

### Styles Not Applying

1. Clear `.next` folder: `rm -rf .next`
2. Restart dev server

## Performance Optimization

### Image Optimization

Use Next.js `<Image>` component:

```typescript
import Image from "next/image";

<Image src="/logo.png" alt="Logo" width={200} height={50} />
```

### Code Splitting

Next.js automatically code-splits by route. For component-level splitting:

```typescript
import dynamic from "next/dynamic";

const HeavyChart = dynamic(() => import("@/components/HeavyChart"), {
  loading: () => <p>Loading...</p>,
});
```

### Caching

Add caching headers in `next.config.mjs`:

```javascript
async headers() {
  return [
    {
      source: "/api/:path*",
      headers: [
        { key: "Cache-Control", value: "public, max-age=3600" },
      ],
    },
  ];
}
```

## License

MIT

---

Built with Next.js, Tailwind CSS, and TypeScript.
