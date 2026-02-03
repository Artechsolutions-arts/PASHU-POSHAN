"use client"

import { gapAnalysisData, formatNumber } from "@/lib/data"
import { SupplyDemandChart } from "../charts/supply-demand-chart"
import { DistributionPieChart } from "../charts/distribution-pie-chart"

export function OverviewView() {
  const sortedData = [...gapAnalysisData].sort((a, b) => b.supply - a.supply)
  
  return (
    <div className="space-y-8">
      {/* Main Chart */}
      <div className="bg-white p-6 border border-slate-200 rounded-xl shadow-sm">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <h4 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
            District-wise Supply vs Demand Comparison
          </h4>
          <div className="flex gap-4 text-[10px] font-bold text-slate-400">
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 bg-amber-400 rounded-sm" />
              SUPPLY
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 bg-rose-500 rounded-sm" />
              DEMAND
            </span>
          </div>
        </div>
        <SupplyDemandChart data={sortedData.slice(0, 15)} />
      </div>
      
      {/* Table and Pie Chart Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* District Register Table */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="bg-slate-50 px-6 py-4 border-b border-slate-200">
            <h4 className="text-xs font-bold text-slate-800 uppercase">
              District Register
            </h4>
          </div>
          <div className="overflow-x-auto max-h-[400px] overflow-y-auto custom-scrollbar">
            <table className="w-full text-left text-[11px]">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-bold uppercase sticky top-0">
                <tr>
                  <th className="px-6 py-4">District</th>
                  <th className="px-6 py-4 text-right">Supply (T)</th>
                  <th className="px-6 py-4 text-right">Demand (T)</th>
                  <th className="px-6 py-4 text-right">Balance (T)</th>
                  <th className="px-6 py-4 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {sortedData.map((row) => (
                  <tr key={row.district} className="hover:bg-slate-50 transition">
                    <td className="px-6 py-3 font-semibold text-slate-700">
                      {row.district}
                    </td>
                    <td className="px-6 py-3 text-right text-slate-600">
                      {formatNumber(row.supply)}
                    </td>
                    <td className="px-6 py-3 text-right text-slate-600">
                      {formatNumber(row.demand)}
                    </td>
                    <td className={`px-6 py-3 text-right font-semibold ${row.balance >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                      {row.balance >= 0 ? '+' : ''}{formatNumber(row.balance)}
                    </td>
                    <td className="px-6 py-3 text-center">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                        row.status === "SURPLUS" 
                          ? "bg-emerald-100 text-emerald-700" 
                          : "bg-rose-100 text-rose-700"
                      }`}>
                        {row.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        
        {/* State Distribution Pie Chart */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h4 className="text-xs font-bold text-slate-800 uppercase mb-4">
            State Distribution
          </h4>
          <DistributionPieChart />
        </div>
      </div>
    </div>
  )
}
