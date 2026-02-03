"use client"

import { useState } from "react"
import { 
  BarChart3, 
  Leaf, 
  TrendingUp, 
  AlertTriangle, 
  LineChart,
  Menu,
  X,
  ChevronRight
} from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
  LineChart as RechartsLineChart,
  Line,
} from "recharts"

// District data for Andhra Pradesh
const districtData = [
  { district: "Anantapur", supply: 2850000, demand: 3200000, balance: -350000 },
  { district: "Chittoor", supply: 1920000, demand: 2100000, balance: -180000 },
  { district: "Kadapa", supply: 1650000, demand: 1800000, balance: -150000 },
  { district: "Kurnool", supply: 2100000, demand: 2450000, balance: -350000 },
  { district: "Nellore", supply: 1450000, demand: 1200000, balance: 250000 },
  { district: "Prakasam", supply: 1780000, demand: 1650000, balance: 130000 },
  { district: "Srikakulam", supply: 980000, demand: 850000, balance: 130000 },
  { district: "Vizianagaram", supply: 1120000, demand: 950000, balance: 170000 },
  { district: "Visakhapatnam", supply: 1350000, demand: 1100000, balance: 250000 },
  { district: "East Godavari", supply: 2100000, demand: 1750000, balance: 350000 },
  { district: "West Godavari", supply: 1980000, demand: 1650000, balance: 330000 },
  { district: "Krishna", supply: 1850000, demand: 1500000, balance: 350000 },
  { district: "Guntur", supply: 2250000, demand: 1900000, balance: 350000 },
]

const totalSupply = districtData.reduce((sum, d) => sum + d.supply, 0)
const totalDemand = districtData.reduce((sum, d) => sum + d.demand, 0)
const totalBalance = totalSupply - totalDemand
const sufficiencyIndex = (totalSupply / totalDemand) * 100

const supplyComposition = [
  { name: "Green Fodder", value: 45, color: "#22c55e" },
  { name: "Dry Fodder", value: 35, color: "#f59e0b" },
  { name: "Concentrates", value: 20, color: "#3b82f6" },
]

const monthlyTrend = [
  { month: "Jan", supply: 2100, demand: 2400 },
  { month: "Feb", supply: 2200, demand: 2350 },
  { month: "Mar", supply: 2400, demand: 2300 },
  { month: "Apr", supply: 2600, demand: 2250 },
  { month: "May", supply: 2300, demand: 2400 },
  { month: "Jun", supply: 1900, demand: 2500 },
]

type View = "overview" | "supply" | "demand" | "risk" | "predict"

const navItems = [
  { id: "overview" as View, label: "Executive Overview", icon: BarChart3 },
  { id: "supply" as View, label: "Supply Profile", icon: Leaf },
  { id: "demand" as View, label: "Demand Dynamics", icon: TrendingUp },
  { id: "risk" as View, label: "Risk & Vulnerability", icon: AlertTriangle },
  { id: "predict" as View, label: "Future Predictions", icon: LineChart },
]

function formatNumber(num: number): string {
  if (Math.abs(num) >= 1000000) {
    return (num / 1000000).toFixed(2) + "M"
  }
  if (Math.abs(num) >= 1000) {
    return (num / 1000).toFixed(1) + "K"
  }
  return num.toString()
}

