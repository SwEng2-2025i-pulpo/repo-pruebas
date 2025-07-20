/// <reference types="cypress" />

describe('Registrar Comida - Caso Exito', () => {
  it('Registrar Comida - Caso Exito', () => {
    // 1. Ir a la página de login
    cy.visit('http://localhost:5173'); // Cambia el puerto si tu frontend usa otro

    // 2. Completar login
    cy.get('input[type="email"]').type('danielfelipe@gmail.com'); // Cambia por usuario válido
    cy.get('input[type="password"]').type('Millonarios2025*'); // Cambia por contraseña válida
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
    // Fecha y hora (usa el formato requerido por tu input)
    // Si el input es type="datetime-local", fuerza el valor:
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const dd = String(now.getDate()).padStart(2, '0');
    const hh = String(now.getHours()).padStart(2, '0');
    const min = String(now.getMinutes()).padStart(2, '0');
    const fechaHora = `${yyyy}-${mm}-${dd}T${hh}:${min}`;
    cy.get('input[type="datetime-local"]').invoke('val', fechaHora).trigger('input');

    // Comida del día (selección)
    cy.get('select').eq(0).select(1); // Selecciona la primera opción distinta a "Selecciona una comida"

    // Descripción del alimento consumido
    cy.get('input[placeholder*="Descripción alimento"]').type('Arroz y pollo');

    // Hidratación (selección)
    cy.get('select').eq(1).select(1); // Selecciona la primera opción distinta a "Selecciona tipo de hidratación"

    // Observaciones
    cy.get('textarea[placeholder*="Observaciones"]').type('Sin observaciones');

    // 7. Click en "Enviar"
    cy.get('button').contains(/^enviar$/i).click();

    // Opcional: puedes agregar screenshots al final
    // cy.screenshot();
  });
});

/// <reference types="cypress" />

describe('Registrar Comida - Casos de Error', () => {
  it('Registrar Comida - Casos de Error', () => {
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

    // 6. NO llenar ningún campo, intentar enviar el formulario vacío
    cy.get('button').contains(/^enviar$/i).click();

    // 7. Verificar mensajes de error en los campos requeridos (ajusta los textos según tu app)
    cy.contains(/La fecha y hora son obligatorios/i).should('be.visible');
    cy.contains(/Ingresar el tipo de comida es obligatorio/i).should('be.visible');
    cy.contains(/Ingresar la descripción del alimento es obligatorio/i).should('be.visible');
    cy.contains(/Ingresar la hidratación es obligatorio/i).should('be.visible');

    // 8. (Opcional) Llenar solo un campo y verificar validaciones parciales
    cy.get('input[type="datetime-local"]').invoke('val', '2025-07-20T08:30').trigger('input');
    cy.get('button').contains(/^enviar$/i).click();
    cy.contains(/Ingresar el tipo de comida es obligatorio/i).should('be.visible');
    cy.contains(/Ingresar la descripción del alimento es obligatorio/i).should('be.visible');
    cy.contains(/Ingresar la hidratación es obligatorio/i).should('be.visible');
  });
});