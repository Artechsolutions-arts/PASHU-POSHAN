"use client"

import { useEffect, useState } from "react"
import { Menu, Download } from "lucide-react"

interface HeaderProps {
  title: string
  onToggleSidebar: () => void
  isSidebarCollapsed: boolean
}

export function Header({ title, onToggleSidebar, isSidebarCollapsed }: HeaderProps) {
  const [currentTime, setCurrentTime] = useState("")
  
  useEffect(() => {
    const updateTime = () => {
      setCurrentTime(new Date().toLocaleTimeString('en-IN', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
      }))
    }
    updateTime()
    const interval = setInterval(updateTime, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <header className="bg-white border-b border-slate-200 px-6 lg:px-10 py-5 flex justify-between items-center sticky top-0 z-30">
      <div className="flex items-center gap-4">
        {isSidebarCollapsed && (
          <button
            onClick={onToggleSidebar}
            className="p-2 bg-slate-100 hover:bg-slate-200 rounded-lg transition text-slate-800 hidden lg:flex"
          >
            <Menu className="h-5 w-5" />
          </button>
        )}
        <div>
          <h2 className="text-slate-800 text-lg font-bold">{title}</h2>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
              Live System Sync <span className="mx-1 text-slate-300">|</span>
              <span className="font-mono text-slate-500">{currentTime}</span>
            </span>
          </div>
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="hidden md:flex items-center gap-4">
          <label className="text-[10px] font-bold text-slate-400 uppercase">Region:</label>
          <select className="bg-slate-100 text-xs font-bold rounded-md px-4 py-2 outline-none border-none focus:ring-2 focus:ring-blue-500">
            <option value="all">ANDHRA PRADESH (STATE)</option>
          </select>
        </div>
        <button className="border border-slate-200 text-slate-800 text-[10px] font-bold px-4 py-2 rounded-md hover:bg-slate-50 transition shadow-sm flex items-center gap-2">
          <Download className="h-3 w-3" />
          <span className="hidden sm:inline">EXPORT DATA</span>
        </button>
      </div>
    </header>
  )
}
