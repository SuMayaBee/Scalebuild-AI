"use server";

import { type PlateSlide } from "@/components/presentation/utils/parser";
import { isDevelopmentMode, getDummySession } from "@/lib/dummy-auth";
import {
  createPresentationAPI,
  getPresentationAPI,
  updatePresentationAPI,
  getUserPresentationsAPI,
} from "@/lib/fastapi-client";
import { requireAuth } from "@/lib/auth-utils";
import { auth } from "@/server/auth";
import { db } from "@/server/db";
import { type InputJsonValue } from "@prisma/client/runtime/library";

export async function createPresentation(
  content: {
    slides: PlateSlide[];
  },
  title: string,
  theme = "default",
  outline?: string[],
  imageModel?: string,
  presentationStyle?: string,
  language?: string
) {
  // Use FastAPI in development mode
  if (isDevelopmentMode()) {
    try {
      console.log(`🔄 Creating presentation with FastAPI: "${title}"`);
      
      const result = await createPresentationAPI({
        title: title ?? "Untitled Presentation",
        content: content,
        theme: theme,
        language: language ?? "English",
        tone: presentationStyle ?? "Professional",
        user_id: "dummy_user_123",
      });
      
      console.log(`✅ FastAPI presentation created:`, result);
      
      return {
        success: true,
        message: "Presentation created successfully",
        presentation: {
          id: result.id,
          title: result.title,
          content: result.content,
          theme: result.theme,
          language: result.language,
          tone: result.tone,
          userId: result.userId,
          createdAt: result.createdAt,
          updatedAt: result.updatedAt,
        },
      };
    } catch (error) {
      console.error("❌ FastAPI presentation creation failed:", error);
      return {
        success: false,
        message: error instanceof Error ? error.message : "Failed to create presentation",
      };
    }
  }

  // Original Next.js logic (for production)
  const session = await requireAuth();
  if (!session?.user) {
    throw new Error("Unauthorized");
  }
  const userId = session.user.id;

  try {
    const presentation = await db.baseDocument.create({
      data: {
        type: "PRESENTATION",
        documentType: "presentation",
        title: title ?? "Untitled Presentation",
        userId,
        presentation: {
          create: {
            content: content as unknown as InputJsonValue,
            theme: theme,
            imageModel,
            presentationStyle,
            language,
            outline: outline,
          },
        },
      },
      include: {
        presentation: true,
      },
    });

    return {
      success: true,
      message: "Presentation created successfully",
      presentation: presentation,
    };
  } catch (error) {
    console.error(error);
    return {
      success: false,
      message: "Failed to create presentation",
    };
  }
}

export async function getPresentation(id: string) {
  // Use FastAPI in development mode
  if (isDevelopmentMode()) {
    try {
      console.log(`🔄 Getting presentation from FastAPI: ${id}`);
      
      const result = await getPresentationAPI(id);
      
      console.log(`✅ FastAPI presentation retrieved:`, result);
      
      // Map FastAPI response to expected format
      return {
        success: true,
        presentation: {
          id: result.id,
          title: result.title,
          userId: result.userId,
          createdAt: result.createdAt,
          updatedAt: result.updatedAt,
          presentation: {
            content: result.content,
            theme: result.theme,
            language: result.language,
            tone: result.tone,
            outline: result.content?.outline || [],
            imageModel: "dall-e-3",
            presentationStyle: result.tone,
          },
        },
      };
    } catch (error) {
      console.error("❌ FastAPI get presentation failed:", error);
      return {
        success: false,
        message: error instanceof Error ? error.message : "Failed to get presentation",
      };
    }
  }

  // Original Next.js logic (for production)
  const session = await requireAuth();
  if (!session?.user) {
    return { success: false, message: "Unauthorized" };
  }

  try {
    const presentation = await db.baseDocument.findUnique({
      where: { id },
      include: {
        presentation: true,
      },
    });

    if (!presentation) {
      return { success: false, message: "Presentation not found" };
    }

    if (presentation.userId !== session.user.id) {
      return { success: false, message: "Unauthorized" };
    }

    return { success: true, presentation };
  } catch (error) {
    console.error(error);
    return { success: false, message: "Failed to retrieve presentation" };
  }
}

export async function updatePresentation(
  id: string,
  content?: {
    slides: PlateSlide[];
  },
  title?: string,
  theme?: string,
  outline?: string[],
  imageModel?: string,
  presentationStyle?: string,
  language?: string
) {
  // Use FastAPI in development mode
  if (isDevelopmentMode()) {
    try {
      console.log(`🔄 Updating presentation with FastAPI: ${id}`);
      
      const updateData: any = {};
      if (content) updateData.content = content;
      if (title) updateData.title = title;
      
      const result = await updatePresentationAPI(id, updateData.content, updateData.title);
      
      console.log(`✅ FastAPI presentation updated:`, result);
      
      return {
        success: true,
        message: "Presentation updated successfully",
        presentation: result,
      };
    } catch (error) {
      console.error("❌ FastAPI update presentation failed:", error);
      return {
        success: false,
        message: error instanceof Error ? error.message : "Failed to update presentation",
      };
    }
  }

  // Original Next.js logic (for production)
  const session = await requireAuth();
  if (!session?.user) {
    return { success: false, message: "Unauthorized" };
  }

  try {
    const updateData: any = {};
    if (content) {
      updateData.presentation = {
        update: {
          content: content as unknown as InputJsonValue,
          ...(theme && { theme }),
          ...(outline && { outline }),
          ...(imageModel && { imageModel }),
          ...(presentationStyle && { presentationStyle }),
          ...(language && { language }),
        },
      };
    }
    if (title) {
      updateData.title = title;
    }

    const presentation = await db.baseDocument.update({
      where: { id },
      data: updateData,
      include: {
        presentation: true,
      },
    });

    return {
      success: true,
      message: "Presentation updated successfully",
      presentation: presentation,
    };
  } catch (error) {
    console.error(error);
    return {
      success: false,
      message: "Failed to update presentation",
    };
  }
}

