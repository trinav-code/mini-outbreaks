import { ReactNode } from "react";
import { LucideIcon } from "lucide-react";

interface SummaryStatBlockProps {
  icon: LucideIcon;
  label: string;
  value: string | number;
  variant?: "default" | "danger" | "warning" | "success";
  iconBg?: string;
}

const variantColors = {
  default: "text-slate-300",
  danger: "text-danger",
  warning: "text-warning",
  success: "text-success",
};

const iconBgColors = {
  default: "bg-slate-700",
  danger: "bg-danger/10",
  warning: "bg-warning/10",
  success: "bg-success/10",
};

export default function SummaryStatBlock({
  icon: Icon,
  label,
  value,
  variant = "default",
}: SummaryStatBlockProps) {
  return (
    <div className="stat-card flex items-center gap-4">
      <div className={`p-3 rounded-lg ${iconBgColors[variant]}`}>
        <Icon className={`w-6 h-6 ${variantColors[variant]}`} />
      </div>
      <div className="flex flex-col">
        <span className="text-slate-400 text-sm">{label}</span>
        <span className={`text-xl font-semibold ${variantColors[variant]}`}>
          {value}
        </span>
      </div>
    </div>
  );
}
