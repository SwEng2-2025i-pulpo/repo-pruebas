const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:5173", // Cambia esto según tu frontend
    supportFile: "cypress/support/e2e.js",
    screenshotOnRunFailure: false,
    screenshotsFolder: false,
    video: false
  }
}); 