export async function getUserPresentations() {
  // Use FastAPI in development mode
  if (isDevelopmentMode()) {
    try {
      console.log(`🔄 Getting user presentations from FastAPI`);
      
      const result = await getUserPresentationsAPI();
      
      console.log(`✅ FastAPI user presentations retrieved:`, result);
      
      // Map FastAPI response to expected format
      const presentations = result.map((p: any) => ({
        id: p.id,
        title: p.title,
        userId: p.userId,
        createdAt: p.createdAt,
        updatedAt: p.updatedAt,
        presentation: {
          content: p.content,
          theme: p.theme,
          language: p.language,
          tone: p.tone,
        },
      }));
      
      return {
        success: true,
        presentations: presentations,
      };
    } catch (error) {
      console.error("❌ FastAPI get user presentations failed:", error);
      return {
        success: false,
        message: error instanceof Error ? error.message : "Failed to get presentations",
      };
    }
  }

  // Original Next.js logic (for production)
  const session = await requireAuth();
  if (!session?.user) {
    return { success: false, message: "Unauthorized" };
  }

  try {
    const presentations = await db.baseDocument.findMany({
      where: {
        userId: session.user.id,
        type: "PRESENTATION",
      },
      include: {
        presentation: true,
      },
      orderBy: {
        updatedAt: "desc",
      },
    });

    return { success: true, presentations };
  } catch (error) {
    console.error(error);
    return { success: false, message: "Failed to retrieve presentations" };
  }
}

export async function deletePresentations(ids: string[]) {
  // Use FastAPI in development mode
  if (isDevelopmentMode()) {
    try {
      console.log(`🔄 Deleting presentations with FastAPI: ${ids.join(', ')}`);
      
      // For now, just return success since we haven't implemented bulk delete in FastAPI
      // You can implement this endpoint in FastAPI later
      console.log(`✅ FastAPI presentations deleted (simulated)`);
      
      return {
        success: true,
        message: "Presentations deleted successfully",
      };
    } catch (error) {
      console.error("❌ FastAPI delete presentations failed:", error);
      return {
        success: false,
        message: error instanceof Error ? error.message : "Failed to delete presentations",
      };
    }
  }

  // Original Next.js logic (for production)
  const session = await auth();
  if (!session?.user) {
    return { success: false, message: "Unauthorized" };
  }

  try {
    await db.baseDocument.deleteMany({
      where: {
        id: { in: ids },
        userId: session.user.id,
      },
    });

    return { success: true, message: "Presentations deleted successfully" };
  } catch (error) {
    console.error(error);
    return { success: false, message: "Failed to delete presentations" };
  }
}

export async function duplicatePresentation(id: string) {
  // Use FastAPI in development mode
  if (isDevelopmentMode()) {
    try {
      console.log(`🔄 Duplicating presentation with FastAPI: ${id}`);
      
      // Get the original presentation
      const original = await getPresentationAPI(id);
      
      // Create a copy with a new title
      const duplicated = await createPresentationAPI({
        title: `${original.title} (Copy)`,
        content: original.content,
        theme: original.theme,
        language: original.language,
        tone: original.tone,
        user_id: "dummy_user_123",
      });
      
      console.log(`✅ FastAPI presentation duplicated:`, duplicated);
      
      return {
        success: true,
        message: "Presentation duplicated successfully",
        presentation: duplicated,
      };
    } catch (error) {
      console.error("❌ FastAPI duplicate presentation failed:", error);
      return {
        success: false,
        message: error instanceof Error ? error.message : "Failed to duplicate presentation",
      };
    }
  }

  // Original Next.js logic (for production)
  const session = await auth();
  if (!session?.user) {
    return { success: false, message: "Unauthorized" };
  }

  try {
    const original = await db.baseDocument.findUnique({
      where: { id },
      include: { presentation: true },
    });

    if (!original || original.userId !== session.user.id) {
      return { success: false, message: "Presentation not found" };
    }

    const duplicated = await db.baseDocument.create({
      data: {
        type: "PRESENTATION",
        documentType: "presentation",
        title: `${original.title} (Copy)`,
        userId: session.user.id,
        presentation: original.presentation
          ? {
              create: {
                content: original.presentation.content as unknown as InputJsonValue,
                theme: original.presentation.theme,
                imageModel: original.presentation.imageModel,
                presentationStyle: original.presentation.presentationStyle,
                language: original.presentation.language,
                outline: original.presentation.outline,
              },
            }
          : undefined,
      },
      include: { presentation: true },
    });

    return {
      success: true,
      message: "Presentation duplicated successfully",
      presentation: duplicated,
    };
  } catch (error) {
    console.error(error);
    return { success: false, message: "Failed to duplicate presentation" };
  }
}

export async function getPresentationContent(id: string) {
  // Just use getPresentation which already has the content
  return getPresentation(id);
}

export async function updatePresentationTitle(id: string, title: string) {
  return updatePresentation(id, undefined, title);
}

export async function createEmptyPresentation(title: string) {
  return createPresentation(
    { slides: [] },
    title,
    "default",
    [],
    "dall-e-3",
    "Professional",
    "English"
  );
}

export async function updatePresentationTheme(id: string, theme: string) {
  return updatePresentation(id, undefined, undefined, theme);
}
