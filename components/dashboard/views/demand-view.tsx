"use client"

import { gapAnalysisData, formatNumber, getDemandComposition } from "@/lib/data"
import { CompositionPieChart } from "../charts/composition-pie-chart"

export function DemandView() {
  const demandComposition = getDemandComposition()
  const topDemandDistricts = [...gapAnalysisData]
    .sort((a, b) => b.demand - a.demand)
    .slice(0, 15)
  
  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Livestock Consumption Pie */}
        <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm">
          <h4 className="text-sm font-bold text-slate-800 uppercase mb-6">
            Livestock Consumption Distribution
          </h4>
          <CompositionPieChart data={demandComposition} />
        </div>
        
        {/* Mandal-wise Demand Register */}
        <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm">
          <h4 className="text-sm font-bold text-slate-800 uppercase mb-6">
            District-wise Demand Register
          </h4>
          <div className="space-y-2 h-72 overflow-y-auto custom-scrollbar pr-2">
            {topDemandDistricts.map((district, idx) => (
              <div
                key={district.district}
                className="flex items-center justify-between p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition"
              >
                <div className="flex items-center gap-3">
                  <span className="w-6 h-6 flex items-center justify-center bg-slate-200 rounded text-[10px] font-bold text-slate-600">
                    {idx + 1}
                  </span>
                  <span className="text-sm font-medium text-slate-700">
                    {district.district}
                  </span>
                </div>
                <div className="text-right">
                  <p className="text-sm font-bold text-slate-800">
                    {formatNumber(district.demand)}
                  </p>
                  <p className="text-[10px] text-slate-500">Tons</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Demand Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {demandComposition.map((item) => (
          <div
            key={item.name}
            className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm"
            style={{ borderTopColor: item.color, borderTopWidth: 3 }}
          >
            <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">{item.name}</p>
            <p className="text-xl font-bold text-slate-800">{formatNumber(item.value)}</p>
            <p className="text-[10px] text-slate-500">Tons Demand</p>
          </div>
        ))}
      </div>
    </div>
  )
}
