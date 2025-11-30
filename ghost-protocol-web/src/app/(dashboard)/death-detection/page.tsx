"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { AlertCircle, CheckCircle, Loader2, Skull } from "lucide-react";
import { runDeathDetection } from "@/lib/api";
import { cn } from "@/lib/utils";

export default function DeathDetectionPage() {
    const [isRunning, setIsRunning] = useState(false);
    const [confidence, setConfidence] = useState(0);
    const [logs, setLogs] = useState<{ time: string; message: string; status: "pending" | "success" | "warning" }[]>([]);
    const [isComplete, setIsComplete] = useState(false);

    const handleRunDetection = async () => {
        setIsRunning(true);
        setIsComplete(false);
        setConfidence(0);
        setLogs([]);

        // Simulate pipeline steps for UI feedback before/during API call
        const steps = [
            "Initializing multi-agent swarm...",
            "Scanning national obituary registries...",
            "Analyzing social media activity patterns...",
            "Verifying email heartbeat signals...",
            "Cross-referencing government databases...",
        ];

        for (let i = 0; i < steps.length; i++) {
            setLogs((prev) => [
                ...prev,
                { time: new Date().toLocaleTimeString(), message: steps[i], status: "pending" },
            ]);
            await new Promise((resolve) => setTimeout(resolve, 1500));
            setConfidence((prev) => prev + 15);
            setLogs((prev) => {
                const newLogs = [...prev];
                newLogs[newLogs.length - 1].status = "success";
                return newLogs;
            });
        }

        try {
            const result = await runDeathDetection("user_123");
            setConfidence(result.confidence * 100);
            setLogs((prev) => [
                ...prev,
                { time: new Date().toLocaleTimeString(), message: "Verification Complete. Consensus Reached.", status: "success" },
            ]);
        } catch (error) {
            setLogs((prev) => [
                ...prev,
                { time: new Date().toLocaleTimeString(), message: "Error connecting to verification network.", status: "warning" },
            ]);
        } finally {
            setIsRunning(false);
            setIsComplete(true);
        }
    };

    return (
        <div className="space-y-8 max-w-5xl mx-auto">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Death Verification</h1>
                    <p className="text-muted-foreground">
                        Multi-source oracle protocol for biological status confirmation.
                    </p>
                </div>
            </div>

            <div className="grid gap-8 md:grid-cols-3">
                {/* Main Control Panel */}
                <Card className="md:col-span-2">
                    <CardHeader>
                        <CardTitle>Verification Pipeline</CardTitle>
                        <CardDescription>
                            Execute autonomous verification across distributed data sources.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        {!isRunning && !isComplete ? (
                            <div className="flex flex-col items-center justify-center py-12 space-y-4">
                                <div className="h-24 w-24 rounded-full bg-muted flex items-center justify-center">
                                    <Skull className="h-12 w-12 text-muted-foreground" />
                                </div>
                                <div className="text-center space-y-2">
                                    <h3 className="text-lg font-medium">Ready to Verify</h3>
                                    <p className="text-sm text-muted-foreground max-w-sm">
                                        Initiate the 5-step verification protocol. This process is irreversible and logged on the ledger.
                                    </p>
                                </div>
                                <Button size="lg" onClick={handleRunDetection} className="w-full max-w-xs">
                                    Run Multi-Source Verification
                                </Button>
                            </div>
                        ) : (
                            <div className="space-y-6">
                                <div className="space-y-2">
                                    <div className="flex justify-between text-sm">
                                        <span>Verification Confidence</span>
                                        <span className="font-bold">{Math.round(confidence)}%</span>
                                    </div>
                                    <Progress value={confidence} className="h-3" />
                                </div>

                                <div className="rounded-md border bg-muted/50 p-4 h-[300px] overflow-y-auto space-y-3">
                                    {logs.map((log, i) => (
                                        <div key={i} className="flex items-start space-x-3 text-sm animate-in fade-in slide-in-from-bottom-2">
                                            <div className="mt-0.5">
                                                {log.status === "pending" && <Loader2 className="h-4 w-4 animate-spin text-blue-500" />}
                                                {log.status === "success" && <CheckCircle className="h-4 w-4 text-green-500" />}
                                                {log.status === "warning" && <AlertCircle className="h-4 w-4 text-red-500" />}
                                            </div>
                                            <div className="flex-1 space-y-1">
                                                <p className="font-medium">{log.message}</p>
                                                <p className="text-xs text-muted-foreground">{log.time}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                {isComplete && (
                                    <Button className="w-full" variant="outline" onClick={() => { setIsComplete(false); setLogs([]); setConfidence(0); }}>
                                        Reset Protocol
                                    </Button>
                                )}
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Sidebar Stats */}
                <div className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-sm font-medium">Protocol Status</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="flex items-center space-x-2">
                                <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
                                <span className="font-bold">Active</span>
                            </div>
                            <p className="text-xs text-muted-foreground mt-1">
                                All oracles operational
                            </p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-sm font-medium">Required Consensus</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">95%</div>
                            <p className="text-xs text-muted-foreground">
                                Minimum confidence score
                            </p>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
