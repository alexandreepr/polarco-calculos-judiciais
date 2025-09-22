import * as React from "react"
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts"

import { useIsMobile } from "@/hooks/use-mobile"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  ToggleGroup,
  ToggleGroupItem,
} from "@/components/ui/toggle-group"

export const description = "Bar charts by user"

const chartDataByUserAndDate = [
  { dateOfPurchase: "2024-01-01", user: "Maria Silva", comprado: 1200, liquidado: 1000 },
  { dateOfPurchase: "2024-01-01", user: "Carlos Pereira", comprado: 900, liquidado: 800 },
  { dateOfPurchase: "2024-02-01", user: "Maria Silva", comprado: 1500, liquidado: 1400 },
  { dateOfPurchase: "2024-02-01", user: "Carlos Pereira", comprado: 1100, liquidado: 900 },
  { dateOfPurchase: "2024-03-01", user: "Maria Silva", comprado: 1700, liquidado: 1600 },
  { dateOfPurchase: "2024-03-01", user: "Carlos Pereira", comprado: 1200, liquidado: 1100 },
  { dateOfPurchase: "2024-03-01", user: "Ana Oliveira", comprado: 1000, liquidado: 900 },
  { dateOfPurchase: "2024-04-01", user: "Ana Oliveira", comprado: 1300, liquidado: 1200 },
  { dateOfPurchase: "2024-04-01", user: "Bruno Costa", comprado: 900, liquidado: 800 },
  { dateOfPurchase: "2024-05-01", user: "Maria Silva", comprado: 2000, liquidado: 1800 },
  { dateOfPurchase: "2024-05-01", user: "Bruno Costa", comprado: 1100, liquidado: 1000 }
]

// Get unique users for chart series

