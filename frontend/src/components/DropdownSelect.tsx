import { ChevronDown } from "lucide-react";

interface DropdownSelectProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: string[];
  placeholder?: string;
}

export default function DropdownSelect({
  label,
  value,
  onChange,
  options,
  placeholder = "Select an option",
}: DropdownSelectProps) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-white font-medium text-lg">{label}</label>
      <div className="relative">
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="input-base appearance-none cursor-pointer pr-10"
        >
          <option value="" disabled>
            {placeholder}
          </option>
          {options.map((option) => (
            <option key={option} value={option} className="bg-navy-700">
              {option}
            </option>
          ))}
        </select>
        <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
      </div>
    </div>
  );
}
