import { Film } from "lucide-react";
import type { Emotion } from "./EmotionSelector";

interface MovieCardProps {
  title: string;
  emotion: Emotion;
  confidence: number;
  delay?: number;
}

const emotionLabels: Record<Emotion, string> = {
  joy: "Joy",
  sadness: "Sadness",
  anger: "Anger",
  fear: "Fear",
  trust: "Trust",
  surprise: "Surprise",
};

export function MovieCard({ title, emotion, confidence, delay = 0 }: MovieCardProps) {
  return (
    <div 
      className="bg-card rounded-xl p-5 shadow-card border border-border hover:shadow-card-hover transition-all duration-200 opacity-0 animate-fade-in"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0 w-12 h-12 rounded-lg bg-muted flex items-center justify-center">
          <Film className="h-6 w-6 text-muted-foreground" />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-foreground text-lg leading-tight mb-2">
            {title}
          </h3>
          <span 
            className={`emotion-tag emotion-${emotion}`}
          >
            {emotionLabels[emotion]}
          </span>
          <p className="mt-3 text-sm text-muted-foreground leading-relaxed">
            Recommended because it matches your emotional preference with {confidence}% confidence.
          </p>
        </div>
      </div>
    </div>
  );
}
