export interface DistrictData {
  district: string
  supply: number
  demand: number
  balance: number
  status: "SURPLUS" | "DEFICIT"
  deficitPercentage: number
}

export interface SupplyData {
  district: string
  total: number
  paddy: number
  wheat: number
  jowar: number
  bajra: number
  maize: number
  ragi: number
  smallMillets: number
  groundnut: number
  sugarcane: number
  cotton: number
  pulses: number
  soyabean: number
}

export interface DemandData {
  district: string
  total: number
  cattle: number
  buffaloes: number
  sheep: number
  goat: number
  pig: number
  poultry: number
}

// Gap Analysis Data
export const gapAnalysisData: DistrictData[] = [
  { district: "PRAKASAM", supply: 529193.34, demand: 2427896.20, balance: -1898702.86, status: "DEFICIT", deficitPercentage: -78.20 },
  { district: "KADAPA", supply: 363509.13, demand: 1481487.20, balance: -1117978.07, status: "DEFICIT", deficitPercentage: -75.46 },
  { district: "PALNADU", supply: 669802.04, demand: 1701896.30, balance: -1032094.26, status: "DEFICIT", deficitPercentage: -60.64 },
  { district: "ALLURI SITARAMA RAJU", supply: 449237.70, demand: 1409566.70, balance: -960328.99, status: "DEFICIT", deficitPercentage: -68.13 },
  { district: "TIRUPATI", supply: 464771.67, demand: 1347164.00, balance: -882392.33, status: "DEFICIT", deficitPercentage: -65.50 },
  { district: "ANANTAPUR", supply: 1056258.44, demand: 1930220.40, balance: -873961.96, status: "DEFICIT", deficitPercentage: -45.28 },
  { district: "CHITTOOR", supply: 464771.67, demand: 1324876.60, balance: -860104.93, status: "DEFICIT", deficitPercentage: -64.92 },
  { district: "SRI SATYASAI", supply: 1056258.44, demand: 1800929.60, balance: -744671.16, status: "DEFICIT", deficitPercentage: -41.35 },
  { district: "ANAKAPALLI", supply: 449237.70, demand: 1023363.20, balance: -574125.50, status: "DEFICIT", deficitPercentage: -56.10 },
  { district: "ANNAMAYYA", supply: 828280.80, demand: 1336268.50, balance: -507987.70, status: "DEFICIT", deficitPercentage: -38.02 },
  { district: "NANDYAL", supply: 1023277.72, demand: 1381420.20, balance: -358142.48, status: "DEFICIT", deficitPercentage: -25.93 },
  { district: "VIZIANAGARAM", supply: 824100.98, demand: 1134477.00, balance: -310376.02, status: "DEFICIT", deficitPercentage: -27.36 },
  { district: "KURNOOL", supply: 1023277.72, demand: 1201229.60, balance: -177951.88, status: "DEFICIT", deficitPercentage: -14.81 },
  { district: "GUNTUR", supply: 669802.04, demand: 735090.20, balance: -65288.16, status: "DEFICIT", deficitPercentage: -8.88 },
  { district: "BAPATLA", supply: 1198995.38, demand: 1242353.80, balance: -43358.42, status: "DEFICIT", deficitPercentage: -3.49 },
  { district: "NELLORE", supply: 1901064.73, demand: 1905278.40, balance: -4213.68, status: "DEFICIT", deficitPercentage: -0.22 },
  { district: "PARVATHIPURAM MANYAM", supply: 824100.98, demand: 719676.60, balance: 104424.38, status: "SURPLUS", deficitPercentage: 14.51 },
  { district: "KAKINADA", supply: 1219509.46, demand: 1105806.80, balance: 113702.66, status: "SURPLUS", deficitPercentage: 10.28 },
  { district: "ELURU", supply: 1828093.46, demand: 1665749.50, balance: 162343.96, status: "SURPLUS", deficitPercentage: 9.75 },
  { district: "VISAKHAPATNAM", supply: 449237.70, demand: 191088.90, balance: 258148.80, status: "SURPLUS", deficitPercentage: 135.09 },
  { district: "KRISHNA", supply: 1215900.87, demand: 932936.60, balance: 282964.27, status: "SURPLUS", deficitPercentage: 30.33 },
  { district: "SRIKAKULAM", supply: 2130032.60, demand: 1826780.20, balance: 303252.40, status: "SURPLUS", deficitPercentage: 16.60 },
  { district: "EAST GODAVARI", supply: 1219509.46, demand: 835828.40, balance: 383681.06, status: "SURPLUS", deficitPercentage: 45.90 },
  { district: "NTR", supply: 1215900.87, demand: 804089.50, balance: 411811.37, status: "SURPLUS", deficitPercentage: 51.21 },
  { district: "DR B.R. AMBEDKAR KONASEEMA", supply: 1219509.46, demand: 647000.60, balance: 572508.86, status: "SURPLUS", deficitPercentage: 88.49 },
  { district: "WEST GODAVARI", supply: 1828093.46, demand: 543642.20, balance: 1284451.26, status: "SURPLUS", deficitPercentage: 236.27 },
]

