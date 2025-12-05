import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="border-b bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <svg className="h-10 w-10" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M8 20C8 18.8954 8.89543 18 10 18C11.1046 18 12 18.8954 12 20C12 21.1046 11.1046 22 10 22C8.89543 22 8 21.1046 8 20Z"
                fill="#9333EA"
              />
              <path
                d="M16 16C16 14.8954 16.8954 14 18 14C19.1046 14 20 14.8954 20 16C20 17.1046 19.1046 18 18 18C16.8954 18 16 17.1046 16 16Z"
                fill="#9333EA"
              />
              <path
                d="M24 20C24 18.8954 24.8954 18 26 18C27.1046 18 28 18.8954 28 20C28 21.1046 27.1046 22 26 22C24.8954 22 24 21.1046 24 20Z"
                fill="#9333EA"
              />
              <path d="M10 24L18 20L26 24" stroke="#9333EA" strokeWidth="2" strokeLinecap="round" />
            </svg>
            <div>
              <div className="text-lg font-bold leading-tight text-black">Warm leads</div>
              <div className="text-lg font-bold leading-tight text-black">Sourcer</div>
            </div>
          </div>
          <div className="flex items-center gap-8">
            <Link href="#" className="text-sm text-gray-700 hover:text-black">
              Home
            </Link>
            <Link href="#" className="text-sm text-gray-700 hover:text-black">
              About Us
            </Link>
            <Link href="#" className="text-sm text-gray-700 hover:text-black">
              How it works
            </Link>
            <Link href="#" className="text-sm text-gray-700 hover:text-black">
              Privacy & Legal
            </Link>
            <Button className="rounded-lg bg-purple-500 px-8 py-2 text-white hover:bg-purple-600">Login</Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section
        className="relative min-h-[600px] bg-cover bg-center"
        style={{ backgroundImage: "url(/images/landing_page.png)" }}
      >
        <div className="absolute inset-0 bg-black/50" />
        <div className="relative mx-auto flex max-w-7xl flex-col items-center justify-center px-6 py-32 text-center">
          <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-pink-500 to-purple-600">
            <span className="text-2xl font-bold text-white">N</span>
          </div>
          <h1 className="mb-12 text-5xl font-bold leading-tight text-white">
            Turn Social Engagement Into
            <br />
            Warm Leads _ Instanly
          </h1>
          <div className="flex gap-4">
            <Button
              variant="outline"
              className="rounded-lg border-2 border-white bg-transparent px-12 py-6 text-lg text-white hover:bg-white/10"
            >
              &nbsp;
            </Button>
            <Button className="rounded-lg bg-purple-500 px-12 py-6 text-lg text-white hover:bg-purple-600">
              Start Extraction
            </Button>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-gray-50 px-6 py-20">
        <div className="mx-auto max-w-7xl">
          <h2 className="mb-12 text-center text-4xl font-bold text-black">How It Works</h2>
          <div className="grid gap-6 md:grid-cols-3">
            <div className="rounded-lg bg-white p-8 shadow-lg">
              <h3 className="text-2xl font-semibold text-black">
                Paste a public
                <br />
                post URL
              </h3>
            </div>
            <div className="rounded-lg bg-white p-8 shadow-lg">
              <h3 className="text-2xl font-semibold text-black">
                We extract
                <br />
                reactions + do
                <br />
                public-only
                <br />
                enrichment
              </h3>
            </div>
            <div className="rounded-lg bg-white p-8 shadow-lg">
              <h3 className="text-2xl font-semibold text-black">
                Download a<br />
                clean CSV/
                <br />
                XLSX lead list
              </h3>
              <Button className="mt-4 rounded-md bg-gray-300 px-6 py-2 text-black hover:bg-gray-400">Download</Button>
            </div>
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="bg-white px-6 py-20">
        <div className="mx-auto max-w-7xl">
          <h2 className="mb-12 text-center text-4xl font-bold text-black">Use cases</h2>
          <div className="grid gap-12 md:grid-cols-3">
            <div className="text-center">
              <h3 className="mb-4 text-xl font-bold text-black">Recruiters</h3>
              <p className="text-sm text-gray-700">Find talent from engagement</p>
            </div>
            <div className="text-center">
              <h3 className="mb-4 text-xl font-bold text-black">Founders</h3>
              <p className="text-sm text-gray-700">
                See who interacted with your
                <br />
                thought-leadership posts.
              </p>
            </div>
            <div className="text-center">
              <h3 className="mb-4 text-xl font-bold text-black">Growth/BD</h3>
              <p className="text-sm text-gray-700">
                Prioritize people already warmed
                <br />
                up
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Compliance Section */}
      <section className="bg-white px-6 py-20">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="mb-8 text-3xl font-bold text-black">Compliance & Privacy Section</h2>
          <ul className="space-y-2 text-left text-sm text-gray-700">
            <li>• Public-only data disclaimer</li>
            <li>• No private data scraping</li>
            <li>• Temporary PII storage</li>
            <li>• 30-day auto-deletion</li>
            <li>• Clear "export/delete request" instructions</li>
          </ul>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-purple-200 px-6 py-12">
        <div className="mx-auto flex max-w-7xl items-start justify-between">
          <div className="flex items-center gap-2">
            <svg className="h-10 w-10" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M8 20C8 18.8954 8.89543 18 10 18C11.1046 18 12 18.8954 12 20C12 21.1046 11.1046 22 10 22C8.89543 22 8 21.1046 8 20Z"
                fill="#9333EA"
              />
              <path
                d="M16 16C16 14.8954 16.8954 14 18 14C19.1046 14 20 14.8954 20 16C20 17.1046 19.1046 18 18 18C16.8954 18 16 17.1046 16 16Z"
                fill="#9333EA"
              />
              <path
                d="M24 20C24 18.8954 24.8954 18 26 18C27.1046 18 28 18.8954 28 20C28 21.1046 27.1046 22 26 22C24.8954 22 24 21.1046 24 20Z"
                fill="#9333EA"
              />
              <path d="M10 24L18 20L26 24" stroke="#9333EA" strokeWidth="2" strokeLinecap="round" />
            </svg>
            <div>
              <div className="text-lg font-bold leading-tight text-black">Warm leads</div>
              <div className="text-lg font-bold leading-tight text-black">Sourcer</div>
            </div>
          </div>
          <div className="flex flex-col gap-3 text-right text-sm text-black">
            <Link href="#" className="hover:underline">
              Privacy Policy
            </Link>
            <Link href="#" className="hover:underline">
              Legal/Ethical Notice
            </Link>
            <Link href="#" className="hover:underline">
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
