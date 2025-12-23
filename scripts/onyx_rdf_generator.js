/**
 * RDF Generator for Onyx Emotion Ontology
 * Converts emotion classifications to RDF triples
 */

const fs = require("fs");

class OnyxRDFGenerator {
  constructor() {
    this.triples = [];
    this.movieCount = 0;
    this.emotionCount = 0;

    // RDF namespaces
    this.namespaces = {
      rdf: "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
      rdfs: "http://www.w3.org/2000/01/rdf-schema#",
      xsd: "http://www.w3.org/2001/XMLSchema#",
      onyx: "http://www.gsi.dit.upm.es/ontologies/onyx/ns#",
      movie: "http://example.org/movie/",
      review: "http://example.org/review/",
      emotion: "http://example.org/emotion/",
    };
  }

  /**
   * Create RDF triple in Turtle format
   * @param {string} subject
   * @param {string} predicate
   * @param {string} object
   */
  addTriple(subject, predicate, object) {
    this.triples.push(`${subject} ${predicate} ${object} .`);
  }

  /**
   * Generate Onyx RDF for a movie with emotion classification
   * @param {string} movieId - IMDb movie ID (without 'tt')
   * @param {string} movieTitle - Movie title
   * @param {array} reviewClassifications - Array of emotion classifications
   * @param {object} aggregation - Aggregated emotion results
   */
  generateMovieEmotionRDF(movieId, movieTitle, reviewClassifications, aggregation) {
    const movieUri = `${this.namespaces.movie}${movieId}`;
    const emotionSetUri = `${this.namespaces.emotion}set_${movieId}`;

    // Movie entity
    this.addTriple(`<${movieUri}>`, "a", `${this.namespaces.onyx}Movie`);
    this.addTriple(
      `<${movieUri}>`,
      `${this.namespaces.rdfs}label`,
      `"${movieTitle}"`
    );

    // Create EmotionSet for the movie
    this.addTriple(
      `<${emotionSetUri}>`,
      "a",
      `${this.namespaces.onyx}AggregatedEmotionSet`
    );
    this.addTriple(
      `<${movieUri}>`,
      `${this.namespaces.onyx}hasEmotionSet`,
      `<${emotionSetUri}>`
    );

    // Add aggregated emotion
    const aggregatedEmotionUri = `${this.namespaces.emotion}agg_${movieId}`;
    this.addTriple(
      `<${aggregatedEmotionUri}>`,
      "a",
      `${this.namespaces.onyx}AggregatedEmotion`
    );
    this.addTriple(
      `<${emotionSetUri}>`,
      `${this.namespaces.onyx}hasEmotion`,
      `<${aggregatedEmotionUri}>`
    );

    // Emotion category (e.g., onyx:Joy)
    const emotionCategory = `${this.namespaces.onyx}${this._capitalizeFirstLetter(aggregation.aggregatedEmotion)}`;
    this.addTriple(
      `<${aggregatedEmotionUri}>`,
      `${this.namespaces.onyx}hasEmotionCategory`,
      `<${emotionCategory}>`
    );

    // Emotion intensity
    this.addTriple(
      `<${aggregatedEmotionUri}>`,
      `${this.namespaces.onyx}hasEmotionIntensity`,
      `"${aggregation.averageIntensity}"^^${this.namespaces.xsd}float`
    );

    // Algorithm confidence
    this.addTriple(
      `<${aggregatedEmotionUri}>`,
      `${this.namespaces.onyx}algorithmConfidence`,
      `"${aggregation.averageConfidence}"^^${this.namespaces.xsd}float`
    );

    // Vote percentage
    this.addTriple(
      `<${aggregatedEmotionUri}>`,
      `${this.namespaces.onyx}emoticonText`,
      `"${aggregation.votePercentage}% of reviews"`
    );

    // Algorithm info
    this.addTriple(
      `<${emotionSetUri}>`,
      `${this.namespaces.onyx}usesEmotionModel`,
      `"Naïve Bayes with NRC Lexicon"`
    );
    this.addTriple(
      `<${emotionSetUri}>`,
      `${this.namespaces.onyx}algorithm`,
      `"keyword-based classification"`
    );

    // Add individual review emotions (for detailed reference)
    reviewClassifications.forEach((classification, index) => {
      const reviewEmotionUri = `${this.namespaces.emotion}review_${movieId}_${index}`;
      const reviewUri = `${this.namespaces.review}${movieId}_${index}`;

      // Review entity
      this.addTriple(`<${reviewUri}>`, "a", `${this.namespaces.onyx}Review`);
      this.addTriple(
        `<${reviewUri}>`,
        `${this.namespaces.onyx}hasEmotion`,
        `<${reviewEmotionUri}>`
      );

      // Individual emotion
      this.addTriple(
        `<${reviewEmotionUri}>`,
        "a",
        `${this.namespaces.onyx}Emotion`
      );
      const reviewEmotionCat = `${this.namespaces.onyx}${this._capitalizeFirstLetter(classification.dominantEmotion)}`;
      this.addTriple(
        `<${reviewEmotionUri}>`,
        `${this.namespaces.onyx}hasEmotionCategory`,
        `<${reviewEmotionCat}>`
      );
      this.addTriple(
        `<${reviewEmotionUri}>`,
        `${this.namespaces.onyx}hasEmotionIntensity`,
        `"${classification.intensity}"^^${this.namespaces.xsd}float`
      );
      this.addTriple(
        `<${reviewEmotionUri}>`,
        `${this.namespaces.onyx}algorithmConfidence`,
        `"${classification.confidence}"^^${this.namespaces.xsd}float`
      );

      // Link review emotion to aggregated emotion
      this.addTriple(
        `<${aggregatedEmotionUri}>`,
        `${this.namespaces.onyx}aggregatesEmotion`,
        `<${reviewEmotionUri}>`
      );
    });

    this.movieCount++;
    this.emotionCount += reviewClassifications.length;
  }

