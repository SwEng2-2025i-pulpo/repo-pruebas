Cypress.Commands.add('login', () => {
  cy.visit('/login');
  cy.get('input[placeholder="Email"]').type('sgarciarod@unal.edu.co');
  cy.get('input[placeholder="Contraseña"]').type('Cuidador|2025');
  cy.contains('Ingresar').click();
  cy.url().should('not.include', '/login');
});