import { render, screen } from '@testing-library/react'
import ProtectedRoute from '@/components/ProtectedRoute'

// Mock Next.js navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn()
  }),
  usePathname: () => '/dashboard'
}))

// Mock AuthContext
jest.mock('@/contexts/AuthContext', () => ({
  useAuth: jest.fn()
}))

import { useAuth } from '@/contexts/AuthContext'

describe('ProtectedRoute', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders children when user is authenticated', () => {
    useAuth.mockReturnValue({
      user: { id: '1', email: 'test@example.com' },
      isLoading: false,
      isInitialized: true
    })

    render(
      <ProtectedRoute>
        <div>Protected Content</div>
      </ProtectedRoute>
    )

    expect(screen.getByText('Protected Content')).toBeInTheDocument()
  })

  it('shows loading spinner when auth is loading', () => {
    useAuth.mockReturnValue({
      user: null,
      isLoading: true,
      isInitialized: false
    })

    render(
      <ProtectedRoute>
        <div>Protected Content</div>
      </ProtectedRoute>
    )

    // Check for loading spinner instead of text
    expect(document.querySelector('.animate-spin')).toBeInTheDocument()
  })
})