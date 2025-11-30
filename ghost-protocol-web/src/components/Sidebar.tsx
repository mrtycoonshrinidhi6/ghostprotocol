"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Skull, HardDrive, FileText, MessageSquare, X } from "lucide-react";
import clsx from "clsx";

const navigation = [
    { name: "Dashboard", href: "/", icon: LayoutDashboard },
    { name: "Death Detection", href: "/death-detection", icon: Skull },
    { name: "Asset Discovery", href: "/asset-discovery", icon: HardDrive },
    { name: "Smart Contract", href: "/smart-contract", icon: FileText },
    { name: "Memorial Chat", href: "/memorial-chat", icon: MessageSquare },
];

interface SidebarProps {
    isOpen: boolean;
    onClose: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
    const pathname = usePathname();

    return (
        <>
            {/* Mobile backdrop */}
            <div
                className={clsx(
                    "fixed inset-0 z-40 bg-gray-900/50 transition-opacity lg:hidden",
                    isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
                )}
                onClick={onClose}
            />

            {/* Sidebar */}
            <div
                className={clsx(
                    "fixed inset-y-0 left-0 z-50 w-64 transform bg-white border-r border-border transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0",
                    isOpen ? "translate-x-0" : "-translate-x-full"
                )}
            >
                <div className="flex h-16 items-center justify-between px-6 border-b border-border">
                    <span className="text-xl font-bold text-primary">Ghost Protocol</span>
                    <button onClick={onClose} className="lg:hidden text-secondary">
                        <X className="h-6 w-6" />
                    </button>
                </div>

                <nav className="flex-1 space-y-1 px-3 py-4">
                    {navigation.map((item) => {
                        const isActive = pathname === item.href;
                        return (
                            <Link
                                key={item.name}
                                href={item.href}
                                className={clsx(
                                    "group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                                    isActive
                                        ? "bg-primary-light text-primary"
                                        : "text-secondary hover:bg-gray-50 hover:text-primary"
                                )}
                            >
                                <item.icon
                                    className={clsx(
                                        "mr-3 h-5 w-5 flex-shrink-0 transition-colors",
                                        isActive ? "text-primary" : "text-secondary group-hover:text-primary"
                                    )}
                                />
                                {item.name}
                            </Link>
                        );
                    })}
                </nav>

                <div className="p-4 border-t border-border">
                    <div className="flex items-center">
                        <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">
                            U
                        </div>
                        <div className="ml-3">
                            <p className="text-sm font-medium text-text-primary">User Demo</p>
                            <p className="text-xs text-text-secondary">Premium Plan</p>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
