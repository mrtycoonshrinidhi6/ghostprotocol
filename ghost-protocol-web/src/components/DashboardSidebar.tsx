"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
    LayoutDashboard,
    Skull,
    HardDrive,
    FileText,
    MessageSquare,
    LogOut,
    Menu,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"; // Will need to install Sheet

const sidebarLinks = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "Death Detection", href: "/death-detection", icon: Skull },
    { name: "Asset Discovery", href: "/asset-discovery", icon: HardDrive },
    { name: "Smart Contracts", href: "/smart-contracts", icon: FileText },
    { name: "Memorial Chat", href: "/memorial-chat", icon: MessageSquare },
];

export function DashboardSidebar() {
    return (
        <>
            {/* Desktop Sidebar */}
            <aside className="hidden w-64 border-r bg-background md:block fixed inset-y-0 left-0 z-40">
                <DashboardSidebarContent />
            </aside>

            {/* Mobile Trigger (To be placed in Dashboard Layout Header) */}
            {/* This component is just the sidebar structure. The layout will handle the sheet trigger. */}
        </>
    );
}

// Mobile Sidebar Wrapper
export function MobileSidebar() {
    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="md:hidden">
                    <Menu className="h-6 w-6" />
                </Button>
            </SheetTrigger>
            <SheetContent side="left" className="p-0 w-64">
                <DashboardSidebarContent />
            </SheetContent>
        </Sheet>
    )
}

// Extracted content for reuse
function DashboardSidebarContent() {
    const pathname = usePathname();

    return (
        <div className="flex h-full flex-col justify-between py-6">
            <div className="space-y-6">
                <div className="px-6">
                    <Link href="/" className="flex items-center space-x-2">
                        <span className="text-xl font-bold tracking-tighter text-primary">
                            Ghost Protocol<span className="text-foreground">AI</span>
                        </span>
                    </Link>
                </div>
                <div className="space-y-1 px-3">
                    {sidebarLinks.map((link) => {
                        const Icon = link.icon;
                        const isActive = pathname === link.href;
                        return (
                            <Link
                                key={link.href}
                                href={link.href}
                                className={cn(
                                    "flex items-center space-x-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                                    isActive
                                        ? "bg-primary/10 text-primary"
                                        : "text-muted-foreground hover:bg-muted hover:text-foreground"
                                )}
                            >
                                <Icon className="h-5 w-5" />
                                <span>{link.name}</span>
                            </Link>
                        );
                    })}
                </div>
            </div>
            <div className="px-3">
                <Button variant="ghost" className="w-full justify-start text-muted-foreground hover:text-destructive">
                    <LogOut className="mr-2 h-5 w-5" />
                    Sign Out
                </Button>
            </div>
        </div>
    )
}
