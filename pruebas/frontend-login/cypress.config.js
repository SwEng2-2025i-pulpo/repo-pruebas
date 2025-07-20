const { defineConfig } = require('cypress');
const generateNegativePDF = require('./utils/pdfNegativeReport');
const generateValidationPDF = require('./utils/pdfValidationReport');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173',
    supportFile: false,

    setupNodeEvents(on, config) {
      on('task', {
        generarPDFNegative({ title, testResult, validationMessage }) {
          return generateNegativePDF({ title, testResult, validationMessage }).then(() => null);
        },
        generarPDFValidation({ title, email, registro, login, resultado }) {
          return generateValidationPDF({ title, email, registro, login, resultado }).then(() => null);
        }
      });
    }
  },
});
