/// <reference types="cypress" />

describe('Registrar y editar comida desde el frontend', () => {
  it('Editar Comida - Caso Exito', () => {
    // 1. Ir a la página de login
    cy.visit('http://localhost:5173');

    // 2. Completar login
    cy.get('input[type="email"]').type('danielfelipe@gmail.com');
    cy.get('input[type="password"]').type('Millonarios2025*');
    cy.contains('Ingresar').click();

    // 3. Esperar a que aparezca el home tras login
    cy.contains('Registrar cuidado').should('be.visible');

    // Crear Usuario
    cy.contains('Pacientes').click();
    cy.contains('Crear Paciente').click();

    cy.get('input[placeholder="Nombre"]').type('Juan');
    cy.get('input[placeholder="Apellido"]').type('Pérez');
    cy.get('#birth_date').type('1955-10-21');
    cy.get('input[placeholder="Documento"]').type('52660903');
    cy.contains('Crear Paciente').click();

    // Seleccionar Paciente
    cy.contains('Pacientes').click();
    cy.contains('Elegir').click();
    cy.get('section').contains('Cerrar').should('be.visible').click();
    cy.get('img[alt="Logo aplicacion"]').click();

    // 4. Click en "Registrar cuidado"
    cy.contains('Registrar cuidado').click();

    // 5. Seleccionar "Alimentación"
    cy.contains('Alimentación').click();

    // 6. Llenar el formulario de alimentación
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const dd = String(now.getDate()).padStart(2, '0');
    const hh = String(now.getHours()).padStart(2, '0');
    const min = String(now.getMinutes()).padStart(2, '0');
    const fechaHora = `${yyyy}-${mm}-${dd}T${hh}:${min}`;
    cy.get('input[type="datetime-local"]').invoke('val', fechaHora).trigger('input');

    // Comida del día (selección)
    cy.get('select').eq(0).select(1);

    // Descripción del alimento consumido
    cy.get('input[placeholder*="Descripción alimento"]').type('Arroz y pollo');

    // Hidratación (selección)
    cy.get('select').eq(1).select(1);

    // Observaciones
    cy.get('textarea[placeholder*="Observaciones"]').type('Sin observaciones');

    // 7. Click en "Enviar"
    cy.get('button').contains(/^enviar$/i).click();

    // 8. Ir a "Ver registros"
    cy.contains('Ver registros').click();

    // 9. Buscar el registro recién creado (por descripción)
    cy.contains('Ensalada y pasta').should('not.exist'); // Asegura que no hay registros previos
    cy.contains('Editar').click();

    // 10. Editar todos los campos menos la fecha
    // Cambiar comida del día
    cy.get('select').eq(0).select(2); // Cambia la opción de comida del día

    // Cambiar descripción alimento
    cy.get('input[placeholder*="Descripción alimento"]').clear().type('Ensalada y pasta');

    // Cambiar hidratación
    cy.get('select').eq(1).select(2); // Cambia la opción de hidratación

    // Cambiar observaciones
    cy.get('textarea[placeholder*="Observaciones"]').clear().type('Agregar aderezo');

    // 11. Click en "Enviar" para guardar cambios
    cy.get('button').contains(/^enviar$/i).click();

    // 12. (Opcional) Validar que los cambios se reflejen en la lista
    cy.contains('Ensalada y pasta').should('exist');
    cy.contains('Agregar aderezo').should('exist');
  });
});

/// <reference types="cypress" />

describe('Registrar comida - casos no ideales (errores)', () => {
  it('Editar Comida - Casos de Error', () => {
    // 1. Ir a la página de login
    cy.visit('http://localhost:5173');

    // 2. Login
    cy.get('input[type="email"]').type('danielfelipe@gmail.com');
    cy.get('input[type="password"]').type('Millonarios2025*');
    cy.contains('Ingresar').click();

    // 3. Esperar home
    cy.contains('Registrar cuidado').should('be.visible');

    // Crear Usuario
    cy.contains('Pacientes').click();
    cy.contains('Crear Paciente').click();
    cy.get('input[placeholder="Nombre"]').type('Juan');
    cy.get('input[placeholder="Apellido"]').type('Pérez');
    cy.get('#birth_date').type('1955-10-21');
    cy.get('input[placeholder="Documento"]').type('52660903');
    cy.contains('Crear Paciente').click();

    // Seleccionar Paciente
    cy.contains('Pacientes').click();
    cy.contains('Elegir').click();
    cy.get('section').contains('Cerrar').should('be.visible').click();
    cy.get('img[alt="Logo aplicacion"]').click();

    // 4. Click en "Registrar cuidado"
    cy.contains('Registrar cuidado').click();

    // 5. Seleccionar "Alimentación"
    cy.contains('Alimentación').click();

    // 6. Omitir los campos obligatorios (no llenar nada) y dar click en "Enviar"
    cy.get('button').contains(/^enviar$/i).click();

    // 7. Verificar mensajes de error en los campos requeridos
    cy.contains('La fecha y hora son obligatorios').should('be.visible');
    cy.contains('Ingresar el tipo de comida es obligatorio.').should('be.visible');
    cy.contains('Ingresar la descripción del alimento es obligatorio').should('be.visible');
    cy.contains('Ingresar la hidratación es obligatorio').should('be.visible');

    // 8. (Opcional) Completar solo algunos campos y volver a intentar para ver validaciones parciales
    cy.get('input[type="datetime-local"]').invoke('val', '2025-07-20T08:30').trigger('input');
    cy.get('button').contains(/^enviar$/i).click();
    cy.contains('Ingresar el tipo de comida es obligatorio.').should('be.visible');
    cy.contains('Ingresar la descripción del alimento es obligatorio').should('be.visible');
    cy.contains('Ingresar la hidratación es obligatorio').should('be.visible');

    // 9. (Opcional) Probar error en edición: dejar descripción vacía y guardar
    // Ir a "Ver registros" y editar el registro recién creado
    cy.get('img[alt="Logo aplicacion"]').click();
    cy.contains('Ver registros').click();
    cy.contains('Editar').click();

    // 10. Borrar descripción y tratar de guardar
    cy.get('input[placeholder*="Descripción alimento"]').clear();
    cy.get('button').contains(/^enviar$/i).click();
    cy.contains('Ingresar la descripción del alimento es obligatorio').should('be.visible');
  });
});