"use client"

import { getRiskDistricts, formatNumber } from "@/lib/data"
import { AlertTriangle } from "lucide-react"

export function RiskView() {
  const riskDistricts = getRiskDistricts()
  
  return (
    <div className="space-y-8">
      {/* Alert Banner */}
      <div className="bg-rose-50 border border-rose-200 p-6 rounded-xl">
        <div className="flex items-start gap-4">
          <AlertTriangle className="h-6 w-6 text-rose-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="text-rose-900 font-bold text-sm uppercase mb-1">
              Administrative Priority Alert
            </h4>
            <p className="text-rose-700 text-[11px]">
              The following districts report a critical resource gap (deficit {'>'} 40%). 
              Immediate logistical support is recommended.
            </p>
          </div>
        </div>
      </div>
      
      {/* Risk District Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {riskDistricts.map((district, idx) => {
          const severity = Math.abs(district.deficitPercentage)
          const severityColor = severity > 65 ? "rose" : severity > 50 ? "orange" : "amber"
          
          return (
            <div
              key={district.district}
              className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden hover:shadow-md transition"
            >
              {/* Severity Header */}
              <div className={`px-4 py-2 ${
                severityColor === "rose" ? "bg-rose-500" :
                severityColor === "orange" ? "bg-orange-500" : "bg-amber-500"
              }`}>
                <div className="flex items-center justify-between">
                  <span className="text-white text-[10px] font-bold uppercase tracking-wider">
                    {severityColor === "rose" ? "CRITICAL" : severityColor === "orange" ? "HIGH" : "MODERATE"} RISK
                  </span>
                  <span className="text-white/80 text-[10px] font-mono">
                    #{idx + 1}
                  </span>
                </div>
              </div>
              
              {/* Card Content */}
              <div className="p-5">
                <h3 className="font-bold text-slate-800 mb-4">{district.district}</h3>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-[10px] font-bold text-slate-400 uppercase">Supply</span>
                    <span className="text-sm font-semibold text-slate-600">
                      {formatNumber(district.supply)} T
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-[10px] font-bold text-slate-400 uppercase">Demand</span>
                    <span className="text-sm font-semibold text-slate-600">
                      {formatNumber(district.demand)} T
                    </span>
                  </div>
                  
                  <div className="border-t border-slate-100 pt-3">
                    <div className="flex justify-between items-center">
                      <span className="text-[10px] font-bold text-slate-400 uppercase">Deficit</span>
                      <span className="text-lg font-bold text-rose-600">
                        {formatNumber(Math.abs(district.balance))} T
                      </span>
                    </div>
                  </div>
                  
                  {/* Deficit Bar */}
                  <div className="mt-2">
                    <div className="flex justify-between text-[9px] text-slate-400 mb-1">
                      <span>Sufficiency Index</span>
                      <span>{(100 + district.deficitPercentage).toFixed(1)}%</span>
                    </div>
                    <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full ${
                          severityColor === "rose" ? "bg-rose-500" :
                          severityColor === "orange" ? "bg-orange-500" : "bg-amber-500"
                        }`}
                        style={{ width: `${Math.max(5, 100 + district.deficitPercentage)}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )
        })}
      </div>
      
      {/* Summary Stats */}
      <div className="bg-slate-800 rounded-xl p-6 text-white">
        <h4 className="font-bold uppercase text-sm mb-4">Risk Summary</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div>
            <p className="text-slate-400 text-[10px] uppercase font-bold">Districts at Risk</p>
            <p className="text-3xl font-bold">{riskDistricts.length}</p>
          </div>
          <div>
            <p className="text-slate-400 text-[10px] uppercase font-bold">Total Deficit</p>
            <p className="text-3xl font-bold text-rose-400">
              {formatNumber(riskDistricts.reduce((acc, d) => acc + Math.abs(d.balance), 0))}
            </p>
          </div>
          <div>
            <p className="text-slate-400 text-[10px] uppercase font-bold">Critical Zones</p>
            <p className="text-3xl font-bold text-rose-400">
              {riskDistricts.filter(d => Math.abs(d.deficitPercentage) > 65).length}
            </p>
          </div>
          <div>
            <p className="text-slate-400 text-[10px] uppercase font-bold">Avg Deficit %</p>
            <p className="text-3xl font-bold text-orange-400">
              {(riskDistricts.reduce((acc, d) => acc + Math.abs(d.deficitPercentage), 0) / riskDistricts.length).toFixed(1)}%
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
