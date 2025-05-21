const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

// Carpeta de vistas HTML
app.use(express.static(path.join(__dirname, 'views')));

// Carpeta de scripts
app.use('/js', express.static(path.join(__dirname, 'front-end-controles')));

// Carpeta de estilos
app.use('/css', express.static(path.join(__dirname, 'styles')));

// Servir index si quieres
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'dashboard.HTML'));
});

app.listen(PORT, () => {
  console.log(`Servidor web disponible en http://localhost:${PORT}`);
});
