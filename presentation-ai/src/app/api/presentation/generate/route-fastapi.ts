import { NextResponse } from "next/server";
import { generateSlidesAPI } from "@/lib/fastapi-client";
import { isDevelopmentMode } from "@/lib/dummy-auth";
import { LangChainAdapter } from "ai";
import { auth } from "@/server/auth";
import { ChatOpenAI } from "@langchain/openai";
import { PromptTemplate } from "@langchain/core/prompts";
import { RunnableSequence } from "@langchain/core/runnables";

interface SlidesRequest {
  title: string;
  outline: string[];
  language: string;
  tone: string;
}

export async function POST(request: Request) {
  try {
    const body: SlidesRequest = await request.json();
    const { title, outline, language, tone } = body;

    if (!title || !outline || !language || !tone) {
      return NextResponse.json(
        { error: "Missing required fields: title, outline, language, tone" },
        { status: 400 }
      );
    }

    // Use FastAPI in development mode
    if (isDevelopmentMode()) {
      console.log(`🔄 Using FastAPI for slides generation`);
      
      try {
        const stream = await generateSlidesAPI({
          title,
          outline,
          language,
          tone,
        });

        return new Response(stream, {
          headers: {
            "Content-Type": "application/xml",
            "Transfer-Encoding": "chunked",
          },
        });
      } catch (error) {
        console.error("❌ FastAPI slides generation failed:", error);
        return NextResponse.json(
          { error: "Failed to generate slides using FastAPI" },
          { status: 500 }
        );
      }
    }

    // Original Next.js logic (for production)
    const session = await auth();
    if (!session?.user) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // Original LangChain logic would go here...
    // For now, return error to force FastAPI usage
    return NextResponse.json(
      { error: "Please use development mode with FastAPI" },
      { status: 501 }
    );
  } catch (error) {
    console.error("Error generating slides:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
