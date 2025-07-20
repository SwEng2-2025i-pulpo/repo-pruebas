describe('Validación del formulario de registro - Datos inválidos', () => {
  const emailInvalido = 'usuario-invalido'; // sin @ ni dominio
  const passwordInvalida = 'contrasena123'; // no tiene carácter especial

  it('no debería permitir registro con correo y contraseña inválidos', () => {
    cy.visit('/SignUp');

    cy.get('#name').type('Nombre');
    cy.get('#last_name').type('Apellido');
    cy.get('#email').type(emailInvalido);
    cy.get('#password').type(passwordInvalida);
    cy.get('#confirm_password').type(passwordInvalida);

    // Aunque los campos sean inválidos, el botón se puede presionar
    cy.get('form.signup__form').contains('Crear Cuenta').click({ force: true });

    // Esperar que NO redirija al login
    cy.url().should('not.include', '/login');

    // Validar y luego generar el PDF
    cy.get('#email:invalid').then(($input) => {
      const mensaje = $input[0].validationMessage; 

      expect(mensaje).to.contain("Please include an '@' in the email address. 'usuario-invalido' is missing an '@'."
);

      // Llamar la tarea para generar PDF
      cy.task('generarPDFNegative', {
        title: 'Reporte de Validación de Registro',
        testResult: 'Fallido (esperado)',
        validationMessage: mensaje
      });
    });
  });
});
