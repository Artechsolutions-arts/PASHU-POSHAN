"use client"

import { DistrictData } from "@/lib/data"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts"

interface SupplyDemandChartProps {
  data: DistrictData[]
}

export function SupplyDemandChart({ data }: SupplyDemandChartProps) {
  const chartData = data.map((d) => ({
    name: d.district.length > 12 ? d.district.substring(0, 12) + "..." : d.district,
    fullName: d.district,
    supply: d.supply / 1000000,
    demand: d.demand / 1000000,
  }))

  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis 
          dataKey="name" 
          tick={{ fontSize: 9, fill: "#64748b" }}
          angle={-45}
          textAnchor="end"
          height={80}
        />
        <YAxis 
          tick={{ fontSize: 10, fill: "#64748b" }}
          tickFormatter={(value) => `${value}M`}
          label={{ value: 'Tons (Millions)', angle: -90, position: 'insideLeft', style: { fontSize: 10, fill: '#94a3b8' } }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "white",
            border: "1px solid #e2e8f0",
            borderRadius: "8px",
            fontSize: "11px",
          }}
          formatter={(value: number, name: string) => [
            `${value.toFixed(2)}M Tons`,
            name === "supply" ? "Supply" : "Demand",
          ]}
          labelFormatter={(label, payload) => {
            if (payload && payload[0]) {
              return payload[0].payload.fullName
            }
            return label
          }}
        />
        <Legend 
          verticalAlign="top" 
          height={36}
          formatter={(value) => (
            <span style={{ fontSize: "10px", fontWeight: 600, color: "#64748b" }}>
              {value === "supply" ? "SUPPLY" : "DEMAND"}
            </span>
          )}
        />
        <Bar dataKey="supply" fill="#facc15" radius={[4, 4, 0, 0]} />
        <Bar dataKey="demand" fill="#ef4444" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}
