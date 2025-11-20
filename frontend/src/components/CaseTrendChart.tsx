"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  ComposedChart,
} from "recharts";
import { DataPoint, Anomaly, ForecastPoint } from "@/types";

interface CaseTrendChartProps {
  data: DataPoint[];
  anomalies: Anomaly[];
  forecast: ForecastPoint[];
}

export default function CaseTrendChart({
  data,
  anomalies,
  forecast,
}: CaseTrendChartProps) {
  // Combine historical and forecast data
  const combinedData = [
    ...data.map((d) => ({
      date: d.date,
      cases: d.cases,
      type: "historical",
    })),
    ...forecast.map((f) => ({
      date: f.date,
      forecast: f.forecast,
      type: "forecast",
    })),
  ];

  // Map anomalies for scatter plot
  const anomalyData = anomalies.map((a) => ({
    date: a.date,
    cases: a.cases,
  }));

  return (
    <div className="card p-6">
      <h3 className="text-white text-xl font-semibold mb-6">
        Case Trend Over Time
      </h3>

      <div className="h-[400px]">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart
            data={combinedData}
            margin={{ top: 10, right: 30, left: 0, bottom: 20 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#334155"
              opacity={0.3}
            />
            <XAxis
              dataKey="date"
              stroke="#94A3B8"
              tick={{ fill: "#94A3B8", fontSize: 12 }}
              tickFormatter={(value) => {
                const date = new Date(value);
                return `${date.toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                })}`;
              }}
            />
            <YAxis
              stroke="#94A3B8"
              tick={{ fill: "#94A3B8", fontSize: 12 }}
              label={{
                value: "Cases",
                angle: -90,
                position: "insideLeft",
                fill: "#94A3B8",
              }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#1E293B",
                border: "1px solid #475569",
                borderRadius: "8px",
                color: "#E2E8F0",
              }}
              labelStyle={{ color: "#CBD5E1" }}
            />

            {/* Historical cases line */}
            <Line
              type="monotone"
              dataKey="cases"
              stroke="#10B981"
              strokeWidth={2}
              dot={false}
              name="Actual Cases"
              connectNulls
            />

            {/* Forecast line */}
            <Line
              type="monotone"
              dataKey="forecast"
              stroke="#10B981"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={false}
              name="Forecast"
              connectNulls
            />

            {/* Anomaly scatter */}
            <Scatter
              data={anomalyData}
              fill="#EF4444"
              shape="circle"
              name="Anomaly"
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-6 mt-6 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-8 h-0.5 bg-emerald"></div>
          <span className="text-slate-300">Actual Cases</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-8 h-0.5 bg-emerald border-dashed"></div>
          <span className="text-slate-300">Forecast</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-danger rounded-full"></div>
          <span className="text-slate-300">Anomaly</span>
        </div>
      </div>
    </div>
  );
}
