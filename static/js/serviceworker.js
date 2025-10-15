const assets = [
  "/",
  "/static/css/style.css",
  "/static/css/base.css",
  "/static/css/chat.css",
  "/static/css/home.css",
  "/static/css/layout.css",
  "/static/css/login.css",
  "/static/css/schedule.css",
  "/static/css/signup.css",
  "/static/css/speech.css",
  "/static/js/app.js",
  "/static/js/chat.js",
  "/static/js/signup.js",
  "/static/images/logo.png",
  "/static/images/Accord.png",
  "/static/images/Chat.png",
  "/static/images/home.png",
  "/static/images/Homepage.png",
  "/static/images/jilm.png",
  "/static/images/Login.png",
  "/static/images/messages.png",
  "/static/images/newalgorithmdesign.png",
  "/static/images/sendmessage.png",
  "/static/images/Signup.png",
  "/static/images/timetable.png",
  "/static/images/timetableicon.png",
  "/static/images/Timetablepage.png",
  "/static/images/user.png",
  "/static/images/week3alternate.png",
];

const CATALOGUE_ASSETS = "catalogue-assets";

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CATALOGUE_ASSETS)
      .then((cache) => {
        console.log("Caching assets...");
        return cache.addAll(assets);
      })
      .then(() => self.skipWaiting())
      .catch((e) => {
        console.error("Install error:", e);
      })
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keyList) => {
        return Promise.all(
          keyList.map((key) => {
            if (key !== CATALOGUE_ASSETS) {
              console.log("Removing old cache:", key);
              return caches.delete(key);
            }
          })
        );
      })
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.open(CATALOGUE_ASSETS).then((cache) => {
        return cache.match(event.request);
      });
    })
  );
});