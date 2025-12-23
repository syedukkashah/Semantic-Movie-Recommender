const axios = require("axios");
const puppeteer = require("puppeteer");
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const { classifyEmotion, aggregateEmotions } = require("./emotion_classifier");
const OnyxRDFGenerator = require("./onyx_rdf_generator");
const path = require("path");
// ===== STEP 1: Query Wikidata =====
async function queryWikidataMovies(filterQuery) {
  const sparqlQuery = `
    SELECT ?movie ?movieLabel ?imdbId WHERE {
      ?movie wdt:P31 wd:Q11424 .
      ?movie wdt:P345 ?imdbId .
      ${filterQuery}
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
    }
    LIMIT 20
    `;

  const url = "https://query.wikidata.org/sparql";

  try {
    console.log("🔍 Querying Wikidata for movies...\n");
    const response = await axios.get(url, {
      params: {
        query: sparqlQuery,
        format: "json",
      },
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
      },
    });

    const results = response.data.results.bindings;

    if (results.length === 0) {
      console.log("❌ No movies found. Check your filter query.");
      return [];
    }

    const movieIds = results.map((r) => r.imdbId.value.replace("tt", ""));

    console.log(`✅ Found ${movieIds.length} movies:\n`);
    results.forEach((r, i) => {
      console.log(`   [${i + 1}] ${r.movieLabel.value} (${r.imdbId.value})`);
    });

    return movieIds;
  } catch (error) {
    console.error("❌ Error querying Wikidata:", error.message);
    return [];
  }
}

// ===== STEP 2: Scrape Reviews =====
async function scrapeMovieReviews(movieIds) {
  if (movieIds.length === 0) {
    console.log("No movie IDs to scrape.");
    return [];
  }

  const browser = await puppeteer.launch({ headless: true });
  const rdfGenerator = new OnyxRDFGenerator();
  const moviesData = [];

  console.log(
    `\n📺 Starting review scraper for ${movieIds.length} movies...\n`
  );

  for (const id of movieIds) {
    const page = await browser.newPage();
    try {
      console.log(`🔍 Fetching reviews for ID: ${id}...`);

      const url = `https://www.imdb.com/title/tt${id}/reviews`;
      await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      );
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });

      const reviews = await page.evaluate(() => {
        const reviewTexts = [];
        const reviewContainers = document.querySelectorAll('[class*="review"]');

        reviewContainers.forEach((container) => {
          const text = container.innerText?.trim();
          if (
            text &&
            text.length > 150 &&
            text.length < 2000 &&
            !text.includes("Sign in") &&
            !text.includes("JavaScript") &&
            !text.includes("Ratings") &&
            !text.includes("stars") &&
            text.split(" ").length > 15
          ) {
            reviewTexts.push(text);
          }
        });

        const uniqueReviews = [...new Set(reviewTexts)].slice(0, 3);
        return uniqueReviews;
      });

      if (reviews.length > 0) {
        console.log(`✅ Found ${reviews.length} reviews:`);
        reviews.forEach((r, i) =>
          console.log(`   [${i + 1}] ${r.substring(0, 80)}...`)
        );

        // ===== STEP 3: Emotion Classification (Naïve Bayes) =====
        console.log(`\n📊 Classifying emotions...`);
        const classificationResults = reviews.map((review) =>
          classifyEmotion(review)
        );

        // Display individual emotion classifications
        classificationResults.forEach((result, i) => {
          console.log(
            `   [${i + 1}] ${result.dominantEmotion.toUpperCase()} (intensity: ${result.intensity}, confidence: ${result.confidence})`
          );
        });

        // ===== STEP 4: Aggregation =====
        console.log(`\n🎬 Aggregating emotions across reviews...`);
        const aggregation = aggregateEmotions(classificationResults);

        console.log(
          `   ➤ Dominant emotion: ${aggregation.aggregatedEmotion.toUpperCase()}`
        );
        console.log(`   ➤ Vote percentage: ${aggregation.votePercentage}%`);
        console.log(`   ➤ Average intensity: ${aggregation.averageIntensity}`);
        console.log(
          `   ➤ Average confidence: ${aggregation.averageConfidence}`
        );
        console.log(
          `   ➤ All votes: ${JSON.stringify(aggregation.allVotes)}\n`
        );

        // ===== STEP 5: Generate RDF =====
        const movieTitle = await page.evaluate(() => {
          const titleElement = document.querySelector("h1");
          return titleElement ? titleElement.innerText : "Unknown";
        });

        rdfGenerator.generateMovieEmotionRDF(
          id,
          movieTitle,
          classificationResults,
          aggregation
        );

        moviesData.push({
          id,
          title: movieTitle,
          aggregation,
          classificationResults,
        });
      } else {
        console.log(`⚠️  No reviews found for movie ${id}`);
      }

      console.log(`⏳ Waiting 10 seconds before next movie...\n`);
      await sleep(10000);
    } catch (error) {
      console.error(`❌ Error fetching ${id}:`, error.message);
    } finally {
      await page.close();
    }
  }

  await browser.close();

  // ===== Write RDF to file =====
  const outputPath = path.join(__dirname, "..", "movie-emotions.ttl");
  rdfGenerator.writeToFile(outputPath);

  console.log("\n✅ Scraping and classification complete!");
  return moviesData;
}

// ===== MAIN: Orchestrate Both Steps =====
async function main() {
  // CUSTOMIZE YOUR QUERY HERE:
  const filterQuery = `?movie wdt:P577 ?date . FILTER(YEAR(?date) = 1950)`;

  // Uncomment for other queries:
  // const filterQuery = `?movie wdt:P57 wd:Q3665 .`;  // Stanley Kubrick
  // const filterQuery = `?movie wdt:P136 wd:Q9826970 .`;  // Action films
  // const filterQuery = `?movie wdt:P166 wd:Q19020 .`;  // Oscar winners

  const movieIds = await queryWikidataMovies(filterQuery);
  await scrapeMovieReviews(movieIds);
}

main().catch(console.error);
