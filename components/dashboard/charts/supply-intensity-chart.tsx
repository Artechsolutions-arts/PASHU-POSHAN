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
} from "recharts"

interface SupplyIntensityChartProps {
  data: DistrictData[]
}

export function SupplyIntensityChart({ data }: SupplyIntensityChartProps) {
  const chartData = data.map((d) => ({
    name: d.district.length > 15 ? d.district.substring(0, 15) + "..." : d.district,
    fullName: d.district,
    supply: d.supply / 1000000,
  }))

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 80, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" horizontal={false} />
        <XAxis 
          type="number"
          tick={{ fontSize: 10, fill: "#64748b" }}
          tickFormatter={(value) => `${value}M`}
        />
        <YAxis 
          type="category"
          dataKey="name"
          tick={{ fontSize: 9, fill: "#64748b" }}
          width={75}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "white",
            border: "1px solid #e2e8f0",
            borderRadius: "8px",
            fontSize: "11px",
          }}
          formatter={(value: number) => [`${value.toFixed(2)}M Tons`, "Supply"]}
          labelFormatter={(label, payload) => {
            if (payload && payload[0]) {
              return payload[0].payload.fullName
            }
            return label
          }}
        />
        <Bar 
          dataKey="supply" 
          fill="#3b82f6" 
          radius={[0, 4, 4, 0]}
          background={{ fill: "#f1f5f9" }}
        />
      </BarChart>
    </ResponsiveContainer>
  )
}
