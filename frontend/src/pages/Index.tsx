import { useState, useEffect } from "react";
import { Loader2, AlertCircle } from "lucide-react";
import { EmotionSelector, type Emotion } from "@/EmotionSelector";
import { IntensitySlider } from "@/IntensitySlider";
import { MovieCard } from "@/MovieCard";
import { useRecommendations } from "@/hooks/useRecommendations";
import { Button } from "@/components/ui/button";
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert";
import { useToast } from "@/hooks/use-toast";

// Map backend emotions to frontend emotions (no mapping needed now - all 7 emotions supported)
const emotionMap: Record<string, Emotion> = {
  joy: "joy",
  sadness: "sadness",
  fear: "fear",
  anger: "anger",
  disgust: "disgust",
  surprise: "surprise",
  trust: "trust",
};

export default function Index() {
  const { toast } = useToast();
  
  // State management
  const [selectedEmotion, setSelectedEmotion] = useState<Emotion | null>(null);
  const [intensity, setIntensity] = useState<number>(50);
  const [count, setCount] = useState<number>(10);
  
  // API hooks
  const { 
    data: recommendations, 
    isLoading, 
    error, 
    refetch 
  } = useRecommendations(
    selectedEmotion as string | null, 
    intensity / 100, // Convert percentage to 0-1 range
    count
  );

  // Handle emotion selection
  const handleEmotionSelect = (emotion: Emotion) => {
    setSelectedEmotion(emotion);
    toast({
      title: "Emotion selected",
      description: `Finding movies that match your ${emotion} mood...`,
    });
  };

  // Handle intensity change
  const handleIntensityChange = (value: number) => {
    setIntensity(value);
  };

  // Handle error state
  useEffect(() => {
    if (error) {
      toast({
        title: "Error fetching recommendations",
        description: error instanceof Error ? error.message : "Please try again",
        variant: "destructive",
      });
    }
  }, [error, toast]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
              <span className="text-white font-bold">🎬</span>
            </div>
            <h1 className="text-2xl font-bold text-foreground">
              Emotion-Based Movie Recommender
            </h1>
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            Select an emotion and intensity to discover movies that match your mood
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Selection Panel */}
        <div className="bg-card rounded-2xl border border-border p-8 shadow-lg mb-12">
          <div className="space-y-8">
            {/* Emotion Selector */}
            <div>
              <h2 className="text-lg font-semibold text-foreground mb-4">
                How are you feeling?
              </h2>
              <EmotionSelector
                selectedEmotion={selectedEmotion}
                onSelect={handleEmotionSelect}
              />
            </div>

            {/* Intensity Slider */}
            {selectedEmotion && (
              <div className="border-t border-border pt-8">
                <IntensitySlider
                  value={intensity}
                  onChange={handleIntensityChange}
                />
                <p className="text-xs text-muted-foreground mt-4">
                  {intensity}% intensity selected for finding{" "}
                  <span className="font-medium capitalize text-foreground">
                    {selectedEmotion}
                  </span>{" "}
                  movies
                </p>
              </div>
            )}

            {/* Results Count Selector */}
            {selectedEmotion && (
              <div className="border-t border-border pt-8">
                <label className="text-sm font-medium text-foreground block mb-3">
                  Number of recommendations
                </label>
                <div className="flex gap-2 flex-wrap">
                  {[5, 10, 15, 20].map((num) => (
                    <Button
                      key={num}
                      variant={count === num ? "default" : "outline"}
                      size="sm"
                      onClick={() => {
                        setCount(num);
                        refetch();
                      }}
                    >
                      {num}
                    </Button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Recommendations Section */}
        {selectedEmotion && (
          <div className="space-y-6">
            <div className="flex items-center gap-3">
              <h2 className="text-2xl font-bold text-foreground">
                Recommended Movies
              </h2>
              {isLoading && (
                <Loader2 className="h-5 w-5 text-primary animate-spin" />
              )}
            </div>

            {/* Error State */}
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>
                  Failed to fetch recommendations. Make sure the API server is running
                  on http://localhost:5000
                </AlertDescription>
              </Alert>
            )}

            {/* Loading State */}
            {isLoading && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[...Array(3)].map((_, i) => (
                  <div
                    key={i}
                    className="bg-card rounded-xl p-5 border border-border animate-pulse"
                  >
                    <div className="h-6 bg-muted rounded w-3/4 mb-4" />
                    <div className="h-4 bg-muted rounded w-1/2" />
                  </div>
                ))}
              </div>
            )}

            {/* Recommendations Grid */}
            {recommendations && recommendations.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {recommendations.map((movie, index) => (
                  <MovieCard
                    key={movie.movie_id}
                    title={movie.title}
                    emotion={
                      (emotionMap[movie.emotion] as Emotion) || "joy"
                    }
                    confidence={Math.round(movie.confidence * 100)}
                    director={movie.director}
                    description={movie.description}
                    delay={index * 50}
                  />
                ))}
              </div>
            ) : !isLoading && !error ? (
              <div className="text-center py-12">
                <p className="text-muted-foreground text-lg">
                  No recommendations found. Try a different emotion or intensity.
                </p>
              </div>
            ) : null}
          </div>
        )}

        {/* Empty State */}
        {!selectedEmotion && (
          <div className="text-center py-16">
            <div className="w-24 h-24 rounded-full bg-muted/30 mx-auto mb-6 flex items-center justify-center">
              <span className="text-5xl">😊</span>
            </div>
            <h3 className="text-xl font-semibold text-foreground mb-2">
              What's your mood?
            </h3>
            <p className="text-muted-foreground max-w-md mx-auto">
              Select an emotion above to get personalized movie recommendations based
              on how you're feeling right now.
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-border/40 bg-muted/20 mt-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center text-sm text-muted-foreground">
          <p>
            Emotion-Based Movie Recommender • Powered by Semantic Web & SPARQL
          </p>
        </div>
      </footer>
    </div>
  );
}
