const BASE_URL = import.meta.env.VITE_API_URL || "https://moviefinder-k306.onrender.com/api";
const WARMUP_TIMEOUT = 5000; // 5 seconds
const SESSION_KEY = "backend_warmed_up";

let warmupPromise = null;

/**
 * Sends a background request to the health endpoint to wake up the backend.
 * Only runs once per session.
 */
export const warmupBackend = () => {
  // Already warming up or already warmed up in this session
  if (warmupPromise || sessionStorage.getItem(SESSION_KEY)) {
    return warmupPromise || Promise.resolve();
  }

  console.log("Starting backend warm-up...");

  warmupPromise = new Promise((resolve) => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      console.warn("Backend warm-up timed out.");
      controller.abort();
      resolve(); // Resolve anyway to not block app
    }, WARMUP_TIMEOUT);

    fetch(`${BASE_URL}/health`, {
      signal: controller.signal,
      mode: "cors",
    })
      .then((res) => {
        if (res.ok) {
          console.log("Backend is awake! ✅");
          sessionStorage.setItem(SESSION_KEY, "true");
        }
      })
      .catch((err) => {
        console.error("Backend warm-up failed:", err);
      })
      .finally(() => {
        clearTimeout(timeoutId);
        resolve();
      });
  });

  return warmupPromise;
};

/**
 * A wrapper for fetch that ensures the warm-up has at least been initiated.
 * @param {string} endpoint - The API endpoint (e.g., /login)
 * @param {object} options - Fetch options
 * @param {boolean} awaitWarmup - Whether to wait for the warm-up to complete before sending
 */
export const backendFetch = async (
  endpoint,
  options = {},
  awaitWarmup = false,
) => {
  if (awaitWarmup) {
    await warmupBackend();
  } else {
    // Just trigger it if not already started
    warmupBackend();
  }

  const url = endpoint.startsWith("http") ? endpoint : `${BASE_URL}${endpoint}`;
  return fetch(url, options);
};
