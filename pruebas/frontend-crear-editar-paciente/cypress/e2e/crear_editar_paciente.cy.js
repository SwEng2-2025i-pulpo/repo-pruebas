describe('Crear y Editar Paciente', () => {
  beforeEach(() => {
    cy.login();
    cy.contains('Pacientes').click();
  });

  it('Flujo correcto de creación de paciente', () => {
    cy.contains('Crear Paciente').click();

    cy.get('input[placeholder="Nombre"]').type('Juan');
    cy.get('input[placeholder="Apellido"]').type('Pérez');
    cy.get('#birth_date').type('1955-10-21');
    cy.get('input[placeholder="Documento"]').type('52660903');
    cy.contains('Crear Paciente').click();

    cy.contains('¡Paciente creado exitosamente!').should('be.visible');
  });

  it('Error por campos vacíos', () => {
    cy.contains('Crear Paciente').click();
    cy.contains('Crear Paciente').click(); // Intenta crear sin llenar

    cy.contains('El nombre es obligatorio').should('be.visible');
    cy.contains('El apellido es obligatorio').should('be.visible');
    cy.contains('La fecha de nacimiento es obligatoria').should('be.visible');
    cy.contains('El documento es obligatorio').should('be.visible');
  });

  it('Error por documento vacío', () => {
    cy.contains('Crear Paciente').click();

    cy.get('input[placeholder="Nombre"]').type('Juana');
    cy.get('input[placeholder="Apellido"]').type('Peres');
    cy.get('#birth_date').type('2000-09-21');
    cy.get('input[placeholder="Documento"]').clear(); // deja vacío el documento
    cy.contains('Crear Paciente').click();

    cy.contains('El documento es obligatorio').should('be.visible');
  });

  it('Flujo de edición de paciente', () => {
    // Busca un paciente existente y edita
    cy.contains('Editar').first().click();

    cy.get('input[placeholder="Nombre"]').clear().type('Alejo Actualizado');
    cy.get('input[placeholder="Apellido"]').clear().type('Ardila');
    cy.get('#birth_date').clear().type('1951-02-19');
    cy.get('input[placeholder="Documento"]').clear().type('512345678');
    cy.contains('Actualizar Paciente').click();

    cy.contains('Paciente actualizado exitosamente').should('be.visible');
  });

  it('Error al editar paciente con datos inválidos', () => {

    cy.contains('Editar').first().click();

    cy.get('input[placeholder="Nombre"]').clear();
    cy.contains('Actualizar Paciente').click();

    cy.contains('El nombre es obligatorio').should('be.visible');
  });
});