  /**
   * Generate complete Turtle RDF document
   * @returns {string} - Turtle RDF content
   */
  generateTurtle() {
    let turtleContent = this._generatePrefixes();
    turtleContent += "\n\n# ===== EMOTION CLASSIFICATION RESULTS =====\n\n";
    turtleContent += this.triples.join("\n");
    turtleContent += `\n\n# Generated: ${new Date().toISOString()}`;
    turtleContent += `\n# Movies processed: ${this.movieCount}`;
    turtleContent += `\n# Emotions analyzed: ${this.emotionCount}`;

    return turtleContent;
  }

  /**
   * Append RDF triples to existing file
   * @param {string} filePath - Path to .ttl file
   */
  appendToFile(filePath) {
    const newContent = "\n\n# ===== EMOTION CLASSIFICATIONS =====\n\n";
    const turtleTriples = this.triples.join("\n");
    fs.appendFileSync(filePath, newContent + turtleTriples);
    console.log(`✅ RDF triples appended to ${filePath}`);
  }

  /**
   * Write RDF to new file
   * @param {string} filePath - Path to output .ttl file
   */
  writeToFile(filePath) {
    const content = this.generateTurtle();
    fs.writeFileSync(filePath, content, "utf-8");
    console.log(`✅ RDF document written to ${filePath}`);
    console.log(`   Movies: ${this.movieCount} | Emotions: ${this.emotionCount}`);
  }

  /**
   * Get statistics about generated RDF
   */
  getStats() {
    return {
      moviesProcessed: this.movieCount,
      emotionsAnalyzed: this.emotionCount,
      triplesGenerated: this.triples.length,
    };
  }

  /**
   * Helper: Generate Turtle prefixes
   */
  _generatePrefixes() {
    return `@prefix rdf: <${this.namespaces.rdf}> .
@prefix rdfs: <${this.namespaces.rdfs}> .
@prefix xsd: <${this.namespaces.xsd}> .
@prefix onyx: <${this.namespaces.onyx}> .
@prefix movie: <${this.namespaces.movie}> .
@prefix review: <${this.namespaces.review}> .
@prefix emotion: <${this.namespaces.emotion}> .`;
  }

  /**
   * Helper: Capitalize first letter
   */
  _capitalizeFirstLetter(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
}

module.exports = OnyxRDFGenerator;
