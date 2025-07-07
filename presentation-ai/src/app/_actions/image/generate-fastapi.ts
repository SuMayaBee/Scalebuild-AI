"use server";

import { generateImageAPI } from "@/lib/fastapi-client";
import { isDevelopmentMode, getDummySession } from "@/lib/dummy-auth";

export type ImageModelList = "dall-e-3";

export async function generateImageAction(
  prompt: string,
  model: ImageModelList = "dall-e-3"
) {
  try {
    console.log(`🔄 Generating image with FastAPI DALL-E: "${prompt}"`);
    
    const result = await generateImageAPI({
      prompt: prompt,
      model: "dalle"
    });
    
    console.log(`✅ FastAPI image generated successfully:`, result);
    
    return {
      success: true,
      image: {
        id: result.id || "fastapi_generated",
        url: result.url,
        prompt: result.prompt,
        userId: result.user_id || "dummy_user_123",
      },
    };
  } catch (error) {
    console.error("❌ FastAPI image generation failed:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Failed to generate image",
    };
  }
}
