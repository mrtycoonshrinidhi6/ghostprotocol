import { ExternalLink } from "lucide-react";
import Link from "next/link";

export default function MemorialChatPage() {
    const chatUrl = "https://gemini.google.com/app?is_sa=1&is_sa=1&android-min-version=301356232&ios-min-version=322.0&campaign_id=bkws&utm_source=sem&utm_source=google&utm_medium=paid-media&utm_medium=cpc&utm_campaign=bkws&utm_campaign=2024enIN_gemfeb&pt=9008&mt=8&ct=p-growth-sem-bkws&gclsrc=aw.ds&gad_source=1&gad_campaignid=20357620749&gbraid=0AAAAApk5BhlSvr4r8AJWMBTSwfbn3YKde&gclid=EAIaIQobChMI_7Kkh8uakQMV0ZVLBR3fWBY8EAAYASAAEgJ4rPD_BwE";

    return (
        <div className="flex h-[calc(100vh-4rem)] flex-col">
            <div className="border-b bg-background p-4">
                <div className="container flex items-center justify-between">
                    <div>
                        <h1 className="text-xl font-bold">Memorial Chat</h1>
                        <p className="text-sm text-muted-foreground">
                            Chat with the AI Twin (Powered by Gemini)
                        </p>
                    </div>
                    <Link
                        href={chatUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
                    >
                        Open in New Window <ExternalLink className="h-4 w-4" />
                    </Link>
                </div>
            </div>
            <div className="relative flex-1 bg-muted/20">
                <iframe
                    src={chatUrl}
                    className="absolute inset-0 h-full w-full border-0"
                    title="Memorial Chat"
                    allow="microphone; camera"
                    sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
                />
                <div className="absolute inset-0 -z-10 flex items-center justify-center text-muted-foreground">
                    <p>Loading chat interface...</p>
                </div>
            </div>
        </div>
    );
}
