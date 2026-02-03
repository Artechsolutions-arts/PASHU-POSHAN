"use client"

import { ForecastChart } from "../charts/forecast-chart"
import { TrendingUp, AlertCircle, CheckCircle } from "lucide-react"

export function PredictView() {
  const predictions = [
    { month: "Mar 2026", supply: 24.5, demand: 31.2, gap: -6.7 },
    { month: "Apr 2026", supply: 22.8, demand: 32.1, gap: -9.3 },
    { month: "May 2026", supply: 28.4, demand: 30.8, gap: -2.4 },
    { month: "Jun 2026", supply: 35.2, demand: 29.5, gap: 5.7 },
    { month: "Jul 2026", supply: 38.1, demand: 28.9, gap: 9.2 },
    { month: "Aug 2026", supply: 36.4, demand: 30.2, gap: 6.2 },
  ]
  
  return (
    <div className="space-y-8">
      {/* Hero Banner */}
      <div className="bg-indigo-900 text-white p-8 rounded-2xl shadow-xl relative overflow-hidden">
        <div className="relative z-10">
          <h4 className="text-xl font-bold mb-2">6-Month Fodder Forecast</h4>
          <p className="text-indigo-200 text-sm max-w-xl">
            Our system has analyzed current farming cycles and animal population trends to 
            predict fodder availability. Monthly projections show a manageable gap if current 
            surplus is reallocated.
          </p>
        </div>
        <div className="absolute right-0 top-0 opacity-10 transform translate-x-1/4 -translate-y-1/4">
          <TrendingUp className="w-64 h-64" />
        </div>
      </div>
      
      {/* Forecast Chart */}
      <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <h4 className="text-sm font-bold text-slate-800 uppercase">
            Future Trends Projection
          </h4>
          <div className="flex gap-6 text-[10px] font-bold text-slate-400">
            <span className="flex items-center gap-2">
              <span className="w-8 h-1 bg-blue-500 rounded" />
              PREDICTED SUPPLY
            </span>
            <span className="flex items-center gap-2">
              <span className="w-8 h-1 bg-indigo-300 rounded border-dashed" />
              PREDICTED DEMAND
            </span>
          </div>
        </div>
        <ForecastChart data={predictions} />
      </div>
      
      {/* Monthly Breakdown */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {predictions.map((pred) => (
          <div
            key={pred.month}
            className={`p-4 rounded-xl border shadow-sm ${
              pred.gap >= 0 
                ? "bg-emerald-50 border-emerald-200" 
                : "bg-rose-50 border-rose-200"
            }`}
          >
            <p className="text-[10px] font-bold text-slate-500 uppercase mb-2">
              {pred.month}
            </p>
            <div className="flex items-center gap-2 mb-2">
              {pred.gap >= 0 ? (
                <CheckCircle className="h-4 w-4 text-emerald-600" />
              ) : (
                <AlertCircle className="h-4 w-4 text-rose-600" />
              )}
              <span className={`text-lg font-bold ${
                pred.gap >= 0 ? "text-emerald-700" : "text-rose-700"
              }`}>
                {pred.gap >= 0 ? "+" : ""}{pred.gap.toFixed(1)}M
              </span>
            </div>
            <div className="text-[9px] text-slate-500 space-y-0.5">
              <p>Supply: {pred.supply}M T</p>
              <p>Demand: {pred.demand}M T</p>
            </div>
          </div>
        ))}
      </div>
      
      {/* Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h4 className="font-bold text-slate-800 mb-4">Key Insights</h4>
          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5 flex-shrink-0" />
              <p className="text-sm text-slate-600">
                <strong>Peak deficit expected in April 2026</strong> - Early harvest delays combined with 
                increased livestock population will create the largest gap.
              </p>
            </li>
            <li className="flex items-start gap-3">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 flex-shrink-0" />
              <p className="text-sm text-slate-600">
                <strong>Recovery starts from June 2026</strong> - Kharif season harvests will significantly 
                boost supply levels across all districts.
              </p>
            </li>
            <li className="flex items-start gap-3">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 flex-shrink-0" />
              <p className="text-sm text-slate-600">
                <strong>Recommended buffer stock: 8.5M tons</strong> - To bridge the projected gap during 
                lean months effectively.
              </p>
            </li>
          </ul>
        </div>
        
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h4 className="font-bold text-slate-800 mb-4">Recommended Actions</h4>
          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <span className="w-5 h-5 rounded bg-blue-100 text-blue-600 flex items-center justify-center text-[10px] font-bold flex-shrink-0">
                1
              </span>
              <p className="text-sm text-slate-600">
                Begin surplus reallocation from West Godavari and Konaseema to deficit districts
              </p>
            </li>
            <li className="flex items-start gap-3">
              <span className="w-5 h-5 rounded bg-blue-100 text-blue-600 flex items-center justify-center text-[10px] font-bold flex-shrink-0">
                2
              </span>
              <p className="text-sm text-slate-600">
                Activate emergency fodder procurement contracts for March-April period
              </p>
            </li>
            <li className="flex items-start gap-3">
              <span className="w-5 h-5 rounded bg-blue-100 text-blue-600 flex items-center justify-center text-[10px] font-bold flex-shrink-0">
                3
              </span>
              <p className="text-sm text-slate-600">
                Increase silage production incentives in surplus-producing districts
              </p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
