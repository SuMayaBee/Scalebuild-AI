"use server";

import { isDevelopmentMode, getDummySession } from "@/lib/dummy-auth";
import { auth } from "@/server/auth";

export async function getServerSession() {
  // Use dummy session in development mode
  if (isDevelopmentMode()) {
    console.log("🔄 Using dummy session for development");
    return getDummySession();
  }

  // Use real auth in production
  return await auth();
}

export async function requireAuth() {
  const session = await getServerSession();
  
  if (!session?.user) {
    if (isDevelopmentMode()) {
      // In development, return dummy user
      return getDummySession();
    }
    throw new Error("Unauthorized");
  }
  
  return session;
}
