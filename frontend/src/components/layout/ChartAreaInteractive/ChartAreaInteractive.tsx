import * as React from "react"
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts"

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

// Mock data: totals by user
const chartDataByUser = [
  { user: "Alice", comprado: 3200, liquidado: 2800 },
  { user: "Bob", comprado: 4100, liquidado: 3900 },
  { user: "Carol", comprado: 3700, liquidado: 3500 },
  { user: "David", comprado: 2900, liquidado: 2700 },
  { user: "Eve", comprado: 4500, liquidado: 4200 },
]

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

export function ChartAreaInteractive() {
  // const isMobile = useIsMobile()
  const [userRange, setUserRange] = React.useState("all")
  const [userRange2, setUserRange2] = React.useState("all")

  const filteredData = React.useMemo(() => {
    if (userRange === "last3" || userRange2 === "current") {
      return chartDataByUser.slice(0, 3)
    }
    return chartDataByUser
  }, [userRange])

  const filteredData2 = React.useMemo(() => {
    if (userRange2 === "last3" || userRange2 === "current") return chartDataByUser.slice(0, 3)
    return chartDataByUser
  }, [userRange2])

  return (
    <div className="flex flex-col gap-4 md:flex-row">
      <Card className="flex-1 @container/card">
        <CardHeader className="relative">
          <CardTitle>Total Comprado por Usuário</CardTitle>
          <CardDescription>
            <span className="@[540px]/card:block hidden">
              Total comprado por usuário
            </span>
            <span className="@[540px]/card:hidden">Comprado by user</span>
          </CardDescription>
          <div className="absolute right-4 top-4">
            <ToggleGroup
              type="single"
              value={userRange}
              onValueChange={setUserRange}
              variant="outline"
              className="@[767px]/card:flex hidden"
            >
              <ToggleGroupItem value="all" className="h-8 px-2.5">
                Últimos 12 meses
              </ToggleGroupItem>
              <ToggleGroupItem value="top3" className="h-8 px-2.5">
                Últimos 3 meses
              </ToggleGroupItem>
              <ToggleGroupItem value="top3" className="h-8 px-2.5">
                Mês Vigente
              </ToggleGroupItem>
            </ToggleGroup>
            <Select value={userRange} onValueChange={setUserRange}>
              <SelectTrigger
                className="@[767px]/card:hidden flex w-40"
                aria-label="Select a value"
              >
                <SelectValue placeholder="Todos" />
              </SelectTrigger>
              <SelectContent className="rounded-xl">
                <SelectItem value="all" className="rounded-lg">
                  Últimos 12 meses
                </SelectItem>
                <SelectItem value="last3" className="rounded-lg">
                  Últimos 3 meses
                </SelectItem>
                <SelectItem value="current" className="rounded-lg">
                  Mês Vigente
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
            <BarChart data={filteredData}>
              <CartesianGrid vertical={false} />
              <XAxis dataKey="user" tickLine={false} axisLine={false} />
              <YAxis />
              <ChartTooltip
                cursor={false}
                content={
                  <ChartTooltipContent
                    labelFormatter={(value) => value}
                    indicator="dot"
                  />
                }
              />
              <Bar
                dataKey="comprado"
                fill="var(--color-desktop)"
                radius={[4, 4, 0, 0]}
                barSize={40}
              />
            </BarChart>
          </ChartContainer>
        </CardContent>
      </Card>
      <Card className="@container/card flex-1">
        <CardHeader className="relative">
          <CardTitle>Total Liquidado por Usuário</CardTitle>
          <CardDescription>
            <span className="@[540px]/card:block hidden">
              Total liquidado por usuário
            </span>
            <span className="@[540px]/card:hidden">Liquidado by user</span>
          </CardDescription>
          <div className="absolute right-4 top-4">
            <ToggleGroup
              type="single"
              value={userRange2}
              onValueChange={setUserRange2}
              variant="outline"
              className="@[767px]/card:flex hidden"
            >
              <ToggleGroupItem value="all" className="h-8 px-2.5">
                Últimos 12 meses
              </ToggleGroupItem>
              <ToggleGroupItem value="top3" className="h-8 px-2.5">
                Últimos 3 meses
              </ToggleGroupItem>
              <ToggleGroupItem value="top3" className="h-8 px-2.5">
                Mês Vigente
              </ToggleGroupItem>
            </ToggleGroup>
            <Select value={userRange2} onValueChange={setUserRange2}>
              <SelectTrigger
                className="@[767px]/card:hidden flex w-40"
                aria-label="Select a value"
              >
                <SelectValue placeholder="Todos" />
              </SelectTrigger>
              <SelectContent className="rounded-xl">
                <SelectItem value="all" className="rounded-lg">
                  Últimos 12 meses
                </SelectItem>
                <SelectItem value="last3" className="rounded-lg">
                  Últimos 3 meses
                </SelectItem>
                <SelectItem value="current" className="rounded-lg">
                  Mês Vigente
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
            <BarChart data={filteredData2}>
              <CartesianGrid vertical={false} />
              <XAxis dataKey="user" tickLine={false} axisLine={false} />
              <YAxis />
              <ChartTooltip
                cursor={false}
                content={
                  <ChartTooltipContent
                    labelFormatter={(value) => value}
                    indicator="dot"
                  />
                }
              />
              <Bar
                dataKey="liquidado"
                fill="var(--color-mobile)"
                radius={[4, 4, 0, 0]}
                barSize={40}
              />
            </BarChart>
          </ChartContainer>
        </CardContent>
      </Card>
    </div>
  )
}