import { Github, Linkedin, Mail, Twitter } from "lucide-react";
import Link from "next/link";

export default function ContactPage() {
    return (
        <div className="container flex min-h-[calc(100vh-200px)] flex-col items-center justify-center py-12 md:py-24">
            <div className="mx-auto max-w-2xl text-center">
                <h1 className="mb-6 text-4xl font-bold tracking-tighter sm:text-5xl">Contact Us</h1>
                <p className="mb-12 text-lg text-muted-foreground">
                    Ghost Protocol is built by a solo developer passionate about AI agents and blockchain.
                    We&apos;d love to hear from you.
                </p>

                <div className="grid gap-8 sm:grid-cols-3">
                    <Link
                        href="mailto:mrtycoonshrinidhi.6@gmail.com"
                        className="group flex flex-col items-center gap-4 rounded-xl border bg-card p-6 shadow-sm transition-all hover:shadow-md"
                    >
                        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                            <Mail className="h-6 w-6" />
                        </div>
                        <div className="space-y-1">
                            <h3 className="font-semibold">Email</h3>
                            <p className="text-sm text-muted-foreground">mrtycoonshrinidhi.6@gmail.com</p>
                        </div>
                    </Link>

                    <Link
                        href="https://twitter.com/mr_tycoon006"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="group flex flex-col items-center gap-4 rounded-xl border bg-card p-6 shadow-sm transition-all hover:shadow-md"
                    >
                        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                            <Twitter className="h-6 w-6" />
                        </div>
                        <div className="space-y-1">
                            <h3 className="font-semibold">Twitter</h3>
                            <p className="text-sm text-muted-foreground">@mr_tycoon006</p>
                        </div>
                    </Link>

                    <Link
                        href="https://www.linkedin.com/in/shrinidhi-h-v"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="group flex flex-col items-center gap-4 rounded-xl border bg-card p-6 shadow-sm transition-all hover:shadow-md"
                    >
                        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                            <Linkedin className="h-6 w-6" />
                        </div>
                        <div className="space-y-1">
                            <h3 className="font-semibold">LinkedIn</h3>
                            <p className="text-sm text-muted-foreground">Shrinidhi H V</p>
                        </div>
                    </Link>
                </div>

                <div className="mt-12 flex justify-center">
                    <Link
                        href="https://github.com/mrtycoonshrinidhi6/ghostprotocol"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
                    >
                        <Github className="h-5 w-5" />
                        <span>View on GitHub</span>
                    </Link>
                </div>
            </div>
        </div>
    );
}
