import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Home } from "lucide-react";

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20 flex items-center justify-center px-4">
      <div className="text-center space-y-6 max-w-md">
        {/* 404 Illustration */}
        <div className="space-y-4">
          <div className="text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-pink-500">
            404
          </div>
          <h1 className="text-3xl font-bold text-foreground">
            Page Not Found
          </h1>
          <p className="text-muted-foreground">
            Oops! We couldn't find the movie recommendation you were looking for.
          </p>
        </div>

        {/* Decorative emoji */}
        <div className="text-6xl">🎬</div>

        {/* Action Buttons */}
        <div className="flex gap-3 justify-center pt-4">
          <Button
            variant="outline"
            onClick={() => navigate(-1)}
            className="gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Go Back
          </Button>
          <Button
            onClick={() => navigate("/")}
            className="gap-2"
          >
            <Home className="h-4 w-4" />
            Home
          </Button>
        </div>

        {/* Additional Help */}
        <div className="pt-8 border-t border-border">
          <p className="text-sm text-muted-foreground mb-4">
            Looking for something?
          </p>
          <p className="text-sm text-muted-foreground">
            Visit the home page to discover movies based on your emotions.
          </p>
        </div>
      </div>
    </div>
  );
}
