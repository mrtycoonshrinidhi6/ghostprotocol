import Link from "next/link";

export function Footer() {
    return (
        <footer className="border-t bg-background py-12">
            <div className="container flex flex-col items-center justify-between gap-4 md:flex-row">
                <div className="flex flex-col items-center gap-2 md:items-start">
                    <span className="text-lg font-bold tracking-tighter text-primary">
                        GhostProtocol <span className="text-foreground">AI</span>
                    </span>
                    <p className="text-center text-sm text-muted-foreground md:text-left">
                        Autonomous digital legacy infrastructure.
                    </p>
                </div>
                <div className="flex gap-4 text-sm text-muted-foreground">
                    <Link href="/privacy-policy" className="hover:text-foreground">
                        Privacy Policy
                    </Link>
                    <Link href="/terms-of-service" className="hover:text-foreground">
                        Terms of Service
                    </Link>
                    <Link href="/contact" className="hover:text-foreground">
                        Contact
                    </Link>
                </div>
                <div className="text-sm text-muted-foreground">
                    &copy; {new Date().getFullYear()} Ghost Protocol AI. All rights reserved.
                </div>
            </div>
        </footer>
    );
}