const chartConfig = {
  comprado: {
    label: "Comprado",
    color: "hsl(var(--chart-1))",
  },
  liquidado: {
    label: "Liquidado",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig

const users = Array.from(new Set(chartDataByUserAndDate.map(d => d.user)))

function aggregateByUser(data, valueKey, startDate, endDate) {
  const userTotals = {}
  data.forEach(item => {
    const date = new Date(item.dateOfPurchase)
    if (date >= startDate && date <= endDate) {
      userTotals[item.user] = (userTotals[item.user] || 0) + (item[valueKey] || 0)
    }
  })
  // Sort users by value (ascending)
  return users
    .map(user => ({
      user,
      value: userTotals[user] || 0
    }))
    .sort((a, b) => a.value - b.value)
}

export function ChartAreaInteractive() {
  const isMobile = useIsMobile()
  const [timeRange, setTimeRange] = React.useState("12m")
  
  
  React.useEffect(() => {
    if (isMobile) {
      setTimeRange("1m")
    }
  }, [isMobile])

  // Calculate date range based on toggle
  const referenceDate = new Date("2024-06-30")
  let daysToSubtract = 365
  if (timeRange === "3m") {
    daysToSubtract = 90
  } else if (timeRange === "1m") {
    daysToSubtract = 30
  }
  const startDate = new Date(referenceDate)
  startDate.setDate(startDate.getDate() - daysToSubtract)

  // Aggregate data for each user in the selected date range
  const compradoData = React.useMemo(
    () => aggregateByUser(chartDataByUserAndDate, "comprado", startDate, referenceDate),
    [timeRange]
  )
  const liquidadoData = React.useMemo(
    () => aggregateByUser(chartDataByUserAndDate, "liquidado", startDate, referenceDate),
    [timeRange]
  )

  return (
    <div className="flex flex-col gap-4 md:flex-row">
      <Card className="flex-1 @container/card">
        <CardHeader>
          <CardTitle>Total Comprado ao longo do tempo</CardTitle>
          <CardDescription>
            Evolução do total comprado por data de compra
          </CardDescription>
          <div className="absolute right-4 top-4">
            <ToggleGroup
              type="single"
              value={timeRange}
              onValueChange={setTimeRange}
              variant="outline"
              className="@[767px]/card:flex hidden"
            >
              <ToggleGroupItem value="12m" className="h-8 px-2.5">
                Últimos 12 meses
              </ToggleGroupItem>
              <ToggleGroupItem value="3m" className="h-8 px-2.5">
                Últimos 3 meses
              </ToggleGroupItem>
              <ToggleGroupItem value="1m" className="h-8 px-2.5">
                Mês vigente
              </ToggleGroupItem>
            </ToggleGroup>
            <Select value={timeRange} onValueChange={setTimeRange}>
              <SelectTrigger
                className="@[767px]/card:hidden flex w-40"
                aria-label="Select a value"
              >
                <SelectValue placeholder="Last 3 months" />
              </SelectTrigger>
              <SelectContent className="rounded-xl">
                <SelectItem value="12m" className="rounded-lg">
                  Últimos 12 meses
                </SelectItem>
                <SelectItem value="3m" className="rounded-lg">
                  Últimos 3 meses
                </SelectItem>
                <SelectItem value="1m" className="rounded-lg">
                  Mês vigente
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
        <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
          <ChartContainer
            config={chartConfig}
            className="aspect-auto h-[250px] w-full"
          >
            <AreaChart data={compradoData}>
              <defs>
                <linearGradient id="fillComprado" x1="0" y1="0" x2="0" y2="1">
                  <stop
                    offset="5%"
                    stopColor="var(--color-desktop)"
                    stopOpacity={1.0}
                  />
                  <stop
                    offset="95%"
                    stopColor="var(--color-desktop)"
                    stopOpacity={0.1}
                  />
                </linearGradient>
              </defs>
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="user"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                minTickGap={32}
              />
              <XAxis
                dataKey="user"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                minTickGap={32}
              />
              <YAxis />
              <ChartTooltip
                cursor={false}
                content={
                  <ChartTooltipContent
                    labelFormatter={value => value}
                    indicator="dot"
                  />
                }
              />
              <Area
                dataKey="value"
                type="natural"
                fill="url(#fillComprado)"
                stroke="var(--color-desktop)"
                stackId="a"
              />
            </AreaChart>
          </ChartContainer>
        </CardContent>
      </Card>
      <Card className="flex-1 @container/card">
        <CardHeader>
          <CardTitle>Total Liquidado ao longo do tempo</CardTitle>
          <CardDescription>
            Evolução do total liquidado por data de compra
          </CardDescription>
          <div className="absolute right-4 top-4">
            <ToggleGroup
              type="single"
              value={timeRange}
              onValueChange={setTimeRange}
              variant="outline"
              className="@[767px]/card:flex hidden"
            >
              <ToggleGroupItem value="12m" className="h-8 px-2.5">
                Últimos 12 meses
              </ToggleGroupItem>
              <ToggleGroupItem value="3m" className="h-8 px-2.5">
                Últimos 3 meses
              </ToggleGroupItem>
              <ToggleGroupItem value="1m" className="h-8 px-2.5">
                Mês vigente
              </ToggleGroupItem>
            </ToggleGroup>
            <Select value={timeRange} onValueChange={setTimeRange}>
              <SelectTrigger
                className="@[767px]/card:hidden flex w-40"
                aria-label="Select a value"
              >
                <SelectValue placeholder="Last 3 months" />
              </SelectTrigger>
              <SelectContent className="rounded-xl">
                <SelectItem value="12m" className="rounded-lg">
                  Últimos 12 meses
                </SelectItem>
                <SelectItem value="3m" className="rounded-lg">
                  Últimos 3 meses
                </SelectItem>
                <SelectItem value="1m" className="rounded-lg">
                  Mês vigente
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
        <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
          <ChartContainer
            config={chartConfig}
            className="aspect-auto h-[250px] w-full"
          >
            <AreaChart data={liquidadoData}>
              <defs>
                <linearGradient id="fillLiquidado" x1="0" y1="0" x2="0" y2="1">
                  <stop
                    offset="5%"
                    stopColor="var(--color-mobile)"
                    stopOpacity={0.8}
                  />
                  <stop
                    offset="95%"
                    stopColor="var(--color-mobile)"
                    stopOpacity={0.1}
                  />
                </linearGradient>
              </defs>
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="user"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                minTickGap={32}
              />
              <YAxis />
              <ChartTooltip
                cursor={false}
                content={
                  <ChartTooltipContent
                    labelFormatter={value => value}
                    indicator="dot"
                  />
                }
              />
              <Area
                dataKey="value"
                type="natural"
                fill="url(#fillLiquidado)"
                stroke="var(--color-mobile)"
                stackId="a"
              />
            </AreaChart>
          </ChartContainer>
        </CardContent>
      </Card>
    </div>
  )
}