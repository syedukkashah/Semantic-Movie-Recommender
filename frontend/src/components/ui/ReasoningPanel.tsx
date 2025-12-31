import { Brain } from "lucide-react";
import type { Emotion } from "./EmotionSelector";

interface ReasoningPanelProps {
  emotion: Emotion;
  intensity: number;
  movieCount: number;
}

const emotionLabels: Record<Emotion, string> = {
  joy: "Joy",
  sadness: "Sadness",
  anger: "Anger",
  fear: "Fear",
  trust: "Trust",
  surprise: "Surprise",
};

export function ReasoningPanel({ emotion, intensity, movieCount }: ReasoningPanelProps) {
  const intensityLevel = intensity < 40 ? "low" : intensity < 70 ? "moderate" : "high";
  
  return (
    <div className="bg-card rounded-xl p-6 shadow-card border border-border">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
          <Brain className="h-5 w-5 text-primary" />
        </div>
        <h2 className="text-lg font-semibold text-foreground">
          Reasoning Explanation
        </h2>
      </div>
      
      <div className="bg-muted rounded-lg p-4 font-mono text-sm text-foreground/90 leading-relaxed space-y-2">
        <p>
          <span className="text-muted-foreground">Query:</span> emotion = {emotionLabels[emotion]}, intensity = {intensityLevel}
        </p>
        <p>
          <span className="text-muted-foreground">Rule applied:</span> IF user_emotion(?e) ∧ movie_emotion(?m, ?e) → recommend(?m)
        </p>
        <p>
          <span className="text-muted-foreground">Knowledge graph:</span> Matched {movieCount} movies with aggregated emotion "{emotionLabels[emotion]}"
        </p>
        <p>
          <span className="text-muted-foreground">Confidence:</span> High (based on emotion knowledge graph inference)
        </p>
      </div>
      
      <p className="mt-4 text-sm text-muted-foreground">
        The semantic reasoner analyzed the emotion knowledge graph and identified movies 
        whose dominant emotional content aligns with your selected preference of "{emotionLabels[emotion]}" 
        at {intensityLevel} intensity.
      </p>
    </div>
  );
}
