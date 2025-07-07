"use client";

import { createContext, useContext, type ReactNode } from "react";
import { isDevelopmentMode, DUMMY_USER, getDummySession } from "@/lib/dummy-auth";

// Mock session type
interface MockSession {
  user: {
    id: string;
    email: string;
    name: string;
    image: string | null;
  };
  expires: string;
}

interface MockAuthContextType {
  data: MockSession | null;
  status: "loading" | "authenticated" | "unauthenticated";
  update: () => Promise<MockSession | null>;
}

const MockAuthContext = createContext<MockAuthContextType | undefined>(undefined);

export function MockAuthProvider({ children }: { children: ReactNode }) {
  // Only provide mock auth in development mode
  if (!isDevelopmentMode()) {
    return <>{children}</>;
  }

  const mockSession = getDummySession();

  const contextValue: MockAuthContextType = {
    data: mockSession,
    status: "authenticated",
    update: async () => mockSession,
  };

  return (
    <MockAuthContext.Provider value={contextValue}>
      {children}
    </MockAuthContext.Provider>
  );
}

export function useMockSession() {
  const context = useContext(MockAuthContext);
  
  if (!isDevelopmentMode()) {
    return {
      data: null,
      status: "unauthenticated" as const,
      update: async () => null,
    };
  }
  
  if (context === undefined) {
    throw new Error("useMockSession must be used within a MockAuthProvider");
  }
  
  return context;
}

// Export a unified session hook that works in both development and production
export function useUnifiedSession() {
  if (isDevelopmentMode()) {
    return useMockSession();
  }
  
  // In production, you would import and use the real useSession from next-auth
  // For now, return unauthenticated to force FastAPI usage
  return {
    data: null,
    status: "unauthenticated" as const,
    update: async () => null,
  };
}