// Demand breakdown by livestock
export const demandByLivestock: DemandData[] = [
  { district: "PRAKASAM", total: 2427896.2, cattle: 137387.8, buffaloes: 1849564.6, sheep: 331450.8, goat: 106927.8, pig: 2565.2, poultry: 0 },
  { district: "ANANTAPUR", total: 1930220.4, cattle: 649569.8, buffaloes: 601075.8, sheep: 570066.3, goat: 103522.5, pig: 5986.0, poultry: 0 },
  { district: "NELLORE", total: 1905278.4, cattle: 139260.0, buffaloes: 1425860.8, sheep: 253269.0, goat: 85055.4, pig: 1833.2, poultry: 0 },
  { district: "SRIKAKULAM", total: 1826780.2, cattle: 1365993.2, buffaloes: 267384.0, sheep: 142930.5, goat: 49414.5, pig: 1058.0, poultry: 0 },
]

// Calculate totals
export function calculateTotals() {
  const totalSupply = gapAnalysisData.reduce((acc, d) => acc + d.supply, 0)
  const totalDemand = gapAnalysisData.reduce((acc, d) => acc + d.demand, 0)
  const totalBalance = totalSupply - totalDemand
  const sufficiencyIndex = (totalSupply / totalDemand) * 100
  
  return {
    totalSupply,
    totalDemand,
    totalBalance,
    sufficiencyIndex
  }
}

// Format number to human readable
export function formatNumber(num: number): string {
  if (Math.abs(num) >= 1000000) {
    return (num / 1000000).toFixed(2) + "M"
  }
  if (Math.abs(num) >= 1000) {
    return (num / 1000).toFixed(1) + "K"
  }
  return num.toFixed(0)
}

// Get supply composition data for pie chart
export function getSupplyComposition() {
  return [
    { name: "Paddy", value: 14523000, color: "#facc15" },
    { name: "Maize", value: 1256000, color: "#22c55e" },
    { name: "Groundnut", value: 1478000, color: "#f97316" },
    { name: "Sugarcane", value: 1289000, color: "#3b82f6" },
    { name: "Small Millets", value: 545000, color: "#8b5cf6" },
    { name: "Others", value: 789000, color: "#94a3b8" },
  ]
}

// Get demand composition data for pie chart
export function getDemandComposition() {
  return [
    { name: "Buffaloes", value: 12450000, color: "#3b82f6" },
    { name: "Cattle", value: 8350000, color: "#22c55e" },
    { name: "Sheep", value: 3120000, color: "#facc15" },
    { name: "Goat", value: 1050000, color: "#f97316" },
    { name: "Pig", value: 45000, color: "#8b5cf6" },
  ]
}

// Get risk districts (deficit > 40%)
export function getRiskDistricts() {
  return gapAnalysisData
    .filter(d => d.status === "DEFICIT" && Math.abs(d.deficitPercentage) > 40)
    .sort((a, b) => a.deficitPercentage - b.deficitPercentage)
}
