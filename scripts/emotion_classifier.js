/**
 * Emotion Classifier using Naïve Bayes approach
 * Based on NRC Emotion Lexicon (emotion keywords)
 * Outputs: emotion category, intensity [0-1], and confidence score
 */

// NRC Emotion Lexicon - Pre-trained emotion keywords
const emotionLexicon = {
  joy: [
    "excellent",
    "wonderful",
    "masterpiece",
    "amazing",
    "love",
    "great",
    "fantastic",
    "brilliant",
    "perfect",
    "beautiful",
    "delightful",
    "gorgeous",
    "impressive",
    "funny",
    "hilarious",
    "entertaining",
    "enjoyable",
    "pleasant",
    "happy",
    "cheerful",
    "triumph",
    "victory",
    "success",
  ],
  sadness: [
    "sad",
    "depressing",
    "tragic",
    "sorrowful",
    "melancholy",
    "heartbreak",
    "tears",
    "suffer",
    "pain",
    "loss",
    "grief",
    "disappointing",
    "disappointed",
    "boring",
    "dull",
    "tedious",
    "awful",
    "terrible",
    "worst",
    "hate",
    "hated",
    "dislike",
  ],
  fear: [
    "scary",
    "terrifying",
    "horror",
    "frightening",
    "horrific",
    "dreadful",
    "ominous",
    "suspense",
    "tense",
    "unsettling",
    "disturbing",
    "creepy",
    "eerie",
    "sinister",
    "evil",
    "menace",
  ],
  anger: [
    "angry",
    "rage",
    "furious",
    "outraged",
    "infuriating",
    "annoying",
    "irritating",
    "frustrating",
    "despicable",
    "insulting",
    "offensive",
    "ridiculous",
    "disgusting",
    "vile",
    "repugnant",
    "abhorrent",
  ],
  disgust: [
    "disgusting",
    "repulsive",
    "vile",
    "filthy",
    "gross",
    "revolting",
    "nauseating",
    "abominable",
    "loathsome",
    "repugnant",
    "despicable",
    "detestable",
  ],
  surprise: [
    "surprising",
    "unexpected",
    "astonishing",
    "astounding",
    "shocking",
    "amazing",
    "incredible",
    "remarkable",
    "startling",
    "stunning",
    "bewildering",
    "confounding",
  ],
  trust: [
    "reliable",
    "trustworthy",
    "credible",
    "dependable",
    "solid",
    "strong",
    "confident",
    "assured",
    "capable",
    "competent",
    "skilled",
    "professional",
    "authentic",
    "genuine",
    "honest",
  ],
};

// Negative intensity markers (weaken emotion score)
const negationWords = [
  "not",
  "no",
  "neither",
  "never",
  "hardly",
  "scarcely",
  "barely",
];

// Intensifier words (strengthen emotion score)
const intensifiers = [
  "very",
  "extremely",
  "incredibly",
  "absolutely",
  "truly",
  "really",
  "so",
  "quite",
  "rather",
  "most",
];

/**
 * Naïve Bayes Emotion Classification
 * @param {string} reviewText - The review to classify
 * @returns {object} - { dominantEmotion, emotions, intensity, confidence }
 */
function classifyEmotion(reviewText) {
  const text = reviewText.toLowerCase();
  const words = text.split(/\s+/);

  // Count emotion keywords in text
  const emotionScores = {};
  let totalEmotionKeywords = 0;

  for (const [emotion, keywords] of Object.entries(emotionLexicon)) {
    emotionScores[emotion] = 0;

    keywords.forEach((keyword) => {
      // Count occurrences of each emotion keyword
      const regex = new RegExp(`\\b${keyword}\\b`, "gi");
      const matches = text.match(regex);

      if (matches) {
        const count = matches.length;
        emotionScores[emotion] += count;
        totalEmotionKeywords += count;
      }
    });
  }

  // Apply Naïve Bayes probability: P(emotion|text) ∝ count(emotion_keywords) / total_keywords
  const emotionProbabilities = {};
  for (const [emotion, score] of Object.entries(emotionScores)) {
    emotionProbabilities[emotion] =
      totalEmotionKeywords > 0 ? score / totalEmotionKeywords : 0;
  }

  // Find dominant emotion
  let dominantEmotion = "neutral";
  let maxProbability = 0;

  for (const [emotion, prob] of Object.entries(emotionProbabilities)) {
    if (prob > maxProbability) {
      maxProbability = prob;
      dominantEmotion = emotion;
    }
  }

  // Calculate intensity based on:
  // 1. Keyword frequency
  // 2. Review length (longer = more developed emotion)
  // 3. Intensifier words
  const intensifierCount = intensifiers.filter((word) =>
    text.includes(word)
  ).length;
  const baseIntensity = Math.min(maxProbability * 2, 1.0); // Scale to [0,1]
  const intensifierBoost = Math.min(intensifierCount * 0.05, 0.2); // Max +0.2 from intensifiers
  const intensity = Math.min(baseIntensity + intensifierBoost, 1.0);

  // Confidence = how dominant is the top emotion
  // High confidence if one emotion is clearly stronger than others
  const emotionProbs = Object.values(emotionProbabilities).sort(
    (a, b) => b - a
  );
  const confidence =
    emotionProbs[0] - (emotionProbs[1] || 0) > 0.1 ? 0.9 : 0.7; // High if gap > 0.1

  return {
    dominantEmotion,
    emotions: emotionProbabilities,
    intensity: Math.round(intensity * 100) / 100,
    confidence: Math.round(confidence * 100) / 100,
    keywordCount: totalEmotionKeywords,
  };
}

/**
 * Aggregate emotions from multiple reviews
 * @param {array} classificationResults - Array of emotion classification results
 * @returns {object} - Aggregated emotion with voting results
 */
function aggregateEmotions(classificationResults) {
  const emotionVotes = {};
  let totalIntensity = 0;
  let totalConfidence = 0;

  // Count votes for each emotion
  classificationResults.forEach((result) => {
    const emotion = result.dominantEmotion;
    emotionVotes[emotion] = (emotionVotes[emotion] || 0) + 1;
    totalIntensity += result.intensity;
    totalConfidence += result.confidence;
  });

  // Find dominant emotion by vote count
  let aggregatedEmotion = "neutral";
  let maxVotes = 0;

  for (const [emotion, votes] of Object.entries(emotionVotes)) {
    if (votes > maxVotes) {
      maxVotes = votes;
      aggregatedEmotion = emotion;
    }
  }

  const votePercentage =
    Math.round((maxVotes / classificationResults.length) * 100);

  return {
    aggregatedEmotion,
    votePercentage,
    allVotes: emotionVotes,
    averageIntensity:
      Math.round((totalIntensity / classificationResults.length) * 100) / 100,
    averageConfidence:
      Math.round((totalConfidence / classificationResults.length) * 100) / 100,
  };
}

module.exports = {
  classifyEmotion,
  aggregateEmotions,
  emotionLexicon,
};
