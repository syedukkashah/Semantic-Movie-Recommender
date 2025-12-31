import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// ===== TYPES =====
export interface Movie {
  movie_id: string;
  title: string;
  director: string;
  cast: string[];
  emotion: string;
  intensity: number;
  confidence: number;
  score: number;
}

export interface RecommendationRequest {
  emotion: string;
  intensity: number;
  count?: number;
}

export interface JourneyRequest {
  startEmotion: string;
  endEmotion: string;
  count?: number;
}

export interface RecommendationResponse {
  success: boolean;
  emotion: string;
  intensity: number;
  count: number;
  recommendations: Movie[];
}

export interface JourneyResponse {
  success: boolean;
  startEmotion: string;
  endEmotion: string;
  count: number;
  journey: Movie[];
}

export interface EmotionsResponse {
  emotions: string[];
}

// ===== API CLIENT =====
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ===== API FUNCTIONS =====

/**
 * Fetch list of supported emotions
 */
async function fetchEmotions(): Promise<string[]> {
  const response = await apiClient.get<EmotionsResponse>('/emotions');
  return response.data.emotions;
}

/**
 * Fetch movie recommendations based on emotion and intensity
 */
async function fetchRecommendations(
  params: RecommendationRequest
): Promise<Movie[]> {
  const response = await apiClient.post<RecommendationResponse>(
    '/recommend',
    params
  );
  return response.data.recommendations;
}

/**
 * Fetch emotion journey (mood progression sequence)
 */
async function fetchJourney(params: JourneyRequest): Promise<Movie[]> {
  const response = await apiClient.post<JourneyResponse>('/journey', params);
  return response.data.journey;
}

/**
 * Fetch popular/top-rated movies
 */
async function fetchPopularMovies(count: number = 10): Promise<Movie[]> {
  const response = await apiClient.get<{ recommendations: Movie[] }>(
    '/popular',
    {
      params: { count },
    }
  );
  return response.data.recommendations;
}

// ===== REACT QUERY HOOKS =====

/**
 * Hook to fetch supported emotions
 * Usage: const { data: emotions, isLoading, error } = useEmotions();
 */
export function useEmotions() {
  return useQuery({
    queryKey: ['emotions'],
    queryFn: fetchEmotions,
    staleTime: 1000 * 60 * 60, // 1 hour
  });
}

/**
 * Hook to fetch movie recommendations
 * Usage: const { data: movies, isLoading, error, refetch } = useRecommendations(emotion, intensity);
 */
export function useRecommendations(
  emotion: string | null,
  intensity: number = 0.5,
  count: number = 10
) {
  return useQuery({
    queryKey: ['recommendations', emotion, intensity, count],
    queryFn: () =>
      fetchRecommendations({
        emotion: emotion || 'joy',
        intensity,
        count,
      }),
    enabled: !!emotion, // Only run query if emotion is selected
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

/**
 * Hook to fetch emotion journey (mood progression)
 * Usage: const { data: journey, isLoading } = useJourney(start, end);
 */
export function useJourney(
  startEmotion: string | null,
  endEmotion: string | null,
  count: number = 5
) {
  return useQuery({
    queryKey: ['journey', startEmotion, endEmotion, count],
    queryFn: () =>
      fetchJourney({
        startEmotion: startEmotion || 'joy',
        endEmotion: endEmotion || 'joy',
        count,
      }),
    enabled: !!startEmotion && !!endEmotion && startEmotion !== endEmotion,
    staleTime: 1000 * 60 * 5,
  });
}

/**
 * Hook to fetch popular movies
 * Usage: const { data: popular } = usePopularMovies(10);
 */
export function usePopularMovies(count: number = 10) {
  return useQuery({
    queryKey: ['popular', count],
    queryFn: () => fetchPopularMovies(count),
    staleTime: 1000 * 60 * 30, // 30 minutes
  });
}

/**
 * Mutation hook for manual recommendation requests
 * Usage: const { mutate, isPending } = useRecommendationsMutation();
 */
export function useRecommendationsMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (params: RecommendationRequest) =>
      fetchRecommendations(params),
    onSuccess: () => {
      // Invalidate recommendations cache on success
      queryClient.invalidateQueries({ queryKey: ['recommendations'] });
    },
  });
}

export default apiClient;
