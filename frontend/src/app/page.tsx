"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import PageContainer from "@/components/PageContainer";
import DropdownSelect from "@/components/DropdownSelect";
import PrimaryButton from "@/components/PrimaryButton";
import { COUNTRIES, DISEASES } from "@/lib/sampleData";
import { analyzeDisease } from "@/lib/api";

export default function Home() {
  const router = useRouter();
  const [country, setCountry] = useState("");
  const [disease, setDisease] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!country || !disease) return;

    setLoading(true);
    setError("");

    try {
      // Call real backend API with live OWID data
      const result = await analyzeDisease({
        country,
        disease,
        data_source: "owid", // Uses real-time data from Our World in Data
      });

      // Store result for results page
      sessionStorage.setItem("analysisResult", JSON.stringify(result));

      // Navigate to results
      router.push(`/results?country=${country}&disease=${disease}`);
    } catch (err) {
      console.error("Analysis failed:", err);
      setError("Analysis failed. Make sure the backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageContainer className="min-h-[calc(100vh-8rem)]">
      {/* Hero Section */}
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

      {/* Analysis Form Card */}
      <div className="max-w-4xl mx-auto">
        <div className="card p-12">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            {/* Country Dropdown */}
            <DropdownSelect
              label="Country"
              value={country}
              onChange={setCountry}
              options={COUNTRIES}
              placeholder="Select a country"
            />

            {/* Disease Dropdown */}
            <DropdownSelect
              label="Disease"
              value={disease}
              onChange={setDisease}
              options={DISEASES}
              placeholder="Select a disease"
            />
          </div>

          {/* Analyze Button */}
          <PrimaryButton
            onClick={handleAnalyze}
            loading={loading}
            disabled={!country || !disease}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </PrimaryButton>

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-4 bg-danger/10 border border-danger/30 rounded-lg">
              <p className="text-danger text-sm">{error}</p>
            </div>
          )}
        </div>
      </div>
    </PageContainer>
  );
}
