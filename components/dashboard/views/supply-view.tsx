"use client"

import { gapAnalysisData, formatNumber, getSupplyComposition } from "@/lib/data"
import { CompositionPieChart } from "../charts/composition-pie-chart"
import { SupplyIntensityChart } from "../charts/supply-intensity-chart"

export function SupplyView() {
  const supplyComposition = getSupplyComposition()
  const topSupplyDistricts = [...gapAnalysisData]
    .sort((a, b) => b.supply - a.supply)
    .slice(0, 10)
  
  return (
    <div className="space-y-8">
      {/* Sunburst placeholder - simplified to composition breakdown */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <h4 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-4">
          Hierarchical Crop Distribution
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {supplyComposition.map((crop) => (
            <div 
              key={crop.name}
              className="p-4 rounded-lg border border-slate-100 hover:border-slate-200 transition"
              style={{ borderLeftColor: crop.color, borderLeftWidth: 3 }}
            >
              <p className="text-[10px] font-bold text-slate-400 uppercase">{crop.name}</p>
              <p className="text-lg font-bold text-slate-800">{formatNumber(crop.value)}</p>
              <p className="text-[10px] text-slate-500">Tons</p>
            </div>
          ))}
        </div>
      </div>
      
      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Biomass Composition */}
        <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm">
          <h4 className="text-sm font-bold text-slate-800 uppercase mb-6">
            Biomass Composition
          </h4>
          <CompositionPieChart data={supplyComposition} />
        </div>
        
        {/* Supply Intensity */}
        <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm">
          <h4 className="text-sm font-bold text-slate-800 uppercase mb-6">
            Supply Intensity by District
          </h4>
          <SupplyIntensityChart data={topSupplyDistricts} />
        </div>
      </div>
    </div>
  )
}
