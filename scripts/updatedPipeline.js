/**
 * PIPELINE STEP 1
 * ----------------
 * JavaScript layer for:
 *  - Querying Wikidata
 *  - Scraping IMDb reviews
 *  - Writing RAW reviews to JSON
 *
 * NO emotion classification
 * NO aggregation
 * NO RDF generation
 */

const axios = require("axios");
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));


// ===== STEP 1: Query Wikidata =====
async function queryWikidataMovies(filterQuery) {
  const sparqlQuery = `
    SELECT ?movie ?movieLabel ?imdbId WHERE {
      ?movie wdt:P31 wd:Q11424 .
      ?movie wdt:P345 ?imdbId .
      ${filterQuery}
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
    }
    LIMIT 10
  `;

  try {
    console.log("🔍 Querying Wikidata...\n");

    const response = await axios.get(
      "https://query.wikidata.org/sparql",
      {
        params: { query: sparqlQuery, format: "json" },
        headers: { "User-Agent": "Mozilla/5.0" },
      }
    );

    const results = response.data.results.bindings;

    if (results.length === 0) {
      console.log("❌ No movies found.");
      return [];
    }

    const movies = results.map((r) => ({
      movieId: r.imdbId.value.replace("tt", ""),
      title: r.movieLabel.value,
    }));

    console.log(`✅ Found ${movies.length} movies:\n`);
    movies.forEach((m, i) =>
      console.log(`   [${i + 1}] ${m.title} (tt${m.movieId})`)
    );

    return movies;
  } catch (error) {
    console.error("❌ Wikidata query failed:", error.message);
    return [];
  }
}


// ===== STEP 2: Scrape IMDb Reviews ONLY =====
async function scrapeMovieReviews(movies) {
  if (movies.length === 0) {
    console.log("⚠️ No movies to scrape.");
    return;
  }

  const browser = await puppeteer.launch({ headless: true });
  const allMoviesData = [];

  console.log(`\n📺 Scraping reviews for ${movies.length} movies...\n`);

  for (const movie of movies) {
    const page = await browser.newPage();

    try {
      const url = `https://www.imdb.com/title/tt${movie.movieId}/reviews`;
      console.log(`🔍 Scraping: ${movie.title}`);

      await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
      );

      await page.goto(url, {
        waitUntil: "domcontentloaded",
        timeout: 30000,
      });

      const reviews = await page.evaluate(() => {
        const texts = [];
        const nodes = document.querySelectorAll('[class*="review"]');

        nodes.forEach((node) => {
          const text = node.innerText?.trim();
          if (
            text &&
            text.length > 150 &&
            text.length < 2000 &&
            !text.includes("Sign in") &&
            !text.includes("Ratings") &&
            text.split(" ").length > 15
          ) {
            texts.push(text);
          }
        });

        return [...new Set(texts)].slice(0, 3);
      });

      console.log(`   ✅ ${reviews.length} reviews collected\n`);

      allMoviesData.push({
        movieId: movie.movieId,
        title: movie.title,
        reviews: reviews,
      });

      await page.close();
      await sleep(5000);

    } catch (err) {
      console.error(`❌ Error scraping ${movie.title}:`, err.message);
      await page.close();
    }
  }

  await browser.close();

  // ===== WRITE RAW DATA TO JSON =====
  const outputPath = path.join(__dirname, "..", "reviews.json");
  fs.writeFileSync(
    outputPath,
    JSON.stringify(allMoviesData, null, 2),
    "utf-8"
  );

  console.log(`\n✅ Raw reviews written to ${outputPath}`);
}


// ===== MAIN =====
async function main() {
  const filterQuery = `?movie wdt:P577 ?date . FILTER(YEAR(?date) = 1950)`;

  const movies = await queryWikidataMovies(filterQuery);
  await scrapeMovieReviews(movies);
}

main().catch(console.error);
