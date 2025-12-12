import '@testing-library/jest-dom'

// Extend Jest matchers
declare global {
  namespace jest {
    interface Matchers<R> {
      toBeInTheDocument(): R
      toHaveTextContent(text: string | RegExp): R
      toHaveClass(className: string): R
      toBeDisabled(): R
    }
  }
}