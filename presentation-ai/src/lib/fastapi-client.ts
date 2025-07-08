// FastAPI client functions for presentation generation
import { FASTAPI_BASE_URL, DUMMY_USER } from "@/lib/dummy-auth";

// Types
export interface OutlineRequest {
  prompt: string;
  numberOfCards: number;
  language: string;
}

export interface SlidesRequest {
  title: string;
  outline: string[];
  language: string;
  tone: string;
}

export interface ImageGenerationRequest {
  prompt: string;
  model?: "dalle" | "flux";
  user_email?: string; // Changed from user_id to user_email
}

export interface PresentationCreateRequest {
  title: string;
  content: any;
  theme?: string;
  language?: string;
  tone?: string;
  user_email: string; // Changed from user_id to user_email
}

// Generate outline using FastAPI
export async function generateOutlineAPI(request: OutlineRequest): Promise<ReadableStream> {
  const response = await fetch(`${FASTAPI_BASE_URL}/presentation/outline`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Failed to generate outline: ${response.statusText}`);
  }

  return response.body!;
}

// Generate slides using FastAPI
export async function generateSlidesAPI(request: SlidesRequest): Promise<ReadableStream> {
  const response = await fetch(`${FASTAPI_BASE_URL}/presentation/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Failed to generate slides: ${response.statusText}`);
  }

  return response.body!;
}

// Generate image using FastAPI DALL-E
export async function generateImageAPI(request: ImageGenerationRequest) {
  const requestWithUser = {
    ...request,
    user_email: DUMMY_USER.email, // Use email instead of id
    model: "dalle", // Force DALL-E for now
  };

  const response = await fetch(`${FASTAPI_BASE_URL}/presentation/generate-image`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestWithUser),
  });

  if (!response.ok) {
    throw new Error(`Failed to generate image: ${response.statusText}`);
  }

  return response.json();
}

// Create presentation using FastAPI
export async function createPresentationAPI(request: PresentationCreateRequest) {
  const requestWithUser = {
    ...request,
    user_email: DUMMY_USER.email, // Use email instead of id
  };

  const response = await fetch(`${FASTAPI_BASE_URL}/presentation/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestWithUser),
  });

  if (!response.ok) {
    throw new Error(`Failed to create presentation: ${response.statusText}`);
  }

  return response.json();
}

// Get presentation using FastAPI
export async function getPresentationAPI(presentationId: string) {
  const response = await fetch(`${FASTAPI_BASE_URL}/presentation/${presentationId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to get presentation: ${response.statusText}`);
  }

  return response.json();
}

// Update presentation using FastAPI
export async function updatePresentationAPI(presentationId: string, content: any, title?: string) {
  const response = await fetch(`${FASTAPI_BASE_URL}/presentation/${presentationId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      content,
      ...(title && { title }),
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to update presentation: ${response.statusText}`);
  }

  return response.json();
}

// Get user presentations using FastAPI
export async function getUserPresentationsAPI() {
  const response = await fetch(`${FASTAPI_BASE_URL}/presentation/user/${DUMMY_USER.email}`, { // Use email instead of id
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to get user presentations: ${response.statusText}`);
  }

  return response.json();
}

// Delete presentations using FastAPI
export async function deletePresentationsAPI(presentationIds: string[]) {
  const response = await fetch(`${FASTAPI_BASE_URL}/presentation/delete`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      presentation_ids: presentationIds,
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to delete presentations: ${response.statusText}`);
  }

  return response.json();
}
