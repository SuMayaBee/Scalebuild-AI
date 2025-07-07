import { auth } from "@/server/auth";
import { NextResponse } from "next/server";
import { type NextRequest } from "next/server";

// Check if we're in development mode to bypass auth
const isDevelopmentMode = () => {
  const nodeEnv = process.env.NODE_ENV;
  const useDummyAuth = process.env.NEXT_PUBLIC_USE_DUMMY_AUTH;
  
  console.log("🔍 Environment check:", { nodeEnv, useDummyAuth });
  
  return nodeEnv === "development" || useDummyAuth === "true";
};

export async function middleware(request: NextRequest) {
  const isAuthPage = request.nextUrl.pathname.startsWith("/auth");
  const isApiRoute = request.nextUrl.pathname.startsWith("/api");

  console.log("🛡️ Middleware called for:", request.nextUrl.pathname);

  // Always redirect from root to /presentation
  if (request.nextUrl.pathname === "/") {
    console.log("🔄 Redirecting root to /presentation");
    return NextResponse.redirect(new URL("/presentation", request.url));
  }

  // BYPASS AUTH IN DEVELOPMENT MODE
  if (isDevelopmentMode()) {
    console.log("🔄 Development mode: Bypassing authentication for", request.nextUrl.pathname);
    
    // Redirect auth pages to presentation in development
    if (isAuthPage) {
      console.log("🔄 Redirecting auth page to /presentation");
      return NextResponse.redirect(new URL("/presentation", request.url));
    }
    
    // Allow all other routes in development
    console.log("✅ Allowing route in development mode");
    return NextResponse.next();
  }

  // PRODUCTION AUTH LOGIC
  const session = await auth();

  // If user is on auth page but already signed in, redirect to home page
  if (isAuthPage && session) {
    return NextResponse.redirect(new URL("/presentation", request.url));
  }

  // If user is not authenticated and trying to access a protected route, redirect to sign-in
  if (!session && !isAuthPage && !isApiRoute) {
    return NextResponse.redirect(
      new URL(
        `/auth/signin?callbackUrl=${encodeURIComponent(request.url)}`,
        request.url
      )
    );
  }

  return NextResponse.next();
}

// Add routes that should be protected by authentication
export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
