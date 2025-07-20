const fs = require('fs-extra');
const path = require('path');
const PDFDocument = require('pdfkit');
const { createCanvas } = require('canvas');

const generatePDF = async ({ title, email, registro, login, resultado }) => {
  const doc = new PDFDocument({ margin: 50 });
  const outputPath = path.join(__dirname, '../cypress/reports', 'reportCorrect.pdf');
  fs.ensureDirSync(path.dirname(outputPath));
  doc.pipe(fs.createWriteStream(outputPath));

  // Logo
  const logoPath = path.join(__dirname, '../../..', 'logo_unal.png');
  if (fs.existsSync(logoPath)) {
    doc.image(logoPath, doc.page.width - 120, 40, { width: 70 });
  }

  // Fecha y hora
  const ahora = new Date();
  const fecha = ahora.toLocaleString('es-CO', {
    dateStyle: 'short',
    timeStyle: 'short',
  });
  doc.fontSize(10).text(`Fecha y hora del test: ${fecha}`, 50, 50);

  // Título
  doc.moveDown(2);
  doc.fontSize(20).text(title, { align: 'center' });
  doc.moveDown(2);

  // Tabla de datos
  const startX = 60;
  let currentY = doc.y;
  const cellWidth = [200, 300];

  const tableData = [
    ['Campo', 'Valor'],
    ['Correo usado', email],
    ['Registro', registro],
    ['Login', login],
    ['Resultado final', resultado],
  ];

  tableData.forEach((row, i) => {
    const cellHeight = row[0] === 'Resultado final' ? 35 : 25;
    const fill = i === 0 ? '#dcdcdc' : '#f9f9f9';

    doc.rect(startX, currentY, cellWidth[0], cellHeight).fill(fill);
    doc.rect(startX + cellWidth[0], currentY, cellWidth[1], cellHeight).fill(fill);

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

  doc.moveDown(2);

  // 🥧 Gráfico de torta
  const canvas = createCanvas(400, 300);
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const data = [1, 1]; // Ambos exitosos
  const labels = ['Registro', 'Login'];
  const colors = ['#2ecc71', '#3498db'];
  const total = data.reduce((acc, val) => acc + val, 0);

  const centerX = 200;
  const centerY = 150;
  const radius = 100;
  let startAngle = 0;

  data.forEach((value, i) => {
    const sliceAngle = (value / total) * 2 * Math.PI;
    const endAngle = startAngle + sliceAngle;

    // Slice
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, startAngle, endAngle);
    ctx.closePath();
    ctx.fillStyle = colors[i];
    ctx.fill();

    // Label
    const midAngle = startAngle + sliceAngle / 2;
    const labelX = centerX + Math.cos(midAngle) * (radius + 20);
    const labelY = centerY + Math.sin(midAngle) * (radius + 20);
    ctx.fillStyle = '#000';
    ctx.font = '14px Arial';
    ctx.fillText(labels[i], labelX - 20, labelY);

    startAngle = endAngle;
  });

  const imgBuffer = canvas.toBuffer('image/png');
  const imgX = (doc.page.width - 400) / 2;
  doc.image(imgBuffer, imgX, doc.y, { width: 400 });

  doc.end();
};

module.exports = generatePDF;
