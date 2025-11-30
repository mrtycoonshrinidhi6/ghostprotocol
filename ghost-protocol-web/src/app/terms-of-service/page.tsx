export default function TermsOfServicePage() {
    return (
        <div className="container max-w-3xl py-12 md:py-24">
            <h1 className="mb-8 text-4xl font-bold tracking-tighter">Terms of Service</h1>

            <div className="prose prose-gray dark:prose-invert max-w-none">
                <p className="lead">
                    By using Ghost Protocol, you agree to the following terms and conditions. Please read them carefully.
                </p>

                <h2 className="mt-8 text-2xl font-bold">1. Service Description</h2>
                <p>
                    Ghost Protocol is an autonomous digital legacy infrastructure designed to detect death, discover assets, and execute digital wills. It is a tool to assist in estate planning but does not replace legal advice or traditional wills.
                </p>

                <h2 className="mt-8 text-2xl font-bold">2. Legal Disclaimer</h2>
                <ul className="list-disc pl-6">
                    <li>
                        <strong>Not a Legal Will:</strong> Ghost Protocol is not a replacement for a legal will. It is a complementary service for managing digital assets. We strongly recommend consulting with a legal professional for comprehensive estate planning.
                    </li>
                    <li>
                        <strong>Family Approval:</strong> The execution of the protocol requires validation from designated family members or trusted individuals (validators).
                    </li>
                </ul>

                <h2 className="mt-8 text-2xl font-bold">3. Security and Liability</h2>
                <ul className="list-disc pl-6">
                    <li>
                        <strong>Multi-Sig Validation:</strong> To prevent false triggers, we employ a multi-signature validation process requiring confirmation from at least 2 validators.
                    </li>
                    <li>
                        <strong>Time-Lock:</strong> A 30-day time-lock is enforced after death confirmation before any assets are distributed, allowing time for intervention if necessary.
                    </li>
                    <li>
                        <strong>Blockchain Audit:</strong> All transactions are recorded on the blockchain for transparency and immutability.
                    </li>
                    <li>
                        <strong>Liability:</strong> Ghost Protocol is not liable for any loss of assets due to incorrect configuration, false validation by designated validators, or blockchain network failures.
                    </li>
                </ul>

                <h2 className="mt-8 text-2xl font-bold">4. User Responsibilities</h2>
                <p>
                    You are responsible for:
                </p>
                <ul className="list-disc pl-6">
                    <li>Providing accurate information about your assets and validators.</li>
                    <li>Ensuring your validators are aware of their role and responsibilities.</li>
                    <li>Keeping your account credentials secure.</li>
                </ul>

                <h2 className="mt-8 text-2xl font-bold">5. Changes to Terms</h2>
                <p>
                    We reserve the right to modify these terms at any time. We will notify you of any significant changes.
                </p>

                <h2 className="mt-8 text-2xl font-bold">Contact Us</h2>
                <p>
                    If you have any questions about our Terms of Service, please contact us at <a href="mailto:mrtycoonshrinidhi.6@gmail.com" className="text-primary hover:underline">mrtycoonshrinidhi.6@gmail.com</a>.
                </p>
            </div>
        </div>
    );
}
