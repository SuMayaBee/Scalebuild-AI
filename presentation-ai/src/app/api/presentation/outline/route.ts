import { NextResponse } from "next/server";
import { generateOutlineAPI } from "@/lib/fastapi-client";
import { isDevelopmentMode } from "@/lib/dummy-auth";
import { getServerSession } from "@/lib/auth-utils";
import { LangChainAdapter } from "ai";
import { ChatOpenAI } from "@langchain/openai";
import { PromptTemplate } from "@langchain/core/prompts";
import { RunnableSequence } from "@langchain/core/runnables";

interface OutlineRequest {
  prompt: string;
  numberOfCards: number;
  language: string;
}

export async function POST(request: Request) {
  try {
    const body: OutlineRequest = await request.json();
    const { prompt, numberOfCards, language } = body;

    if (!prompt || !numberOfCards || !language) {
      return NextResponse.json(
        { error: "Missing required fields: prompt, numberOfCards, language" },
        { status: 400 }
      );
    }

    // Use FastAPI in development mode
    if (isDevelopmentMode()) {
      console.log(`🔄 Using FastAPI for outline generation`);
      
      try {
        const stream = await generateOutlineAPI({
          prompt,
          numberOfCards,
          language,
        });

        return new Response(stream, {
          headers: {
            "Content-Type": "text/plain",
            "Transfer-Encoding": "chunked",
          },
        });
      } catch (error) {
        console.error("❌ FastAPI outline generation failed:", error);
        return NextResponse.json(
          { error: "Failed to generate outline using FastAPI" },
          { status: 500 }
        );
      }
    }

    // Original Next.js logic (for production)
    const session = await getServerSession();
    if (!session?.user) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const outlineTemplate = `Given the following presentation topic and requirements, generate a structured outline with {numberOfCards} main topics in markdown format.
The outline should be in {language}.

Topic: {prompt}

Generate exactly {numberOfCards} main topics that would make for an engaging and well-structured presentation. 
Format the response as markdown content, with each topic as a heading followed by 2-3 bullet points.

Example format:
# First Main Topic
- Key point about this topic
- Another important aspect
- Brief conclusion or impact

# Second Main Topic
- Main insight for this section
- Supporting detail or example
- Practical application or takeaway

# Third Main Topic 
- Primary concept to understand
- Evidence or data point
- Conclusion or future direction

Make sure the topics:
1. Flow logically from one to another
2. Cover the key aspects of the main topic
3. Are clear and concise
4. Are engaging for the audience
5. ALWAYS use bullet points (not paragraphs) and format each point as "- point text"
6. Do not use bold, italic or underline
7. Keep each bullet point brief - just one sentence per point
8. Include exactly 2-3 bullet points per topic (not more, not less)`;

    const outlineChain = RunnableSequence.from([
      PromptTemplate.fromTemplate(outlineTemplate),
      new ChatOpenAI({
        model: "gpt-4o-mini",
        temperature: 0.7,
        streaming: true,
      }),
    ]);

    const stream = await outlineChain.stream({
      prompt,
      numberOfCards,
      language,
    });

    return LangChainAdapter.toDataStreamResponse(stream);
  } catch (error) {
    console.error("Error generating outline:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
