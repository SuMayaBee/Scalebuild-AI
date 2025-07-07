"use client";

import { Wand2, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { usePresentationState } from "@/states/presentation-state";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { PresentationInput } from "./PresentationInput";
import { PresentationControls } from "./PresentationControls";
import { PresentationTemplates } from "./PresentationTemplates";
import { RecentPresentations } from "./RecentPresentations";
import { PresentationExamples } from "./PresentationExamples";
import { PresentationsSidebar } from "./PresentationsSidebar";
import { useEffect } from "react";
import { PresentationHeader } from "./PresentationHeader";
import { createPresentationAPI } from "@/lib/fastapi-client";
import { DUMMY_USER } from "@/lib/dummy-auth";

export function PresentationDashboard() {
  const router = useRouter();
  const {
    presentationInput,
    isGeneratingOutline,
    setCurrentPresentation,
    setIsGeneratingOutline,
    // We'll use these instead of directly calling startOutlineGeneration
    setShouldStartOutlineGeneration,
  } = usePresentationState();

  useEffect(() => {
    setCurrentPresentation("", "");
    // Make sure to reset any generation flags when landing on dashboard
    setIsGeneratingOutline(false);
    setShouldStartOutlineGeneration(false);
  }, []);

  const handleGenerate = async (e?: React.FormEvent) => {
    // Prevent default form submission
    if (e) {
      e.preventDefault();
    }
    
    if (!presentationInput.trim()) {
      toast.error("Please enter a topic for your presentation");
      return;
    }

    // Set UI loading state
    setIsGeneratingOutline(true);

    try {
      const presentation = await createPresentationAPI({
        title: presentationInput.substring(0, 50) || "Untitled Presentation",
        content: { slides: [] }, // Empty content for new presentation
        theme: "default",
        language: "English",
        tone: "Professional",
        user_email: DUMMY_USER.email,
      });

      // Set the current presentation
      setCurrentPresentation(
        presentation.id,
        presentation.title
      );
      router.push(`/presentation/generate/${presentation.id}`);
    } catch (error) {
      setIsGeneratingOutline(false);
      console.error("Error creating presentation:", error);
      toast.error("Failed to create presentation");
    }
  };

  const handleCreateBlank = async () => {
    try {
      setIsGeneratingOutline(true);
      const presentation = await createPresentationAPI({
        title: "Untitled Presentation",
        content: { slides: [] }, // Empty content for blank presentation
        theme: "default",
        language: "English",
        tone: "Professional",
        user_email: DUMMY_USER.email,
      });
      
      setCurrentPresentation(
        presentation.id,
        presentation.title
      );
      router.push(`/presentation/generate/${presentation.id}`);
    } catch (error) {
      setIsGeneratingOutline(false);
      console.error("Error creating presentation:", error);
      toast.error("Failed to create presentation");
    }
  };

  return (
    <div className="notebook-section relative w-full">
      <PresentationsSidebar />
      <div className="mx-auto w-full max-w-4xl space-y-12 px-6 py-12">
        <PresentationHeader />

        <form onSubmit={handleGenerate} className="space-y-8">
          <PresentationInput />
          <PresentationControls />
          <div className="flex items-center justify-end">
            <div className="flex items-center gap-2">
              <Button
                type="submit"
                disabled={!presentationInput.trim() || isGeneratingOutline}
                variant={isGeneratingOutline ? "loading" : "default"}
                className="gap-2"
              >
                <Wand2 className="h-4 w-4" />
                Generate Presentation
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={handleCreateBlank}
                className="gap-2"
              >
                <Plus className="h-4 w-4" />
                Create Blank
              </Button>
            </div>
          </div>
        </form>

        <PresentationExamples />
        <RecentPresentations />
        <PresentationTemplates />
      </div>
    </div>
  );
}
