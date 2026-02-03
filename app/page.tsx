"use client"

import { useState } from "react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { KpiCard } from "@/components/dashboard/kpi-card"
import { OverviewView } from "@/components/dashboard/views/overview-view"
import { SupplyView } from "@/components/dashboard/views/supply-view"
import { DemandView } from "@/components/dashboard/views/demand-view"
import { RiskView } from "@/components/dashboard/views/risk-view"
import { PredictView } from "@/components/dashboard/views/predict-view"
import { calculateTotals, formatNumber } from "@/lib/data"

type View = "overview" | "supply" | "demand" | "risk" | "predict"

const viewTitles: Record<View, string> = {
  overview: "Executive Overview",
  supply: "Supply Profile",
  demand: "Demand Dynamics",
  risk: "Risk & Vulnerability",
  predict: "Future Predictions",
}

export default function Home() {
  const [currentView, setCurrentView] = useState<View>("overview")
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  
  const totals = calculateTotals()
  
  return (
    <div className="min-h-screen bg-[hsl(var(--background))]">
      <Sidebar
        currentView={currentView}
        onViewChange={setCurrentView}
        isCollapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
      />
      
      <div className={`transition-all duration-300 ${sidebarCollapsed ? "lg:ml-0" : "lg:ml-72"}`}>
        <Header
          title={viewTitles[currentView]}
          onToggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)}
          isSidebarCollapsed={sidebarCollapsed}
        />
        
        <main className="p-6 lg:p-10">
          {/* Global KPIs */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mb-8 lg:mb-10">
            <KpiCard
              title="Gross Fodder Supply"
              value={formatNumber(totals.totalSupply)}
              unit="Tons"
              variant="blue"
            />
            <KpiCard
              title="Total Dry Matter Demand"
              value={formatNumber(totals.totalDemand)}
              unit="Tons"
              variant="slate"
            />
            <KpiCard
              title="Consolidated Net Gap"
              value={formatNumber(totals.totalBalance)}
              unit="Tons"
              variant="rose"
            />
            <KpiCard
              title="Sufficiency Index"
              value={`${totals.sufficiencyIndex.toFixed(1)}%`}
              variant="emerald"
            />
          </div>
          
          {/* View Content */}
          {currentView === "overview" && <OverviewView />}
          {currentView === "supply" && <SupplyView />}
          {currentView === "demand" && <DemandView />}
          {currentView === "risk" && <RiskView />}
          {currentView === "predict" && <PredictView />}
        </main>
      </div>
    </div>
  )
}
