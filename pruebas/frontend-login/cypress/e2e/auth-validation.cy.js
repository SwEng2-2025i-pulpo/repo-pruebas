describe('Signup', () => {
  const email = `test${Date.now()}@example.com`;
  const password = 'ValidPass1!';

  it('debería crear una cuenta y mostrar mensaje de éxito', () => {
    cy.visit('/SignUp');
    cy.get('#name').type('Juan');
    cy.get('#last_name').type('Pérez');
    cy.get('#email').type(email);
    cy.get('#password').type(password);
    cy.get('#confirm_password').type(password);
    cy.get('form.signup__form').contains('Crear Cuenta').click({ force: true });

    cy.contains('¡Cuenta creada exitosamente!', { timeout: 10000 }).should('be.visible');
    cy.url({ timeout: 10000 }).should('include', '/login');
  });

  it('debería iniciar sesión con la cuenta recién creada', () => {
    cy.visit('/login');
    cy.get('#email').type(email);
    cy.get('#password').type(password);
    cy.contains('Ingresar').click();

    // cy.contains('¡Inicio de sesión exitoso!', { timeout: 10000 }).should('be.visible');
    cy.wait(200); // esperar un poco por seguridad
    cy.get('body').should('include.text', 'Bienvenido a ConectaCare');
    cy.url({ timeout: 10000 }).should('eq', 'http://localhost:5173/');

    cy.task('generarPDFValidation', {
    title: 'Reporte de Validación de Registro/Login',
    email,
    registro: 'Exitoso',
    login: 'Exitoso',
    resultado: 'Completado con éxito'
  });

  });
});
