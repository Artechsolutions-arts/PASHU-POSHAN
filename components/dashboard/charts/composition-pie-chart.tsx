"use client"

import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts"

interface CompositionData {
  name: string
  value: number
  color: string
}

interface CompositionPieChartProps {
  data: CompositionData[]
}

export function CompositionPieChart({ data }: CompositionPieChartProps) {
  const formatValue = (value: number) => {
    if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`
    if (value >= 1000) return `${(value / 1000).toFixed(0)}K`
    return value.toString()
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={50}
          outerRadius={90}
          paddingAngle={2}
          dataKey="value"
          label={({ name, percent }) => 
            percent > 0.05 ? `${name} ${(percent * 100).toFixed(0)}%` : ""
          }
          labelLine={false}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: "white",
            border: "1px solid #e2e8f0",
            borderRadius: "8px",
            fontSize: "11px",
          }}
          formatter={(value: number) => [`${formatValue(value)} Tons`, ""]}
        />
        <Legend
          verticalAlign="bottom"
          height={36}
          formatter={(value) => (
            <span style={{ fontSize: "10px", fontWeight: 500, color: "#64748b" }}>
              {value}
            </span>
          )}
        />
      </PieChart>
    </ResponsiveContainer>
  )
}
