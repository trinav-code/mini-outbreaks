import Link from "next/link";
import { Activity } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="bg-black border-b border-slate-800">
      <div className="container-custom">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <Activity className="w-6 h-6 text-emerald group-hover:scale-110 transition-transform" />
            <span className="text-white font-medium text-lg">
              Mini Outbreak Detector
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-8">
            <Link
              href="/"
              className="text-white hover:text-emerald transition-colors font-medium"
            >
              Home
            </Link>
            <Link
              href="/about"
              className="text-slate-400 hover:text-emerald transition-colors"
            >
              About
            </Link>
            <Link
              href="/documentation"
              className="text-slate-400 hover:text-emerald transition-colors"
            >
              Documentation
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
