"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Link from "next/link"

export default function AuthFlowPage() {
  const [step, setStep] = useState(1) // 1: email, 2: verify code, 3: reset password
  const [email, setEmail] = useState("")
  const [code, setCode] = useState(["", "", "", ""])
  const [newPassword, setNewPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")

  const handleEmailSubmit = () => {
    if (email) {
      setStep(2)
    }
  }

  const handleCodeSubmit = () => {
    if (code.every(digit => digit !== "")) {
      setStep(3)
    }
  }

  const handleCodeChange = (index: number, value: string) => {
    if (value.length <= 1) {
      const newCode = [...code]
      newCode[index] = value
      setCode(newCode)
      
      // Auto-focus next input
      if (value && index < 3) {
        const nextInput = document.getElementById(`code-${index + 1}`)
        nextInput?.focus()
      }
    }
  }

  const handlePasswordSubmit = () => {
    if (newPassword && confirmPassword && newPassword === confirmPassword) {
      // Handle password reset logic here
      console.log("Password reset successful")
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="ml-8 max-w-sm pt-16 lg:ml-32">
        {/* Step 1: Forgot Password - Email Entry */}
        {step === 1 && (
          <div className="space-y-8">
            <div>
              <h1 className="mb-4 text-xl font-bold text-black">Forgot Password?</h1>
              <p className="text-sm text-gray-600">
                Please verify your email ID to receive a confirmation code to set up new password
              </p>
            </div>

            <div className="space-y-6">
              <div className="space-y-2">
                <label htmlFor="forgot-email" className="text-sm  font-medium text-black">
                  Email Address
                </label>
                <Input
                  id="forgot-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@gmail.com"
                  className="w-full text-black rounded-md border border-gray-300 bg-white px-4 py-3 text-sm"
                />
              </div>

              <Button 
                onClick={handleEmailSubmit}
                className="w-full rounded-md bg-purple-600 py-6 text-sm font-semibold text-white hover:bg-purple-700"
              >
                Confirm Email
              </Button>
            </div>
          </div>
        )}

        {/* Step 2: Verify Email - Code Entry */}
        {step === 2 && (
          <div className="space-y-8">
            <div>
              <h2 className="mb-3 text-xl font-bold text-black">Verify email address</h2>
              <p className="text-sm text-black">
                verification code sent to <span className="text-purple-600">{email}</span>
              </p>
            </div>

            <div className="space-y-6">
              <div className="flex gap-3">
                {[0, 1, 2, 3].map((index) => (
                  <Input
                    key={index}
                    id={`code-${index}`}
                    type="text"
                    maxLength={1}
                    value={code[index]}
                    onChange={(e) => handleCodeChange(index, e.target.value)}
                    className="h-16 w-16 rounded-md border border-gray-300 bg-white text-center  text-black text-xl font-semibold"
                  />
                ))}
              </div>

              <Button 
                onClick={handleCodeSubmit}
                className="w-full rounded-md bg-purple-600 py-6 text-sm font-semibold text-white hover:bg-purple-700"
              >
                Confirm code
              </Button>

              <p className="text-center text-sm text-gray-600">
                <span className="font-semibold text-black">00:58</span> Resend Confirmation Code
              </p>
            </div>
          </div>
        )}

        {/* Step 3: Reset Password */}
        {step === 3 && (
          <div className="space-y-8">
            <div>
              <h2 className="mb-3 text-xl font-bold text-black">Reset Password</h2>
              <p className="text-sm text-gray-600">Please enter your new password</p>
            </div>

            <div className="space-y-6">
              <div className="space-y-2">
                <label htmlFor="new-password" className="text-sm font-medium text-black">
                  Password
                </label>
                <Input
                  id="new-password"
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="Enter new password"
                  className="w-full rounded-md border border-gray-300 mt-3  bg-white px-4 py-3 text-sm"
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="confirm-password" className="text-sm font-medium text-black">
                  Confirm Password
                </label>
                <Input
                  id="confirm-password"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Confirm new password"
                  className="w-full rounded-md border border-gray-300 text-black bg-white px-4 py-3 text-sm"
                />
              </div>

              <Button 
                onClick={handlePasswordSubmit}
                className="w-full rounded-md bg-purple-600 py-6 text-sm font-semibold text-white hover:bg-purple-700"
              >
                Confirm Password
              </Button>

              <p className="text-center text-sm text-gray-600">
                Know your password?{" "}
                <Link href="/login" className="font-medium text-purple-600 hover:underline">
                  Log in
                </Link>
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
