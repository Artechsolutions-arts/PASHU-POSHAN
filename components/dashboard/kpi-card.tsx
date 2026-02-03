import { cn } from "@/lib/utils"

interface KpiCardProps {
  title: string
  value: string
  unit?: string
  variant: "blue" | "slate" | "rose" | "emerald"
}

const variantStyles = {
  blue: "border-l-blue-600 bg-blue-50/30",
  slate: "border-l-slate-400 bg-slate-50/30",
  rose: "border-l-rose-500 bg-rose-50/30",
  emerald: "border-l-emerald-500 bg-emerald-50/30",
}

const valueStyles = {
  blue: "text-slate-800",
  slate: "text-slate-800",
  rose: "text-rose-700",
  emerald: "text-emerald-700",
}

const unitStyles = {
  blue: "text-slate-400",
  slate: "text-slate-400",
  rose: "text-rose-400",
  emerald: "text-emerald-400",
}

export function KpiCard({ title, value, unit, variant }: KpiCardProps) {
  return (
    <div
      className={cn(
        "bg-white border border-slate-200 border-l-[3px] p-5 rounded-lg shadow-sm hover:shadow-md transition-all hover:-translate-y-0.5",
        variantStyles[variant]
      )}
    >
      <p className="text-slate-400 text-[9px] font-bold uppercase tracking-widest mb-1">
        {title}
      </p>
      <div className="flex items-baseline">
        <h3 className={cn("text-2xl font-bold", valueStyles[variant])}>
          {value}
        </h3>
        {unit && (
          <span className={cn("ml-1 text-[9px] font-bold", unitStyles[variant])}>
            {unit}
          </span>
        )}
      </div>
    </div>
  )
}
