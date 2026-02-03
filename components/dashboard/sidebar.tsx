"use client"

import { cn } from "@/lib/utils"
import { BarChart3, Leaf, Users, AlertTriangle, TrendingUp, Upload, Download, ChevronLeft, Menu } from "lucide-react"

type View = "overview" | "supply" | "demand" | "risk" | "predict"

interface SidebarProps {
  currentView: View
  onViewChange: (view: View) => void
  isCollapsed: boolean
  onToggle: () => void
}

const navItems = [
  { id: "overview" as View, label: "Executive Overview", icon: BarChart3 },
  { id: "supply" as View, label: "Supply Profile", icon: Leaf },
  { id: "demand" as View, label: "Demand Dynamics", icon: Users },
  { id: "risk" as View, label: "Risk & Vulnerability", icon: AlertTriangle },
  { id: "predict" as View, label: "Future Predictions", icon: TrendingUp },
]

export function Sidebar({ currentView, onViewChange, isCollapsed, onToggle }: SidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {!isCollapsed && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onToggle}
        />
      )}
      
      <aside
        className={cn(
          "fixed left-0 top-0 h-screen bg-[hsl(var(--navy-dark))] text-white z-50 transition-transform duration-300 flex flex-col",
          isCollapsed ? "-translate-x-full" : "translate-x-0",
          "w-72"
        )}
      >
        {/* Header */}
        <div className="p-6 border-b border-slate-700">
          <div className="flex items-center justify-between">
            <div className="text-center flex-1">
              <h1 className="text-2xl font-black tracking-tight">FORAGE</h1>
              <p className="text-[10px] text-slate-400 mt-1 uppercase font-bold tracking-[0.2em]">
                pashuposhana
              </p>
            </div>
            <button
              onClick={onToggle}
              className="p-1.5 hover:bg-slate-700 rounded-lg transition lg:absolute lg:-right-4 lg:top-10 lg:bg-blue-600 lg:hover:bg-blue-500 lg:rounded-full lg:shadow-xl"
            >
              <ChevronLeft className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="p-6 space-y-2">
          <button className="w-full bg-blue-600 hover:bg-blue-500 text-white text-[10px] font-bold py-3 rounded-lg flex items-center justify-center transition shadow-lg">
            <Upload className="h-4 w-4 mr-2" />
            UPLOAD DATASET
          </button>
          <button className="w-full bg-slate-800 hover:bg-slate-700 text-slate-300 text-[10px] font-bold py-3 rounded-lg flex items-center justify-center transition border border-slate-700">
            <Download className="h-4 w-4 mr-2" />
            EXPORT REPORT
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = currentView === item.id
            return (
              <button
                key={item.id}
                onClick={() => onViewChange(item.id)}
                className={cn(
                  "w-full text-left flex items-center px-4 py-3 rounded-lg font-semibold transition group",
                  isActive
                    ? "bg-slate-800 text-white border-l-[3px] border-blue-400"
                    : "text-slate-400 hover:text-white hover:bg-slate-800/50"
                )}
              >
                <Icon className={cn(
                  "h-4 w-4 mr-3 transition",
                  isActive ? "text-blue-400" : "text-slate-500 group-hover:text-blue-400"
                )} />
                {item.label}
              </button>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="p-6 text-[10px] text-slate-500 font-mono">
          <p>BUILD: 2026.02.03-V1</p>
          <p>DEPT. OF ANIMAL HUSBANDRY</p>
        </div>
      </aside>

      {/* Mobile toggle button */}
      {isCollapsed && (
        <button
          onClick={onToggle}
          className="fixed top-4 left-4 z-40 p-2 bg-slate-100 hover:bg-slate-200 rounded-lg transition text-slate-800 lg:hidden"
        >
          <Menu className="h-5 w-5" />
        </button>
      )}
    </>
  )
}
