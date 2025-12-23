/**
 * Quick test of emotion classifier and RDF generator
 * No network calls, just demonstrates the functionality
 */

const { classifyEmotion, aggregateEmotions } = require("./emotion_classifier");
const OnyxRDFGenerator = require("./onyx_rdf_generator");

// Sample reviews for testing
const sampleReviews = [
  "This is a masterpiece! Absolutely brilliant and wonderful. The acting was excellent and the plot was amazing. I loved every minute of it!",
  "Great film. Very entertaining and funny. I really enjoyed the storytelling and the cinematography was beautiful.",
  "Disappointed with this movie. It was boring and tedious. The characters were unlikeable and the ending was terrible.",
];

console.log("🔬 EMOTION CLASSIFICATION TEST\n");
console.log("=".repeat(60));

// Step 1: Classify each review
console.log("\n📊 Step 1: Classifying individual reviews...\n");
const classifications = sampleReviews.map((review, i) => {
  const result = classifyEmotion(review);
  console.log(`Review ${i + 1}:`);
  console.log(`  Text: "${review.substring(0, 60)}..."`);
  console.log(`  Dominant Emotion: ${result.dominantEmotion.toUpperCase()}`);
  console.log(`  Intensity: ${result.intensity}`);
  console.log(`  Confidence: ${result.confidence}`);
  console.log(`  All emotions:`, result.emotions);
  console.log();
  return result;
});

// Step 2: Aggregate emotions
console.log("=".repeat(60));
console.log("\n🎬 Step 2: Aggregating emotions across all reviews...\n");
const aggregation = aggregateEmotions(classifications);

console.log(
  `Aggregated Emotion: ${aggregation.aggregatedEmotion.toUpperCase()}`
);
console.log(`Vote Percentage: ${aggregation.votePercentage}%`);
console.log(`Average Intensity: ${aggregation.averageIntensity}`);
console.log(`Average Confidence: ${aggregation.averageConfidence}`);
console.log(`All Votes:`, aggregation.allVotes);

// Step 3: Generate RDF
console.log("\n=".repeat(60));
console.log("\n📄 Step 3: Generating RDF triples...\n");

const rdfGenerator = new OnyxRDFGenerator();
rdfGenerator.generateMovieEmotionRDF(
  "0123456",
  "Test Movie Title",
  classifications,
  aggregation
);

const rdfContent = rdfGenerator.generateTurtle();
console.log(rdfContent);

// Write to file
const fs = require("fs");
const path = require("path");
const outputPath = path.join(__dirname, "..", "test-emotions.ttl");
fs.writeFileSync(outputPath, rdfContent, "utf-8");

console.log("\n=".repeat(60));
console.log(`✅ Test complete! RDF written to: ${outputPath}`);
console.log(
  `   Statistics: ${rdfGenerator.getStats().moviesProcessed} movie(s), ${
    rdfGenerator.getStats().emotionsAnalyzed
  } emotions, ${rdfGenerator.getStats().triplesGenerated} triples`
);
