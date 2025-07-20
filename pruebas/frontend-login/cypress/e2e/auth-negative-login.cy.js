describe('Login con credenciales incorrectas', () => {
  const email = 'usuario-no-existe@example.com';
  const password = 'ContraseñaIncorrecta123!';

  it('debería mostrar mensaje de error al usar credenciales inválidas', () => {
    cy.visit('/login');
    cy.get('#email').type(email);
    cy.get('#password').type(password);
    cy.contains('Ingresar').click();

    cy.wait(500); // Esperar a que aparezca el mensaje

    // Verifica el mensaje de error mostrado (ajusta si tu app usa otro texto)
    cy.contains('Error al iniciar sesión: Credenciales inválidas').should('be.visible');

    // Generar PDF de resultado negativo
    cy.task('generarPDFNegative', {
      title: 'Reporte de Login Fallido',
      testResult: 'Fallido - Credenciales incorrectas',
      validationMessage: 'El sistema rechazó las credenciales como era esperado.'
    });
  });
});
