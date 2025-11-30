import { DashboardSidebar, MobileSidebar } from "@/components/DashboardSidebar";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex min-h-screen bg-background">
            <DashboardSidebar />
            <div className="flex flex-1 flex-col md:pl-64">
                {/* Mobile Header */}
                <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background px-6 md:hidden">
                    <MobileSidebar />
                    <span className="font-bold">Ghost Protocol AI</span>
                </header>
                <main className="flex-1 p-6 md:p-8">{children}</main>
            </div>
        </div>
    );
}
