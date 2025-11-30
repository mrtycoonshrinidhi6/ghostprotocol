import { SpotlightCard } from "@/components/ui/SpotlightCard";
import { DocumentationViewer } from "@/components/DocumentationViewer";
import { Brain, FileSearch, HeartHandshake, ScrollText, ShieldAlert, Users } from "lucide-react";

export default function HowItWorksPage() {
    return (
        <div className="flex min-h-screen flex-col">
            {/* Hero Section */}
            <section className="relative flex flex-col items-center justify-center overflow-hidden bg-background py-24 md:py-32">
                <div className="container relative z-10 flex flex-col items-center text-center">
                    <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl">
                        How <span className="text-primary">Ghost Protocol</span> Works
                    </h1>
                    <p className="mt-6 max-w-[800px] text-lg text-muted-foreground md:text-xl">
                        An autonomous multi-agent AI system that secures your digital legacy.
                        From death detection to asset distribution, we handle it all.
                    </p>
                </div>
                <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/20 via-background to-background" />
            </section>

            {/* Problem & Solution */}
            <section className="container py-12 md:py-24">
                <div className="grid gap-12 md:grid-cols-2">
                    <div className="space-y-4">
                        <h2 className="text-3xl font-bold tracking-tighter">The Problem</h2>
                        <p className="text-muted-foreground">
                            What happens to your digital life after you die?
                        </p>
                        <ul className="list-disc space-y-2 pl-6 text-muted-foreground">
                            <li>2.7 billion digital accounts will be &quot;orphaned&quot; by 2100</li>
                            <li>$10 trillion in digital assets (crypto, NFTs) at risk of being lost</li>
                            <li>Families spend 100+ hours manually closing accounts</li>
                            <li>No automated system exists to execute digital wills</li>
                        </ul>
                    </div>
                    <div className="space-y-4">
                        <h2 className="text-3xl font-bold tracking-tighter">The Solution</h2>
                        <p className="text-muted-foreground">
                            Ghost Protocol is an autonomous multi-agent AI system that detects your death,
                            discovers your digital assets, sends personalized farewell messages through an AI twin,
                            and executes a blockchain-based smart contract to distribute assets to beneficiaries.
                        </p>
                    </div>
                </div>
            </section>

            {/* Key Features */}
            <section className="bg-muted/50 py-12 md:py-24">
                <div className="container">
                    <h2 className="mb-12 text-center text-3xl font-bold tracking-tighter">Key Features</h2>
                    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                        <SpotlightCard className="p-6">
                            <div className="flex flex-col gap-4">
                                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary">
                                    <ShieldAlert className="h-6 w-6" />
                                </div>
                                <h3 className="text-xl font-bold">Automated Death Detection</h3>
                                <p className="text-muted-foreground">
                                    Multi-source verification with 95%+ confidence using obituary scanning, social media monitoring, and government registries.
                                </p>
                            </div>
                        </SpotlightCard>
                        <SpotlightCard className="p-6">
                            <div className="flex flex-col gap-4">
                                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary">
                                    <FileSearch className="h-6 w-6" />
                                </div>
                                <h3 className="text-xl font-bold">Digital Asset Discovery</h3>
                                <p className="text-muted-foreground">
                                    Scans email, cloud storage, crypto wallets, and social media to create a comprehensive inventory of your digital estate.
                                </p>
                            </div>
                        </SpotlightCard>
                        <SpotlightCard className="p-6">
                            <div className="flex flex-col gap-4">
                                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary">
                                    <Brain className="h-6 w-6" />
                                </div>
                                <h3 className="text-xl font-bold">AI Memorial Twin</h3>
                                <p className="text-muted-foreground">
                                    Sends personalized farewell messages in your voice to loved ones, trained on your communication style.
                                </p>
                            </div>
                        </SpotlightCard>
                        <SpotlightCard className="p-6">
                            <div className="flex flex-col gap-4">
                                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary">
                                    <ScrollText className="h-6 w-6" />
                                </div>
                                <h3 className="text-xl font-bold">Smart Contract Execution</h3>
                                <p className="text-muted-foreground">
                                    Blockchain-based will with a 30-day time-lock to ensure secure and immutable distribution of assets.
                                </p>
                            </div>
                        </SpotlightCard>
                        <SpotlightCard className="p-6">
                            <div className="flex flex-col gap-4">
                                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary">
                                    <Users className="h-6 w-6" />
                                </div>
                                <h3 className="text-xl font-bold">Multi-Sig Validation</h3>
                                <p className="text-muted-foreground">
                                    Requires confirmation from 2+ trusted validators (family/friends) to prevent false triggers.
                                </p>
                            </div>
                        </SpotlightCard>
                        <SpotlightCard className="p-6">
                            <div className="flex flex-col gap-4">
                                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary">
                                    <HeartHandshake className="h-6 w-6" />
                                </div>
                                <h3 className="text-xl font-bold">Dead-Man Switch</h3>
                                <p className="text-muted-foreground">
                                    Auto-triggers the protocol after 90 days of inactivity if no check-in is received.
                                </p>
                            </div>
                        </SpotlightCard>
                    </div>
                </div>
            </section>

            {/* Architecture */}
            <section className="container py-12 md:py-24">
                <h2 className="mb-12 text-center text-3xl font-bold tracking-tighter">System Architecture</h2>
                <div className="rounded-xl border bg-card p-8 text-card-foreground shadow">
                    <pre className="overflow-x-auto rounded-lg bg-muted p-4 text-sm">
                        {`User Setup → Monitoring Loop → Death Detection → Asset Scan → AI Messages + Will Execution
                   ↑_____________|                                        |
                   (30-day health check)                    (Beneficiaries notified)`}
                    </pre>
                    <div className="mt-8 space-y-4">
                        <h3 className="text-xl font-bold">Multi-Agent Pipeline</h3>
                        <ul className="list-decimal space-y-2 pl-6 text-muted-foreground">
                            <li>
                                <strong>DeathDetectionAgent:</strong> Monitors obituaries, social media, and registries.
                            </li>
                            <li>
                                <strong>DigitalAssetAgent:</strong> Scans emails, wallets, and cloud storage for assets.
                            </li>
                            <li>
                                <strong>LegacyAgent:</strong> Generates personalized messages using an AI twin.
                            </li>
                            <li>
                                <strong>SmartContractAgent:</strong> Executes the blockchain will and distributes assets.
                            </li>
                        </ul>
                    </div>
                </div>
            </section>

            {/* Documentation */}
            <section className="container py-12 md:py-24">
                <h2 className="mb-12 text-center text-3xl font-bold tracking-tighter">Detailed Documentation</h2>
                <DocumentationViewer />
            </section>
        </div>
    );
}
