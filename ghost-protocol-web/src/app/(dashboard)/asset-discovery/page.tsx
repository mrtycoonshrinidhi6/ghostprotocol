"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { HardDrive, RefreshCw, Wallet, Cloud, Mail, Share2 } from "lucide-react";
import { scanAssets, AssetScanResponse } from "@/lib/api";

interface Asset {
    type: string;
    source: string;
    value: string;
    status: string;
}

export default function AssetDiscoveryPage() {
    const [scanning, setScanning] = useState(false);
    const [assets, setAssets] = useState<Asset[]>([]);
    const [summary, setSummary] = useState({ crypto: 0, cloud: 0, social: 0, email: 0 });

    const handleScan = async () => {
        setScanning(true);
        try {
            // Simulate scan delay
            await new Promise(resolve => setTimeout(resolve, 2000));
            const result: AssetScanResponse = await scanAssets("user_123", "session_123");

            // Transform result for table
            const newAssets: Asset[] = [
                ...result.crypto_wallets.map(w => ({ type: "Crypto Wallet", source: w.address, value: "$12,450", status: "Secured" })),
                ...result.cloud_storage.map(c => ({ type: "Cloud Storage", source: c.provider, value: "150 GB", status: "Indexed" })),
                ...result.email_accounts.map(e => ({ type: "Email", source: e.email, value: "Primary", status: "Monitored" })),
            ];
            setAssets(newAssets);
            setSummary({
                crypto: result.crypto_wallets.length,
                cloud: result.cloud_storage.length,
                social: result.social_accounts.length,
                email: result.email_accounts.length
            });

        } catch (error) {
            console.error("Scan failed", error);
        } finally {
            setScanning(false);
        }
    };

    // Initial load (mock)
    useEffect(() => {
        // Pre-load some mock data or fetch existing
        setAssets([
            { type: "Crypto Wallet", source: "0x71C...9A2", value: "$4,200", status: "Secured" },
            { type: "Social Media", source: "Twitter/X", value: "@ghost_user", status: "Linked" },
        ]);
        setSummary({ crypto: 1, cloud: 0, social: 1, email: 0 });
    }, []);

    return (
        <div className="space-y-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Asset Discovery</h1>
                    <p className="text-muted-foreground">
                        Autonomous inventory of distributed digital assets.
                    </p>
                </div>
                <Button onClick={handleScan} disabled={scanning}>
                    {scanning ? <RefreshCw className="mr-2 h-4 w-4 animate-spin" /> : <HardDrive className="mr-2 h-4 w-4" />}
                    {scanning ? "Scanning Network..." : "Scan Digital Assets"}
                </Button>
            </div>

            {/* Summary Cards */}
            <div className="grid gap-4 md:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Crypto Wallets</CardTitle>
                        <Wallet className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{summary.crypto}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Cloud Storage</CardTitle>
                        <Cloud className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{summary.cloud}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Social Accounts</CardTitle>
                        <Share2 className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{summary.social}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Email Accounts</CardTitle>
                        <Mail className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{summary.email}</div>
                    </CardContent>
                </Card>
            </div>

            {/* Asset Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Discovered Assets</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Type</TableHead>
                                <TableHead>Source / Identifier</TableHead>
                                <TableHead>Est. Value / Size</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {assets.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={4} className="text-center h-24 text-muted-foreground">
                                        No assets found. Run a scan to discover assets.
                                    </TableCell>
                                </TableRow>
                            ) : (
                                assets.map((asset, i) => (
                                    <TableRow key={i}>
                                        <TableCell className="font-medium">{asset.type}</TableCell>
                                        <TableCell>{asset.source}</TableCell>
                                        <TableCell>{asset.value}</TableCell>
                                        <TableCell>
                                            <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80">
                                                {asset.status}
                                            </span>
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
