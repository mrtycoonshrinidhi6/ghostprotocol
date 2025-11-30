"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Activity, ShieldCheck, Users, Zap, AlertCircle } from "lucide-react";
import { getSystemStatus, SystemStatus } from "@/lib/api";
import { cn } from "@/lib/utils";
import Link from "next/link";

export default function DashboardPage() {
    const [status, setStatus] = useState<SystemStatus | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchStatus() {
            try {
                const data = await getSystemStatus();
                setStatus(data);
            } catch (error) {
                console.error("Failed to fetch system status", error);
            } finally {
                setLoading(false);
            }
        }
        fetchStatus();
    }, []);

    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                    <p className="text-muted-foreground">
                        System overview and autonomous agent status.
                    </p>
                </div>
                <div className="flex items-center space-x-2">
                    <div className={cn("flex items-center space-x-2 rounded-full px-3 py-1 text-sm font-medium",
                        status ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400" : "bg-yellow-100 text-yellow-700"
                    )}>
                        <div className={cn("h-2 w-2 rounded-full", status ? "bg-green-500" : "bg-yellow-500 animate-pulse")} />
                        <span>{status ? "System Online" : "Connecting..."}</span>
                    </div>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Active Agents
                        </CardTitle>
                        <Users className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{status?.active_agents || "-"}</div>
                        <p className="text-xs text-muted-foreground">
                            Autonomous processes running
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            System Uptime
                        </CardTitle>
                        <Activity className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{status?.uptime || "-"}</div>
                        <p className="text-xs text-muted-foreground">
                            Since last deployment
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Assets Secured
                        </CardTitle>
                        <ShieldCheck className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{status?.assets_secured || "-"}</div>
                        <p className="text-xs text-muted-foreground">
                            Digital assets protected
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Detection Confidence
                        </CardTitle>
                        <Zap className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">98.5%</div>
                        <p className="text-xs text-muted-foreground">
                            Average verification score
                        </p>
                    </CardContent>
                </Card>
            </div>

            {/* Quick Actions & Activity */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4">
                    <CardHeader>
                        <CardTitle>Quick Actions</CardTitle>
                    </CardHeader>
                    <CardContent className="grid gap-4 md:grid-cols-2">
                        <Link href="/death-detection">
                            <Button className="w-full h-24 flex flex-col items-center justify-center space-y-2" variant="outline">
                                <AlertCircle className="h-8 w-8 text-destructive" />
                                <span className="font-semibold">Run Death Detection</span>
                                <span className="text-xs text-muted-foreground">Trigger verification pipeline</span>
                            </Button>
                        </Link>
                        <Link href="/asset-discovery">
                            <Button className="w-full h-24 flex flex-col items-center justify-center space-y-2" variant="outline">
                                <ShieldCheck className="h-8 w-8 text-primary" />
                                <span className="font-semibold">Scan Assets</span>
                                <span className="text-xs text-muted-foreground">Discover new digital assets</span>
                            </Button>
                        </Link>
                    </CardContent>
                </Card>
                <Card className="col-span-3">
                    <CardHeader>
                        <CardTitle>Recent Activity</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-8">
                            {[
                                { event: "System Health Check", time: "2 mins ago", status: "Success" },
                                { event: "Asset Scan Completed", time: "1 hour ago", status: "Found 3" },
                                { event: "Smart Contract Verified", time: "3 hours ago", status: "Verified" },
                            ].map((item, i) => (
                                <div key={i} className="flex items-center">
                                    <div className="ml-4 space-y-1">
                                        <p className="text-sm font-medium leading-none">{item.event}</p>
                                        <p className="text-sm text-muted-foreground">
                                            {item.time}
                                        </p>
                                    </div>
                                    <div className="ml-auto font-medium text-sm text-muted-foreground">{item.status}</div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
