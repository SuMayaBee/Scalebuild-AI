"use client";

import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";
import { usePresentationState } from "@/states/presentation-state";
import { SlideParser } from "../utils/parser";
import { generateOutlineAPI, generateSlidesAPI, updatePresentationAPI, type OutlineRequest, type SlidesRequest } from "@/lib/fastapi-client";

export function PresentationGenerationManager() {
  const {
    numSlides,
    language,
    presentationInput,
    shouldStartOutlineGeneration,
    shouldStartPresentationGeneration,
    setIsGeneratingOutline,
    setShouldStartOutlineGeneration,
    setShouldStartPresentationGeneration,
    resetGeneration,
    setOutline,
    setSlides,
    setIsGeneratingPresentation,
  } = usePresentationState();

  // Create a ref for the streaming parser to persist between renders
  const streamingParserRef = useRef<SlideParser>(new SlideParser());

  // Add refs to track the animation frame IDs
  const slidesRafIdRef = useRef<number | null>(null);
  const outlineRafIdRef = useRef<number | null>(null);

  // Create buffer refs to store the latest content
  // Note: The types should match what setOutline and setSlides expect
  const slidesBufferRef = useRef<ReturnType<
    SlideParser["getAllSlides"]
  > | null>(null);
  const outlineBufferRef = useRef<string[] | null>(null);

  // Function to update slides using requestAnimationFrame
  const updateSlidesWithRAF = (): void => {
    // Always check for the latest slides in the buffer
    if (slidesBufferRef.current !== null) {
      setSlides(slidesBufferRef.current);
      slidesBufferRef.current = null;
    }

    // Clear the current frame ID
    slidesRafIdRef.current = null;

    // We don't recursively schedule new frames
    // New frames will be scheduled only when new content arrives
  };

  // Function to update outline using requestAnimationFrame
  const updateOutlineWithRAF = (): void => {
    // Always check for the latest outline in the buffer
    if (outlineBufferRef.current !== null) {
      console.log('🔄 Updating outline via RAF:', outlineBufferRef.current);
      setOutline(outlineBufferRef.current);
      outlineBufferRef.current = null;
    }

    // Clear the current frame ID
    outlineRafIdRef.current = null;

    // We don't recursively schedule new frames
    // New frames will be scheduled only when new content arrives
  };

  // State for outline generation
  const [outlineCompletion, setOutlineCompletion] = useState<string>("");
  const [isGeneratingOutlineInternal, setIsGeneratingOutlineInternal] = useState(false);

  // Outline generation function
  const generateOutline = async () => {
    if (isGeneratingOutlineInternal) {
      console.log('🔄 Outline generation already in progress, skipping');
      return;
    }

    console.log('🚀 Starting outline generation with FastAPI');
    setIsGeneratingOutlineInternal(true);
    setIsGeneratingOutline(true);
    setOutlineCompletion("");

    try {
      const request: OutlineRequest = {
        prompt: presentationInput,
        numberOfCards: numSlides,
        language,
      };

      const stream = await generateOutlineAPI(request);
      const reader = stream.getReader();
      const decoder = new TextDecoder();

      let accumulatedContent = "";

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        accumulatedContent += chunk;
        setOutlineCompletion(accumulatedContent);
      }

      console.log('🏁 Outline generation finished:', accumulatedContent);
      
      // Handle completion
      setIsGeneratingOutline(false);
      setIsGeneratingOutlineInternal(false);
      setShouldStartOutlineGeneration(false);
      setShouldStartPresentationGeneration(false);

      const {
        currentPresentationId,
        outline,
        currentPresentationTitle,
        theme,
      } = usePresentationState.getState();

      if (currentPresentationId) {
        try {
          await updatePresentationAPI(currentPresentationId, { outline }, currentPresentationTitle ?? "");
          console.log('✅ Presentation outline updated successfully');
        } catch (error) {
          console.error('❌ Failed to update presentation outline:', error);
        }
      }

      // Cancel any pending outline animation frame
      if (outlineRafIdRef.current !== null) {
        cancelAnimationFrame(outlineRafIdRef.current);
        outlineRafIdRef.current = null;
      }

    } catch (error) {
      console.error('❌ Outline generation error:', error);
      toast.error("Failed to generate outline: " + (error as Error).message);
      resetGeneration();
      setIsGeneratingOutlineInternal(false);

      // Cancel any pending outline animation frame
      if (outlineRafIdRef.current !== null) {
        cancelAnimationFrame(outlineRafIdRef.current);
        outlineRafIdRef.current = null;
      }
    }
  };

  useEffect(() => {
    console.log('🔄 outlineCompletion changed:', outlineCompletion);
    if (outlineCompletion && typeof outlineCompletion === "string") {
      console.log('🔍 Raw outline completion:', outlineCompletion);
      
      // Parse the outline into sections
      let outlineItems: string[] = [];
      
      // Strategy 1: Split by markdown headers (# ) - Fixed regex to handle the exact format
      const sections = outlineCompletion.split(/^# /gm).filter(section => section.trim().length > 0);
      
      if (sections.length > 1) {
        // First section might be empty if the string starts with #, so handle that
        outlineItems = sections.map((section, index) => {
          const cleaned = section.trim();
          // If this is the first section and it's empty, skip it
          if (index === 0 && cleaned === '') return '';
          // Add the # back if it doesn't start with it
          return cleaned.startsWith('#') ? cleaned : `# ${cleaned}`;
        }).filter(item => item.length > 0);
      } else if (sections.length === 1 && sections[0]) {
        // Handle case where the entire text is one section
        const text = sections[0].trim();
        if (text) {
          outlineItems = [text.startsWith('#') ? text : `# ${text}`];
        }
      }
      
      // Strategy 2: If no sections found, try splitting by lines that start with #
      if (outlineItems.length === 0) {
        const lines = outlineCompletion.split('\n');
        const headerLines: string[] = [];
        let currentSection = '';
        
        for (const line of lines) {
          if (line.trim().startsWith('# ')) {
            // If we have a current section, save it
            if (currentSection.trim()) {
              headerLines.push(currentSection.trim());
            }
            // Start a new section
            currentSection = line.trim();
          } else if (line.trim().length > 0 && currentSection) {
            // Add content to current section
            currentSection += '\n' + line;
          }
        }
        
        // Don't forget the last section
        if (currentSection.trim()) {
          headerLines.push(currentSection.trim());
        }
        
        if (headerLines.length > 0) {
          outlineItems = headerLines;
        }
      }
      
      // Strategy 3: Fallback - split by double newlines and treat each paragraph as a topic
      if (outlineItems.length === 0) {
        const paragraphs = outlineCompletion.split(/\n\s*\n/).filter(p => p.trim().length > 0);
        if (paragraphs.length > 0) {
          outlineItems = paragraphs.map(p => {
            const trimmed = p.trim();
            return trimmed.startsWith('#') ? trimmed : `# ${trimmed.split('\n')[0]}`;
          });
        }
      }

      console.log('📝 Parsed outline items:', outlineItems);
      console.log('📝 Number of outline items:', outlineItems.length);

      // Store the latest outline in the buffer
      outlineBufferRef.current = outlineItems;

      // Only schedule a new frame if one isn't already pending
      if (outlineRafIdRef.current === null) {
        outlineRafIdRef.current = requestAnimationFrame(updateOutlineWithRAF);
      }
    }
  }, [outlineCompletion]);

  // Watch for outline generation start
  useEffect(() => {
    const startOutlineGeneration = async (): Promise<void> => {
      const { presentationInput, numSlides, language } =
        usePresentationState.getState();
      if (shouldStartOutlineGeneration && !isGeneratingOutlineInternal) {
        console.log('🚀 useEffect triggering outline generation');
        try {
          // Start the RAF cycle for outline updates
          if (outlineRafIdRef.current === null) {
            outlineRafIdRef.current =
              requestAnimationFrame(updateOutlineWithRAF);
          }

          await generateOutline();
        } catch (error) {
          console.log(error);
          // Error is handled by the function itself
        }
      }
    };

    void startOutlineGeneration();
  }, [shouldStartOutlineGeneration, isGeneratingOutlineInternal, presentationInput, numSlides, language]);

  // State for presentation generation
  const [presentationCompletion, setPresentationCompletion] = useState<string>("");
  const [isGeneratingPresentationInternal, setIsGeneratingPresentationInternal] = useState(false);

  // Presentation generation function
  const generatePresentation = async () => {
    if (isGeneratingPresentationInternal) {
      console.log('🔄 Presentation generation already in progress, skipping');
      return;
    }

    console.log('🚀 Starting presentation generation with FastAPI');
    setIsGeneratingPresentationInternal(true);
    setIsGeneratingPresentation(true);
    setPresentationCompletion("");

    try {
      const { outline, currentPresentationTitle, theme } = usePresentationState.getState();
      
      const request: SlidesRequest = {
        title: currentPresentationTitle || "Untitled Presentation",
        outline: outline,
        language: language,
        tone: theme || "professional",
      };

      const stream = await generateSlidesAPI(request);
      const reader = stream.getReader();
      const decoder = new TextDecoder();

      let accumulatedContent = "";

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        accumulatedContent += chunk;
        setPresentationCompletion(accumulatedContent);
      }

      console.log('🏁 Presentation generation finished');
      
      // Handle completion
      const { currentPresentationId, currentPresentationTitle: finalTitle, theme: finalTheme } =
        usePresentationState.getState();
      const parser = streamingParserRef.current;
      parser.reset();
      parser.parseChunk(accumulatedContent);
      parser.finalize();
      parser.clearAllGeneratingMarks();
      const slides = parser.getAllSlides();
      slidesBufferRef.current = slides;

      requestAnimationFrame(updateSlidesWithRAF);

      if (currentPresentationId) {
        try {
          await updatePresentationAPI(currentPresentationId, { slides: slides }, finalTitle ?? "");
          console.log('✅ Presentation slides updated successfully');
        } catch (error) {
          console.error('❌ Failed to update presentation slides:', error);
        }
      }

      setIsGeneratingPresentation(false);
      setIsGeneratingPresentationInternal(false);
      setShouldStartPresentationGeneration(false);
      
      // Cancel any pending animation frame
      if (slidesRafIdRef.current !== null) {
        cancelAnimationFrame(slidesRafIdRef.current);
        slidesRafIdRef.current = null;
      }

    } catch (error) {
      console.error('❌ Presentation generation error:', error);
      toast.error("Failed to generate presentation: " + (error as Error).message);
      resetGeneration();
      streamingParserRef.current.reset();
      setIsGeneratingPresentationInternal(false);

      // Cancel any pending animation frame
      if (slidesRafIdRef.current !== null) {
        cancelAnimationFrame(slidesRafIdRef.current);
        slidesRafIdRef.current = null;
      }
    }
  };

  useEffect(() => {
    if (presentationCompletion) {
      try {
        streamingParserRef.current.reset();
        streamingParserRef.current.parseChunk(presentationCompletion);
        streamingParserRef.current.finalize();
        const allSlides = streamingParserRef.current.getAllSlides();

        // Store the latest slides in the buffer
        slidesBufferRef.current = allSlides;

        // Only schedule a new frame if one isn't already pending
        if (slidesRafIdRef.current === null) {
          slidesRafIdRef.current = requestAnimationFrame(updateSlidesWithRAF);
        }
      } catch (error) {
        console.error("Error processing presentation XML:", error);
        toast.error("Error processing presentation content");
      }
    }
  }, [presentationCompletion]);

  useEffect(() => {
    if (shouldStartPresentationGeneration) {
      const {
        outline,
        presentationInput,
        language,
        presentationStyle,
        currentPresentationTitle,
      } = usePresentationState.getState();

      // Reset the parser before starting a new generation
      streamingParserRef.current.reset();

      // Start the RAF cycle for slide updates
      if (slidesRafIdRef.current === null) {
        slidesRafIdRef.current = requestAnimationFrame(updateSlidesWithRAF);
      }

      void generatePresentation();
    }
  }, [shouldStartPresentationGeneration]);

  // Clean up RAF on unmount
  useEffect(() => {
    return () => {
      if (slidesRafIdRef.current !== null) {
        cancelAnimationFrame(slidesRafIdRef.current);
        slidesRafIdRef.current = null;
      }

      if (outlineRafIdRef.current !== null) {
        cancelAnimationFrame(outlineRafIdRef.current);
        outlineRafIdRef.current = null;
      }
    };
  }, []);

  return null;
}
