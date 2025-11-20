/**
 * API service for connecting to Mini Outbreak Detector backend
 */

import { AnalyzeRequest, AnalysisResult } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Analyze disease data for a specific country
 */
export async function analyzeDisease(
  request: AnalyzeRequest
): Promise<AnalysisResult> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Analysis failed");
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

/**
 * Get list of available countries
 */
export async function getCountries(dataSource = "owid"): Promise<string[]> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/countries?data_source=${dataSource}`
    );

    if (!response.ok) {
      throw new Error("Failed to fetch countries");
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

/**
 * Get list of supported diseases
 */
export async function getDiseases(): Promise<string[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/diseases`);

    if (!response.ok) {
      throw new Error("Failed to fetch diseases");
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

/**
 * Health check
 */
export async function healthCheck(): Promise<{ status: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return await response.json();
  } catch (error) {
    console.error("Health check failed:", error);
    throw error;
  }
}
