import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Image from "next/image"

export default function LoginPage() {
  return (
    <div className="flex min-h-screen">
      {/* Left Side - Form */}
      <div className="flex w-full items-center justify-center bg-gray-50 p-8 lg:w-1/2">
        <div className="w-full max-w-md space-y-6">
          <div className="mb-8">
            <h1 className="text-xl font-bold text-black">WELCOME BACK!</h1>
          </div>

          <div className="space-y-5">
            <div className="space-y-2">
              <label htmlFor="username" className="text-sm font-medium text-black">
                Username
              </label>
              <Input
                id="username"
                type="text"
                placeholder="username"
                className="w-full rounded-md border-0 bg-purple-100 px-4 py-3 text-sm placeholder:text-gray-500"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium text-black">
                Email
              </label>
              <Input
                id="email"
                type="email"
                placeholder="name@gmail.com"
                className="w-full rounded-md border-0 bg-purple-100 px-4 py-3 text-sm placeholder:text-gray-500"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium text-black">
                Password
              </label>
              <div className="relative">
                <Input
                  id="password"
                  type="password"
                  placeholder="password"
                  className="w-full rounded-md border-0 bg-purple-100 px-4 py-3 pr-10 text-sm placeholder:text-gray-500"
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-purple-400 hover:text-purple-600"
                  aria-label="Toggle password visibility"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                </button>
              </div>
              <div className="text-right">
                <Link href="#" className="text-xs text-purple-600 hover:underline">
                  forgot password?
                </Link>
              </div>
            </div>

            <Button className="w-full rounded-md bg-purple-600 py-6 text-sm font-semibold text-white hover:bg-purple-700">
              CONFIRM
            </Button>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-xs">
                <span className="bg-gray-50 px-2 text-gray-500">or</span>
              </div>
            </div>

            <Button
              variant="outline"
              className="w-full rounded-md border-2 border-gray-300 bg-white py-6 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              <svg className="mr-2 h-5 w-5" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              SIGN IN WITH GOOGLE
            </Button>
          </div>
        </div>
      </div>

      {/* Right Side - Image */}
      <div className="hidden w-1/2 bg-linear-to-br from-gray-100 to-gray-200 lg:block">
        <div className="flex h-full items-center justify-center p-12">
          <div className="relative">
            <Image
              src="/phone-social-laptop.png"
              alt="Phone showing social media apps on laptop with hearts"
              width={800}
              height={800}
              className="object-contain"
              priority
            />
          </div>
        </div>
      </div>
    </div>
  )
}
