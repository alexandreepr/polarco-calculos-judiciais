import * as React from "react"
import {
  ArrowUpCircleIcon,
  CalendarDaysIcon,
  CameraIcon,
  FileCodeIcon,
  FileIcon,
  FileTextIcon,
  BanknoteArrowDownIcon,
  HelpCircleIcon,
  LayoutDashboardIcon,
  ScaleIcon,
  SearchIcon,
  SettingsIcon,
  CircleQuestionMarkIcon,
} from "lucide-react"

import { NavDocuments } from "@/components/layout/Nav/NavDocuments"
import { NavMain } from "@/components/layout/Nav/NavMain"
import { NavSecondary } from "@/components/layout/Nav/NavSecondary"
import { NavUser } from "@/components/layout/Nav/NavUser"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import { Avatar, AvatarImage } from "@/components/ui/avatar"

const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  navMain: [
    {
      title: "Dashboard",
      url: "#",
      icon: LayoutDashboardIcon,
    },
    {
      title: "Processos",
      url: "#",
      icon: ScaleIcon,
    },
    {
      title: "Agenda",
      url: "#",
      icon: CalendarDaysIcon,
    },
    {
      title: "Despesas",
      url: "#",
      icon: BanknoteArrowDownIcon,
    },
    {
      title: "Relatórios",
      url: "#",
      icon: FileIcon,
    },
  ],
  navClouds: [
    {
      title: "Capture",
      icon: CameraIcon,
      isActive: true,
      url: "#",
      items: [
        {
          title: "Active Proposals",
          url: "#",
        },
        {
          title: "Archived",
          url: "#",
        },
      ],
    },
    {
      title: "Proposal",
      icon: FileTextIcon,
      url: "#",
      items: [
        {
          title: "Active Proposals",
          url: "#",
        },
        {
          title: "Archived",
          url: "#",
        },
      ],
    },
    {
      title: "Prompts",
      icon: FileCodeIcon,
      url: "#",
      items: [
        {
          title: "Active Proposals",
          url: "#",
        },
        {
          title: "Archived",
          url: "#",
        },
      ],
    },
  ],
  navSecondary: [
    {
      title: "Settings",
      url: "#",
      icon: SettingsIcon,
    },
    {
      title: "Get Help",
      url: "#",
      icon: HelpCircleIcon,
    },
    {
      title: "Search",
      url: "#",
      icon: SearchIcon,
    },
  ],
  documents: [
    {
      name: "FAQ | Treinamento",
      url: "#",
      icon: CircleQuestionMarkIcon,
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    // Fix width
    <Sidebar collapsible="offcanvas" className="w-200" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <a href="#">
                <Avatar className="h-7 w-7">
                  <AvatarImage src="/src/assets/Logo_PBL_Fundo_Verde.jpg" alt="Logo" />
                </Avatar>
                <span className="text-base font-semibold">PBL Compra de Créditos Judiciais</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
        <NavDocuments items={data.documents} />
        <NavSecondary items={data.navSecondary} className="mt-auto" />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
    </Sidebar>
  )
}