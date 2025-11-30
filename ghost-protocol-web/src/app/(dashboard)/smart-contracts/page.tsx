"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { FileText, Shield, Clock, CheckCircle, ExternalLink, Loader2 } from "lucide-react";
import { deployContract, getContractStatus } from "@/lib/api";

export default function SmartContractsPage() {
    const [deploying, setDeploying] = useState(false);
    const [contractAddress, setContractAddress] = useState<string | null>(null);
    const [status, setStatus] = useState("Draft");

    const handleDeploy = async () => {
        setDeploying(true);
        try {
            // Simulate deployment delay
            await new Promise(resolve => setTimeout(resolve, 3000));
            const result = await deployContract("user_123", "session_123");
            setContractAddress(result.contract_address || "0x71C...9A2"); // Fallback if mock is empty
            setStatus("Active");
        } catch (error) {
            console.error("Deployment failed", error);
        } finally {
            setDeploying(false);
        }
    };

    return (
        <div className="space-y-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Smart Contracts</h1>
                    <p className="text-muted-foreground">
                        Immutable execution of digital will protocols.
                    </p>
                </div>
            </div>

            <div className="grid gap-8 md:grid-cols-3">
                {/* Main Contract Card */}
                <Card className="md:col-span-2">
                    <CardHeader>
                        <CardTitle>Digital Will Contract</CardTitle>
                        <CardDescription>
                            Current active protocol for asset distribution.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="rounded-lg border p-4 bg-muted/30">
                            <div className="flex items-center justify-between mb-4">
                                <div className="flex items-center space-x-2">
                                    <FileText className="h-5 w-5 text-primary" />
                                    <span className="font-semibold">Protocol v2.1</span>
                                </div>
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${status === "Active" ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"
                                    }`}>
                                    {status}
                                </span>
                            </div>
                            <div className="space-y-2 text-sm text-muted-foreground">
                                <div className="flex justify-between">
                                    <span>Contract Address</span>
                                    <span className="font-mono">{contractAddress || "Not Deployed"}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span>Timelock Period</span>
                                    <span>30 Days</span>
                                </div>
                                <div className="flex justify-between">
                                    <span>Beneficiaries</span>
                                    <span>3 Wallets</span>
                                </div>
                            </div>
                        </div>

                        <div className="flex justify-end">
                            {!contractAddress ? (
                                <Button onClick={handleDeploy} disabled={deploying}>
                                    {deploying && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                    {deploying ? "Deploying to Mainnet..." : "Deploy Contract"}
                                </Button>
                            ) : (
                                <Button variant="outline" className="space-x-2">
                                    <ExternalLink className="h-4 w-4" />
                                    <span>View on Etherscan</span>
                                </Button>
                            )}
                        </div>
                    </CardContent>
                </Card>

                {/* Validator Status */}
                <div className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-sm font-medium">Multi-Sig Validators</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                {[
                                    { name: "Legal Oracle", status: "Active" },
                                    { name: "Family Key 1", status: "Pending" },
                                    { name: "Family Key 2", status: "Active" },
                                ].map((validator, i) => (
                                    <div key={i} className="flex items-center justify-between text-sm">
                                        <div className="flex items-center space-x-2">
                                            <Shield className="h-4 w-4 text-muted-foreground" />
                                            <span>{validator.name}</span>
                                        </div>
                                        {validator.status === "Active" ? (
                                            <CheckCircle className="h-4 w-4 text-green-500" />
                                        ) : (
                                            <Clock className="h-4 w-4 text-yellow-500" />
                                        )}
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>

            {/* Transaction History */}
            <Card>
                <CardHeader>
                    <CardTitle>Execution Log</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Event</TableHead>
                                <TableHead>Hash</TableHead>
                                <TableHead>Time</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {contractAddress ? (
                                <TableRow>
                                    <TableCell>Contract Deployment</TableCell>
                                    <TableCell className="font-mono text-xs">0x8a...3b1</TableCell>
                                    <TableCell>Just now</TableCell>
                                    <TableCell><span className="text-green-600">Confirmed</span></TableCell>
                                </TableRow>
                            ) : (
                                <TableRow>
                                    <TableCell colSpan={4} className="text-center text-muted-foreground">No transactions yet.</TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
