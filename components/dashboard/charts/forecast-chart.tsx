"use client"

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts"

interface ForecastData {
  month: string
  supply: number
  demand: number
  gap: number
}

interface ForecastChartProps {
  data: ForecastData[]
}

export function ForecastChart({ data }: ForecastChartProps) {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis 
          dataKey="month" 
          tick={{ fontSize: 11, fill: "#64748b" }}
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
            `${value.toFixed(1)}M Tons`,
            name === "supply" ? "Predicted Supply" : "Predicted Demand",
          ]}
        />
        <ReferenceLine y={30} stroke="#94a3b8" strokeDasharray="3 3" />
        <Line
          type="monotone"
          dataKey="supply"
          stroke="#3b82f6"
          strokeWidth={3}
          dot={{ fill: "#3b82f6", strokeWidth: 2, r: 4 }}
          activeDot={{ r: 6 }}
        />
        <Line
          type="monotone"
          dataKey="demand"
          stroke="#a5b4fc"
          strokeWidth={3}
          strokeDasharray="5 5"
          dot={{ fill: "#a5b4fc", strokeWidth: 2, r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
