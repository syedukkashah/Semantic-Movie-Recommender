import { cn } from "@/lib/utils";
import { Smile, Frown, Angry, Ghost, Heart, Sparkles } from "lucide-react";

export type Emotion = "joy" | "sadness" | "anger" | "fear" | "trust" | "surprise";

interface EmotionSelectorProps {
  selectedEmotion: Emotion | null;
  onSelect: (emotion: Emotion) => void;
}

const emotions: { id: Emotion; label: string; icon: React.ElementType }[] = [
  { id: "joy", label: "Joy", icon: Smile },
  { id: "sadness", label: "Sadness", icon: Frown },
  { id: "anger", label: "Anger", icon: Angry },
  { id: "fear", label: "Fear", icon: Ghost },
  { id: "trust", label: "Trust", icon: Heart },
  { id: "surprise", label: "Surprise", icon: Sparkles },
];

export function EmotionSelector({ selectedEmotion, onSelect }: EmotionSelectorProps) {
  return (
    <div className="grid grid-cols-3 sm:grid-cols-6 gap-3">
      {emotions.map((emotion) => {
        const Icon = emotion.icon;
        const isSelected = selectedEmotion === emotion.id;
        
        return (
          <button
            key={emotion.id}
            onClick={() => onSelect(emotion.id)}
            className={cn(
              "flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all duration-200",
              "hover:shadow-card-hover hover:-translate-y-0.5",
              isSelected
                ? `border-emotion-${emotion.id} bg-emotion-${emotion.id}-bg`
                : "border-border bg-card hover:border-muted-foreground/30"
            )}
            style={{
              borderColor: isSelected ? `hsl(var(--emotion-${emotion.id}))` : undefined,
              backgroundColor: isSelected ? `hsl(var(--emotion-${emotion.id}-bg))` : undefined,
            }}
          >
            <Icon 
              className={cn(
                "h-6 w-6 transition-colors",
                isSelected ? "text-foreground" : "text-muted-foreground"
              )}
              style={{
                color: isSelected ? `hsl(var(--emotion-${emotion.id}))` : undefined,
              }}
            />
            <span className={cn(
              "text-sm font-medium",
              isSelected ? "text-foreground" : "text-muted-foreground"
            )}>
              {emotion.label}
            </span>
          </button>
        );
      })}
    </div>
  );
}
