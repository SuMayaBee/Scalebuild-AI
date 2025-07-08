// Dummy authentication configuration for testing
export const DUMMY_USER = {
  id: "dummy_user_123",
  email: "test@example.com",
  name: "Test User",
  image: null,
};

export const FASTAPI_BASE_URL = "http://localhost:8000/api";

// Mock auth session
export const getDummySession = () => ({
  user: DUMMY_USER,
  expires: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // 24 hours from now
});

// Check if we're in development mode to use dummy auth
export const isDevelopmentMode = () => {
  return process.env.NODE_ENV === "development" || process.env.NEXT_PUBLIC_USE_DUMMY_AUTH === "true";
};
