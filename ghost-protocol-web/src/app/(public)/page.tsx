import Link from "next/link";
import Image from "next/image";
import { ArrowRight, Shield, Activity, Lock, ChevronRight } from "lucide-react";
import { AuroraBackground } from "@/components/ui/AuroraBackground";
import { SplitText } from "@/components/ui/SplitText";
import { SpotlightCard } from "@/components/ui/SpotlightCard";

export default function LandingPage() {
    return (
        <AuroraBackground className="!h-auto min-h-screen">
            <div className="relative z-10 w-full">
                {/* Navigation */}
                <nav className="flex items-center justify-between px-6 py-6 md:px-12">
                    <div className="text-2xl font-bold text-primary">Ghost Protocol</div>
                    <div className="flex items-center space-x-6">
                        <Link href="/login" className="text-sm font-medium text-text-secondary hover:text-primary">
                            Sign In
                        </Link>
                        <Link
                            href="/dashboard"
                            className="rounded-full bg-primary px-6 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-hover"
                        >
                            Launch App
                        </Link>
                    </div>
                </nav>

                {/* Hero Section */}
                <div className="mx-auto max-w-7xl px-6 py-12 md:px-12 md:py-24 lg:flex lg:items-center lg:justify-between">
                    <div className="lg:w-1/2">
                        <div className="inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary">
                            <span className="mr-2 flex h-2 w-2 rounded-full bg-primary"></span>
                            v2.0 Now Live
                        </div>
                        <h1 className="mt-6 text-5xl font-bold tracking-tight text-text-primary md:text-6xl">
                            <SplitText text="Secure Your Digital Legacy" />
                        </h1>
                        <p className="mt-6 text-lg text-text-secondary md:text-xl">
                            The world&apos;s first autonomous digital inheritance protocol. Ensure your assets, memories, and identity live on securely.
                        </p>
                        <div className="mt-8 flex flex-col space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0">
                            <Link
                                href="/dashboard"
                                className="inline-flex items-center justify-center rounded-lg bg-primary px-8 py-3 text-base font-medium text-white transition-all hover:bg-primary-hover hover:shadow-lg"
                            >
                                Get Started
                                <ArrowRight className="ml-2 h-5 w-5" />
                            </Link>
                            <Link
                                href="/how-it-works"
                                className="inline-flex items-center justify-center rounded-lg border border-border bg-white px-8 py-3 text-base font-medium text-text-primary transition-colors hover:bg-gray-50"
                            >
                                How it Works
                            </Link>
                        </div>
                    </div>
                    <div className="mt-12 lg:mt-0 lg:w-1/2">
                        <div className="relative mx-auto max-w-lg">
                            <div className="absolute -inset-4 rounded-xl bg-gradient-to-r from-primary to-purple-600 opacity-20 blur-2xl"></div>
                            <Image
                                src="/hero.png"
                                alt="Digital Legacy Vault"
                                width={600}
                                height={600}
                                className="relative rounded-xl shadow-2xl border border-white/20"
                            />
                        </div>
                    </div>
                </div>

                {/* Features Section */}
                <div className="mx-auto max-w-7xl px-6 py-24 md:px-12">
                    <div className="text-center">
                        <h2 className="text-3xl font-bold text-text-primary">Autonomous Protection</h2>
                        <p className="mt-4 text-lg text-text-secondary">
                            Powered by smart contracts and multi-source verification.
                        </p>
                    </div>

                    <div className="mt-16 grid gap-8 md:grid-cols-3">
                        <SpotlightCard className="p-8">
                            <div className="mb-4 inline-flex rounded-lg bg-blue-100 p-3 text-primary">
                                <Activity className="h-8 w-8" />
                            </div>
                            <h3 className="text-xl font-bold text-text-primary">Death Detection</h3>
                            <p className="mt-4 text-text-secondary">
                                Our oracle network monitors 12+ data sources including government registries and social activity to verify status with 99.9% accuracy.
                            </p>
                            <div className="mt-6 flex items-center text-sm font-medium text-primary">
                                Learn more <ChevronRight className="ml-1 h-4 w-4" />
                            </div>
                        </SpotlightCard>

                        <SpotlightCard className="p-8">
                            <div className="mb-4 inline-flex rounded-lg bg-purple-100 p-3 text-purple-600">
                                <Shield className="h-8 w-8" />
                            </div>
                            <h3 className="text-xl font-bold text-text-primary">Asset Discovery</h3>
                            <p className="mt-4 text-text-secondary">
                                AI agents autonomously scan your cloud accounts and emails to discover forgotten crypto wallets and digital accounts.
                            </p>
                            <div className="mt-6 flex items-center text-sm font-medium text-primary">
                                View Integration <ChevronRight className="ml-1 h-4 w-4" />
                            </div>
                        </SpotlightCard>

                        <SpotlightCard className="p-8">
                            <div className="mb-4 inline-flex rounded-lg bg-green-100 p-3 text-green-600">
                                <Lock className="h-8 w-8" />
                            </div>
                            <h3 className="text-xl font-bold text-text-primary">Smart Will</h3>
                            <p className="mt-4 text-text-secondary">
                                Trustless execution of your will on the Polygon blockchain. Assets are transferred automatically to verified beneficiaries.
                            </p>
                            <div className="mt-6 flex items-center text-sm font-medium text-primary">
                                View Contract <ChevronRight className="ml-1 h-4 w-4" />
                            </div>
                        </SpotlightCard>
                    </div>
                </div>
            </div>
        </AuroraBackground>
    );
}
