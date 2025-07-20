const fs = require('fs-extra');
const path = require('path');
const PDFDocument = require('pdfkit');
const { createCanvas } = require('canvas');

const generatePDF = async ({ title, testResult, validationMessage }) => {
  const doc = new PDFDocument({ margin: 50 });
  const outputPath = path.join(__dirname, '../cypress/reports', 'reportErrors.pdf');
  fs.ensureDirSync(path.dirname(outputPath));
  doc.pipe(fs.createWriteStream(outputPath));

  // Logo UNAL
  const logoPath = path.join(__dirname, '../../..', 'logo_unal.png');
  if (fs.existsSync(logoPath)) {
    doc.image(logoPath, doc.page.width - 120, 40, { width: 70 });
  }

  // Fecha y hora
  const now = new Date();
  const horaTest = now.toLocaleString('es-CO', {
    dateStyle: 'short',
    timeStyle: 'short',
  });
  doc.fontSize(10).text(`Fecha y hora del test: ${horaTest}`, 50, 50);

  // Título
  doc.moveDown(2);
  doc.fontSize(20).text(title, { align: 'center' });
  doc.moveDown(2);

  // Tabla con fila especial para el mensaje del navegador
  const startX = 60;
  let currentY = doc.y;

  const tableData = [
    ['Campo', 'Valor'],
    ['Resultado', testResult],
    ['Mensaje del Navegador', validationMessage],
  ];

  const cellWidth = [200, 300];

  tableData.forEach((row, i) => {
    // Ajustar altura de fila según contenido
    const isMessageRow = row[0] === 'Mensaje del Navegador';
    const cellHeight = isMessageRow ? 40 : 25;

    // Fondo para encabezado o filas
    const fillColor = i === 0 ? '#dcdcdc' : '#f9f9f9';
    doc.rect(startX, currentY, cellWidth[0], cellHeight).fill(fillColor);
    doc.rect(startX + cellWidth[0], currentY, cellWidth[1], cellHeight).fill(fillColor);

    // Texto
    doc.fillColor('black')
      .fontSize(12)
      .text(row[0], startX + 10, currentY + 7, {
        width: cellWidth[0] - 20,
        align: 'left',
      })
      .text(row[1], startX + cellWidth[0] + 10, currentY + 7, {
        width: cellWidth[1] - 20,
        align: 'left',
      });

    currentY += cellHeight;
  });

  doc.moveDown(3);

  // Gráfico centrado
  const canvas = createCanvas(500, 300);
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = 100;

  ctx.beginPath();
  ctx.moveTo(centerX, centerY);
  ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
  ctx.closePath();
  ctx.fillStyle = '#e74c3c';
  ctx.fill();

  // Leyenda
  ctx.fillStyle = '#e74c3c';
  ctx.fillRect(360, 80, 15, 15);
  ctx.fillStyle = '#000';
  ctx.font = '14px Arial';
  ctx.fillText('Campos inválidos', 380, 93);

  // Insertar imagen centrada
  const chartImage = canvas.toBuffer('image/png');
  const imgWidth = 400;
  const xOffset = (doc.page.width - imgWidth) / 2;
  doc.image(chartImage, xOffset, doc.y, { width: imgWidth });

  doc.end();
};

module.exports = generatePDF;