export default function Dashboard() {
  const [currentView, setCurrentView] = useState<View>("overview")
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const criticalDistricts = districtData.filter(d => d.balance < 0)

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Mobile Header */}
      <header className="lg:hidden fixed top-0 left-0 right-0 h-16 bg-slate-900 text-white flex items-center px-4 z-50">
        <Button 
          variant="ghost" 
          size="icon" 
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="text-white hover:bg-slate-800"
        >
          {sidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </Button>
        <div className="ml-4">
          <h1 className="text-lg font-bold tracking-tight">FORAGE</h1>
          <p className="text-xs text-slate-400">Pashu Poshan</p>
        </div>
      </header>

      {/* Sidebar */}
      <aside className={`
        fixed top-0 left-0 h-full w-72 bg-slate-900 text-white z-40 transition-transform duration-300
        lg:translate-x-0
        ${sidebarOpen ? "translate-x-0" : "-translate-x-full"}
      `}>
        <div className="p-6 border-b border-slate-800">
          <h1 className="text-2xl font-bold tracking-tight">FORAGE</h1>
          <p className="text-xs text-slate-400 uppercase tracking-widest mt-1">Pashu Poshan</p>
          <p className="text-xs text-slate-500 mt-2">Fodder Analytics Dashboard</p>
        </div>
        
        <nav className="p-4 space-y-1">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => {
                setCurrentView(item.id)
                setSidebarOpen(false)
              }}
              className={`
                w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-all
                ${currentView === item.id 
                  ? "bg-blue-600 text-white" 
                  : "text-slate-400 hover:bg-slate-800 hover:text-white"
                }
              `}
            >
              <item.icon className="h-5 w-5" />
              <span className="text-sm font-medium">{item.label}</span>
              {currentView === item.id && <ChevronRight className="h-4 w-4 ml-auto" />}
            </button>
          ))}
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-800">
          <p className="text-xs text-slate-500 text-center">Andhra Pradesh</p>
          <p className="text-xs text-slate-600 text-center mt-1">Animal Husbandry Dept.</p>
        </div>
      </aside>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <main className="lg:ml-72 pt-16 lg:pt-0">
        {/* Page Header */}
        <div className="bg-white border-b border-slate-200 px-6 py-5">
          <h2 className="text-2xl font-semibold text-slate-900">
            {navItems.find(n => n.id === currentView)?.label}
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Comprehensive fodder supply and demand analytics
          </p>
        </div>

        <div className="p-6 space-y-6">
          {/* KPI Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card className="border-l-4 border-l-blue-500">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-500">
                  Gross Fodder Supply
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-slate-900">
                  {formatNumber(totalSupply)}
                </div>
                <p className="text-xs text-slate-500 mt-1">Metric Tons</p>
              </CardContent>
            </Card>

            <Card className="border-l-4 border-l-slate-500">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-500">
                  Total Dry Matter Demand
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-slate-900">
                  {formatNumber(totalDemand)}
                </div>
                <p className="text-xs text-slate-500 mt-1">Metric Tons</p>
              </CardContent>
            </Card>

            <Card className={`border-l-4 ${totalBalance >= 0 ? "border-l-emerald-500" : "border-l-rose-500"}`}>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-500">
                  Consolidated Net Gap
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className={`text-2xl font-bold ${totalBalance >= 0 ? "text-emerald-600" : "text-rose-600"}`}>
                  {totalBalance >= 0 ? "+" : ""}{formatNumber(totalBalance)}
                </div>
                <p className="text-xs text-slate-500 mt-1">Metric Tons</p>
              </CardContent>
            </Card>

            <Card className="border-l-4 border-l-emerald-500">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-500">
                  Sufficiency Index
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-emerald-600">
                  {sufficiencyIndex.toFixed(1)}%
                </div>
                <p className="text-xs text-slate-500 mt-1">Supply / Demand Ratio</p>
              </CardContent>
            </Card>
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Supply vs Demand Bar Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">District-wise Supply vs Demand</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={districtData.slice(0, 8)} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                      <XAxis type="number" tickFormatter={(v) => formatNumber(v)} />
                      <YAxis dataKey="district" type="category" width={100} tick={{ fontSize: 12 }} />
                      <Tooltip 
                        formatter={(value: number) => formatNumber(value)}
                        contentStyle={{ borderRadius: "8px", border: "1px solid #e2e8f0" }}
                      />
                      <Legend />
                      <Bar dataKey="supply" name="Supply" fill="#3b82f6" radius={[0, 4, 4, 0]} />
                      <Bar dataKey="demand" name="Demand" fill="#94a3b8" radius={[0, 4, 4, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            {/* Supply Composition Pie */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Fodder Supply Composition</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={supplyComposition}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={100}
                        paddingAngle={2}
                        dataKey="value"
                        label={({ name, value }) => `${name}: ${value}%`}
                      >
                        {supplyComposition.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Monthly Trend */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Monthly Supply & Demand Trend</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <RechartsLineChart data={monthlyTrend}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip contentStyle={{ borderRadius: "8px", border: "1px solid #e2e8f0" }} />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="supply" 
                      name="Supply" 
                      stroke="#3b82f6" 
                      strokeWidth={2}
                      dot={{ fill: "#3b82f6" }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="demand" 
                      name="Demand" 
                      stroke="#ef4444" 
                      strokeWidth={2}
                      dot={{ fill: "#ef4444" }}
                    />
                  </RechartsLineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          {/* Critical Districts */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-amber-500" />
                Critical Deficit Districts
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-slate-200">
                      <th className="text-left py-3 px-4 text-sm font-semibold text-slate-600">District</th>
                      <th className="text-right py-3 px-4 text-sm font-semibold text-slate-600">Supply</th>
                      <th className="text-right py-3 px-4 text-sm font-semibold text-slate-600">Demand</th>
                      <th className="text-right py-3 px-4 text-sm font-semibold text-slate-600">Deficit</th>
                      <th className="text-left py-3 px-4 text-sm font-semibold text-slate-600">Severity</th>
                    </tr>
                  </thead>
                  <tbody>
                    {criticalDistricts.map((d) => {
                      const severity = Math.abs(d.balance) / d.demand * 100
                      return (
                        <tr key={d.district} className="border-b border-slate-100 hover:bg-slate-50">
                          <td className="py-3 px-4 font-medium text-slate-900">{d.district}</td>
                          <td className="py-3 px-4 text-right text-slate-600">{formatNumber(d.supply)}</td>
                          <td className="py-3 px-4 text-right text-slate-600">{formatNumber(d.demand)}</td>
                          <td className="py-3 px-4 text-right font-medium text-rose-600">
                            {formatNumber(d.balance)}
                          </td>
                          <td className="py-3 px-4">
                            <div className="flex items-center gap-2">
                              <div className="w-20 h-2 bg-slate-200 rounded-full overflow-hidden">
                                <div 
                                  className={`h-full rounded-full ${
                                    severity > 15 ? "bg-rose-500" : severity > 10 ? "bg-amber-500" : "bg-yellow-500"
                                  }`}
                                  style={{ width: `${Math.min(severity * 5, 100)}%` }}
                                />
                              </div>
                              <span className="text-xs text-slate-500">{severity.toFixed(1)}%</span>
                            </div>
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
