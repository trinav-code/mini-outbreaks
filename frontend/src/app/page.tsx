"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import PageContainer from "@/components/PageContainer";
import DropdownSelect from "@/components/DropdownSelect";
import PrimaryButton from "@/components/PrimaryButton";
import { COUNTRIES, DISEASES } from "@/lib/sampleData";

export default function Home() {
  const router = useRouter();
  const [country, setCountry] = useState("");
  const [disease, setDisease] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!country || !disease) return;

    setLoading(true);

    // Simulate API call delay
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Navigate to results page with query params
    router.push(`/results?country=${country}&disease=${disease}`);
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
        </div>
      </div>
    </PageContainer>
  );
}
