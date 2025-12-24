//DELETE ONCE OG VERSION IS UPDATED 

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

// ===== NAÏVE BAYES SETUP =====

// All emotion classes
const EMOTIONS = Object.keys(emotionLexicon);

// 1️ Priors P(emotion) — assume uniform
const emotionPriors = {};
EMOTIONS.forEach((e) => {
  emotionPriors[e] = 1 / EMOTIONS.length;
});

// 2️ Build vocabulary from lexicon
const vocabulary = new Set();
Object.values(emotionLexicon).forEach((words) => {
  words.forEach((w) => vocabulary.add(w));
});
const VOCAB_SIZE = vocabulary.size;

// 3️ Likelihoods P(word | emotion) with Laplace smoothing
const likelihoods = {};

EMOTIONS.forEach((emotion) => {
  likelihoods[emotion] = {};
  const emotionWords = emotionLexicon[emotion];
  const totalWords = emotionWords.length;

  vocabulary.forEach((word) => {
    const count = emotionWords.includes(word) ? 1 : 0;
    likelihoods[emotion][word] =
      (count + 1) / (totalWords + VOCAB_SIZE);
  });
});


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
  const words = reviewText.toLowerCase().split(/\s+/);

  const logScores = {};
const emotionWordCounts = {};
EMOTIONS.forEach(e => emotionWordCounts[e] = 0);


  // 4️ Apply Naïve Bayes formula
  EMOTIONS.forEach((emotion) => {
    let logProb = Math.log(emotionPriors[emotion]);

    words.forEach((word) => {
     if (vocabulary.has(word)) {
  logProb += Math.log(likelihoods[emotion][word]);

  // Count ONLY if word belongs to this emotion
  if (emotionLexicon[emotion].includes(word)) {
    emotionWordCounts[emotion] += 1;
  }
}

    });

    logScores[emotion] = logProb;
  });

  // 5️ Pick best emotion
  let dominantEmotion = "neutral";
  let maxScore = -Infinity;

  for (const [emotion, score] of Object.entries(logScores)) {
    if (score > maxScore) {
      maxScore = score;
      dominantEmotion = emotion;
    }
  }

  // 6️ Normalize to probabilities
  const expScores = {};
  let sum = 0;

  for (const [e, s] of Object.entries(logScores)) {
    expScores[e] = Math.exp(s - maxScore);
    sum += expScores[e];
  }

  const probabilities = {};
  for (const e of Object.keys(expScores)) {
    probabilities[e] = expScores[e] / sum;
  }

  // 7️ Intensity + confidence (same idea as before)
  const sorted = Object.values(probabilities).sort((a, b) => b - a);
  const confidence = sorted[0] - (sorted[1] || 0) > 0.1 ? 0.9 : 0.7;
  const intensity = Math.min(probabilities[dominantEmotion] * 2, 1.0);

  return {
    dominantEmotion,
    emotions: probabilities,
     emotionWordCounts,
    intensity: Math.round(intensity * 100) / 100,
    confidence,
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

 // Count total emotion WORD frequencies across all reviews
classificationResults.forEach((result) => {
  for (const [emotion, count] of Object.entries(result.emotionWordCounts)) {
    emotionVotes[emotion] = (emotionVotes[emotion] || 0) + count;
  }
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

  const votePercentage = Math.round(
    (maxVotes / classificationResults.length) * 100
  );

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
