export default function PrivacyPolicyPage() {
    return (
        <div className="container max-w-3xl py-12 md:py-24">
            <h1 className="mb-8 text-4xl font-bold tracking-tighter">Privacy Policy</h1>

            <div className="prose prose-gray dark:prose-invert max-w-none">
                <p className="lead">
                    At Ghost Protocol, we take your privacy and security seriously. Given the sensitive nature of digital estate planning, we have implemented strict measures to ensure your data remains secure and private.
                </p>

                <h2 className="mt-8 text-2xl font-bold">Data Security</h2>
                <ul className="list-disc pl-6">
                    <li>
                        <strong>Encryption at Rest:</strong> All sensitive credentials, including passwords and private keys, are encrypted using industry-standard encryption protocols before being stored in our database.
                    </li>
                    <li>
                        <strong>No Third-Party Sharing:</strong> We do not share, sell, or rent your personal data to third parties. Your data is used solely for the purpose of executing your digital will.
                    </li>
                    <li>
                        <strong>User Control:</strong> You have full control over your data. You can request the deletion of your memory bank and account data at any time.
                    </li>
                </ul>

                <h2 className="mt-8 text-2xl font-bold">Information We Collect</h2>
                <p>
                    To provide our services, we may collect the following information:
                </p>
                <ul className="list-disc pl-6">
                    <li>Account information (name, email, contact details)</li>
                    <li>Digital asset details (for inventory purposes)</li>
                    <li>Validator contact information</li>
                    <li>Obituary and death registry data (for verification purposes)</li>
                </ul>

                <h2 className="mt-8 text-2xl font-bold">How We Use Your Information</h2>
                <p>
                    We use your information to:
                </p>
                <ul className="list-disc pl-6">
                    <li>Monitor for proof of life or death</li>
                    <li>Verify your identity and the identity of your validators</li>
                    <li>Execute your digital will and distribute assets</li>
                    <li>Generate personalized messages for your beneficiaries</li>
                </ul>

                <h2 className="mt-8 text-2xl font-bold">Contact Us</h2>
                <p>
                    If you have any questions about our Privacy Policy, please contact us at <a href="mailto:mrtycoonshrinidhi.6@gmail.com" className="text-primary hover:underline">mrtycoonshrinidhi.6@gmail.com</a>.
                </p>
            </div>
        </div>
    );
}
