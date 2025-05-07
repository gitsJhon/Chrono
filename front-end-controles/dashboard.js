const ws = new WebSocket('ws://localhost:8765');

ws.onmessage = function(event) {
  const apps = JSON.parse(event.data);
  const tableBody = document.getElementById('appsTableBody');
  tableBody.innerHTML = '';

  apps.forEach(app => {
    const row = document.createElement('tr');

    // Nombre de la app
    const nameCell = document.createElement('td');
    nameCell.textContent = app.name.replace(/\.exe$/i, '');

    // Categoría
    const categoryCell = document.createElement('td');
    categoryCell.textContent = app.category;

    // Última apertura formateada
    const timeCell = document.createElement('td');
    const date = new Date(app.start_time * 1000);
    timeCell.textContent = date.toLocaleString(); // puedes usar .toLocaleTimeString() si quieres solo hora

    // Agregar celdas a la fila
    row.appendChild(nameCell);
    row.appendChild(categoryCell);
    row.appendChild(timeCell);

    // Agregar fila a la tabla
    tableBody.appendChild(row);
  });
};
