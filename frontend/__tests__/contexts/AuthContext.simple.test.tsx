import { render, screen } from '@testing-library/react'
import { AuthProvider } from '@/contexts/AuthContext'

// Mock fetch to prevent real API calls
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: false,
    status: 401,
    json: () => Promise.resolve({}),
  })
) as jest.Mock

describe('AuthContext Simple', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('provides AuthProvider without crashing', () => {
    render(
      <AuthProvider>
        <div data-testid="test-child">Test Content</div>
      </AuthProvider>
    )

    expect(screen.getByTestId('test-child')).toHaveTextContent('Test Content')
  })
})