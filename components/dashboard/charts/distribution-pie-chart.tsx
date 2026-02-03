"use client"

import { gapAnalysisData } from "@/lib/data"
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts"

const COLORS = ["#22c55e", "#ef4444"]

export function DistributionPieChart() {
  const surplusCount = gapAnalysisData.filter((d) => d.status === "SURPLUS").length
  const deficitCount = gapAnalysisData.filter((d) => d.status === "DEFICIT").length

  const data = [
    { name: "Surplus Districts", value: surplusCount },
    { name: "Deficit Districts", value: deficitCount },
  ]

  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={90}
          paddingAngle={5}
          dataKey="value"
          label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}
          labelLine={false}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: "white",
            border: "1px solid #e2e8f0",
            borderRadius: "8px",
            fontSize: "11px",
          }}
          formatter={(value: number) => [`${value} districts`, ""]}
        />
        <Legend
          verticalAlign="bottom"
          height={36}
          formatter={(value) => (
            <span style={{ fontSize: "10px", fontWeight: 600, color: "#64748b" }}>
              {value}
            </span>
          )}
        />
      </PieChart>
    </ResponsiveContainer>
  )
}
