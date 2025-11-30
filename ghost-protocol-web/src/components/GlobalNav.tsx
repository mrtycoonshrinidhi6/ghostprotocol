"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Menu, X } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

const navLinks = [
    { name: "How it Works", href: "/how-it-works" },
    { name: "Dashboard", href: "/dashboard" },
    { name: "Death Detection", href: "/death-detection" },
    { name: "Asset Discovery", href: "/asset-discovery" },
    { name: "Smart Contracts", href: "/smart-contracts" },
    { name: "Memorial Chat", href: "/memorial-chat" },
];

export function GlobalNav() {
    const [isOpen, setIsOpen] = useState(false);
    const pathname = usePathname();

    return (
        <nav className="sticky top-0 z-50 w-full border-b bg-background/80 backdrop-blur-md">
            <div className="container flex h-16 items-center justify-between">
                {/* Logo */}
                <Link href="/" className="flex items-center space-x-2">
                    <span className="text-xl font-bold tracking-tighter text-primary">
                        Ghost Protocol<span className="text-foreground">AI</span>
                    </span>
                </Link>

                {/* Desktop Links */}
                <div className="hidden md:flex md:items-center md:space-x-6">
                    {navLinks.map((link) => (
                        <Link
                            key={link.href}
                            href={link.href}
                            className={cn(
                                "text-sm font-medium transition-colors hover:text-primary",
                                pathname === link.href
                                    ? "text-foreground"
                                    : "text-muted-foreground"
                            )}
                        >
                            {link.name}
                        </Link>
                    ))}
                </div>

                {/* CTA */}
                <div className="hidden md:flex">
                    <Link href="/dashboard">
                        <Button>Launch App</Button>
                    </Link>
                </div>

                {/* Mobile Menu Toggle */}
                <button
                    className="md:hidden"
                    onClick={() => setIsOpen(!isOpen)}
                    aria-label="Toggle menu"
                >
                    {isOpen ? (
                        <X className="h-6 w-6 text-foreground" />
                    ) : (
                        <Menu className="h-6 w-6 text-foreground" />
                    )}
                </button>
            </div>

            {/* Mobile Menu */}
            {isOpen && (
                <div className="border-b bg-background md:hidden">
                    <div className="container flex flex-col space-y-4 py-4">
                        {navLinks.map((link) => (
                            <Link
                                key={link.href}
                                href={link.href}
                                className="text-sm font-medium text-foreground hover:text-primary"
                                onClick={() => setIsOpen(false)}
                            >
                                {link.name}
                            </Link>
                        ))}
                        <Link href="/dashboard" onClick={() => setIsOpen(false)}>
                            <Button className="w-full">Launch App</Button>
                        </Link>
                    </div>
                </div>
            )}
        </nav>
    );
}
