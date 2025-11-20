import { Github, BookOpen, Mail, HelpCircle } from "lucide-react";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-black border-t border-slate-800 mt-auto">
      <div className="container-custom">
        <div className="flex items-center justify-between h-16">
          {/* Copyright */}
          <p className="text-slate-400 text-sm">
            © 2025 Mini Outbreak Detector. Built for education and research.
          </p>

          {/* Links */}
          <div className="flex items-center gap-6">
            <Link
              href="https://github.com"
              target="_blank"
              className="flex items-center gap-2 text-slate-400 hover:text-emerald transition-colors"
            >
              <Github className="w-5 h-5" />
              <span className="text-sm">GitHub</span>
            </Link>
            <Link
              href="https://medium.com"
              target="_blank"
              className="flex items-center gap-2 text-slate-400 hover:text-emerald transition-colors"
            >
              <BookOpen className="w-5 h-5" />
              <span className="text-sm">Medium</span>
            </Link>
            <Link
              href="/contact"
              className="flex items-center gap-2 text-slate-400 hover:text-emerald transition-colors"
            >
              <Mail className="w-5 h-5" />
              <span className="text-sm">Contact</span>
            </Link>
            <button className="text-slate-400 hover:text-emerald transition-colors">
              <HelpCircle className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
}
