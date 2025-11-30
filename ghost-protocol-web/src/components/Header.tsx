"use client";

import { Menu } from "lucide-react";

interface HeaderProps {
    onMenuClick: () => void;
}

export default function Header({ onMenuClick }: HeaderProps) {
    return (
        <header className="flex h-16 items-center justify-between border-b border-border bg-white px-4 lg:hidden">
            <div className="flex items-center">
                <button
                    onClick={onMenuClick}
                    className="text-secondary hover:text-primary focus:outline-none"
                >
                    <Menu className="h-6 w-6" />
                </button>
                <span className="ml-4 text-lg font-bold text-primary">Ghost Protocol</span>
            </div>
        </header>
    );
}
