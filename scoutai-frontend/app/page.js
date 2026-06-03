"use client";

import React, { useState } from "react";
import {
  Building2,
  Globe,
  Search,
  Sparkles,
  Download,
  Copy,
  Check,
  FileText,
  Loader2
} from "lucide-react";
import remarkGfm from 'remark-gfm';
import ReactMarkdown from 'react-markdown';


export default function ScoutAIPage() {
  const [formData, setFormData] = useState({ companyName: "", domain: "" });
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState(null);

  // Simulated handle submit to trigger CrewAI backend later
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.companyName || !formData.domain) return;

    setLoading(true);
    setReport(null);
    setError(null);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/run_crew`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          startup: formData.companyName,
          domain: formData.domain,
        }),
      });

      const data = await res.json();

      if (res.status === 429) {
        setError("⚠️ AI engine is busy or daily limit reached. Please try again after some time.");
        return;
      }

      if (!res.ok) {
        setError("Something went wrong. Please try again.");
        return;
      }

      setReport(data.report_md);

    } catch (err) {
      setError(err.message || "An unexpected error occurred. Please try again.");
    } finally {
      setLoading(false);
    }


  };

  const handleCopy = () => {
    if (!report) return;
    navigator.clipboard.writeText(report);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500/30">
      {/* Background Glow Effect */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[500px] bg-gradient-to-b from-indigo-600/10 via-purple-600/5 to-transparent blur-3xl pointer-events-none z-0" />

      {/* Navbar */}
      <header className="relative border-b border-slate-800 bg-slate-950/80 backdrop-blur-md z-10">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-indigo-600 p-2 rounded-xl shadow-lg shadow-indigo-600/20">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-xl tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
              Scout<span className="text-indigo-500">AI</span>
            </span>
          </div>
          <div className="flex items-center gap-4 text-sm text-slate-400">
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              CrewAI Engine Active
            </span>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="relative max-w-6xl mx-auto px-4 py-12 grid grid-cols-1 lg:grid-cols-12 gap-8 z-10">

        {/* Left Column: Inputs */}
        <section className="lg:col-span-4 space-y-6">
          <div className="space-y-2">
            <h1 className="text-3xl font-extrabold tracking-tight text-white">
              Instant Intelligence.
            </h1>
            <p className="text-slate-400 text-sm leading-relaxed">
              Deploy specialized AI agents to scout your market domain, analyze financials, and break down competitor positioning.
            </p>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm shadow-xl">
            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Startup Name Input */}
              <div className="space-y-2">
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
                  Startup Name
                </label>
                <div className="relative">
                  <Building2 className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                  <input
                    type="text"
                    required
                    placeholder="e.g., EventLink"
                    value={formData.companyName}
                    onChange={(e) => setFormData({ ...formData, companyName: e.target.value })}
                    className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition text-slate-200 placeholder:text-slate-600"
                  />
                </div>
              </div>

              {/* Domain Input */}
              <div className="space-y-2">
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
                  Market Domain / Niche
                </label>
                <div className="relative">
                  <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                  <input
                    type="text"
                    required
                    placeholder="e.g., AI-driven career tech or ride-hailing safety"
                    value={formData.domain}
                    onChange={(e) => setFormData({ ...formData, domain: e.target.value })}
                    className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition text-slate-200 placeholder:text-slate-600"
                  />
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full relative group overflow-hidden bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-500 text-white font-medium text-sm py-3 px-4 rounded-xl transition flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/10"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Agents Scouring Web...</span>
                  </>
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    <span>Generate Competitive Report</span>
                  </>
                )}
              </button>
            </form>
          </div>
        </section>

        {/* Right Column: Output / Report Workspace */}
        {/* Right Column: Output / Report Workspace */}
        <section className="lg:col-span-8 min-w-0"> {/* min-w-0 prevents child elements from expanding the column width */}
          <div className="bg-slate-900/30 border border-slate-800 rounded-2xl h-[650px] flex flex-col overflow-hidden backdrop-blur-sm">

            {/* Report Header Controls */}
            <div className="border-b border-slate-800 bg-slate-900/40 px-6 py-4 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-indigo-400" />
                <span className="text-sm font-medium text-slate-300">Analysis Workspace</span>
              </div>
              {error && (
                <div className="text-red-400 bg-red-900/20 border border-red-500/30 
                  rounded-lg p-4 text-sm">
                  {error}
                </div>
              )}

              {report && (
                <div className="flex items-center gap-2">
                  <button
                    onClick={handleCopy}
                    className="p-1.5 text-slate-400 hover:text-white bg-slate-800/60 hover:bg-slate-800 border border-slate-700/50 rounded-lg transition text-xs flex items-center gap-1"
                    title="Copy Markdown"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    <span>{copied ? "Copied" : "Copy"}</span>
                  </button>
                </div>
              )}
            </div>

            {/* Content Area - Enforcing strict overflow containment and custom scrollbar */}
            <div className="p-6 flex-1 overflow-y-auto overflow-x-hidden custom-scrollbar">
              {loading && (
                <div className="h-full flex flex-col items-center justify-center text-center space-y-4 my-12">
                  <div className="relative">
                    <div className="w-12 h-12 rounded-full border-2 border-indigo-500/20 border-t-indigo-500 animate-spin" />
                    <Sparkles className="w-5 h-5 text-indigo-400 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-pulse" />
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm font-medium text-slate-300">Deploying CrewAI Agent Squad</p>
                    <p className="text-xs text-slate-500 max-w-xs mx-auto">
                      Researcher agent is identifying core actors. Financial Analyst agent is pulling funding parameters...
                    </p>
                  </div>
                </div>
              )}

              {!loading && !report && (
                <div className="h-full flex flex-col items-center justify-center text-center p-8 my-16 space-y-3">
                  <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-500">
                    <Search className="w-5 h-5" />
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm font-medium text-slate-400">No report generated yet</p>
                    <p className="text-xs text-slate-600 max-w-xs">
                      Enter your startup details on the left to let the agent workforce compile structured competitive intelligence.
                    </p>
                  </div>
                </div>
              )}

              {/* Rendered Markdown Output with Strict Word Wrap and Table Containment */}
              {!loading && report && (
                <div className="prose prose-invert max-w-none text-sm text-slate-300 leading-relaxed break-words
          prose-headings:text-white prose-headings:font-bold prose-headings:tracking-tight
          prose-h1:text-2xl prose-h1:border-b prose-h1:border-slate-800 prose-h1:pb-2 prose-h1:mt-2
          prose-h2:text-xl prose-h2:text-indigo-400 prose-h2:mt-6
          prose-h3:text-base prose-h3:text-slate-200
          prose-ul:list-disc prose-ul:pl-5 prose-li:my-1
          prose-strong:text-white prose-hr:border-slate-800 prose-hr:my-6
          [&_table]:w-full [&_table]:overflow-x-auto [&_table]:block [&_table]:my-4
          [&_th]:bg-slate-900 [&_th]:p-2 [&_th]:border [&_th]:border-slate-800
          [&_td]:p-2 [&_td]:border [&_td]:border-slate-800"
                >
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {report}
                  </ReactMarkdown>
                </div>
              )}
            </div>

          </div>
        </section>

      </main>
    </div>
  );
}