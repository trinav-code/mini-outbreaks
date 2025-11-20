"use client";

import { useSearchParams } from "next/navigation";
import { Suspense, useState, useEffect } from "react";
import PageContainer from "@/components/PageContainer";
import CaseTrendChart from "@/components/CaseTrendChart";
import SummaryStatBlock from "@/components/SummaryStatBlock";
import AIExplanationPanel from "@/components/AIExplanationPanel";
import { SAMPLE_ANALYSIS } from "@/lib/sampleData";
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

  const [data, setData] = useState<typeof SAMPLE_ANALYSIS | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get from sessionStorage (set on home page after API call)
    const storedResult = sessionStorage.getItem("analysisResult");
    if (storedResult) {
      setData(JSON.parse(storedResult));
    } else {
      // Fallback to sample data if no API call was made
      setData(SAMPLE_ANALYSIS);
    }
    setLoading(false);
  }, []);

  if (loading || !data) {
    return (
      <PageContainer>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-slate-400">Loading results...</div>
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-section text-white mb-2">
          Analysis Results: {disease} in {country}
        </h1>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Chart - Takes up 2 columns */}
        <div className="lg:col-span-2">
          <CaseTrendChart
            data={data.cleaned_data}
            anomalies={data.anomalies}
            forecast={data.forecast}
          />
        </div>

        {/* Summary Statistics Sidebar */}
        <div className="space-y-4">
          <div className="card p-6">
            <h3 className="text-white text-xl font-semibold mb-6">
              Summary Statistics
            </h3>

            <div className="space-y-4">
              <SummaryStatBlock
                icon={TrendingUp}
                label="Recent Trend"
                value="Increasing"
                variant="warning"
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
                value="Upward"
                variant="success"
              />

              <SummaryStatBlock
                icon={Calendar}
                label="Last Updated"
                value="Nov 19, 2025"
                variant="default"
              />
            </div>
          </div>
        </div>
      </div>

      {/* AI Explanation */}
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
