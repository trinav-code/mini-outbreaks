import { Sparkles } from "lucide-react";
import { AIExplanation } from "@/types";

interface AIExplanationPanelProps {
  explanation: AIExplanation;
}

export default function AIExplanationPanel({ explanation }: AIExplanationPanelProps) {
  return (
    <div className="card p-8">
      <div className="flex items-center gap-3 mb-6">
        <Sparkles className="w-6 h-6 text-emerald" />
        <h3 className="text-white text-2xl font-semibold">AI Explanation</h3>
      </div>

      <div className="bg-navy-700/50 rounded-lg p-6 space-y-4">
        <p className="text-slate-200 leading-relaxed">
          {explanation.explanation}
        </p>
      </div>
    </div>
  );
}
