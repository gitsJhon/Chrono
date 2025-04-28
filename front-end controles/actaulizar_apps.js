const ws = new WebSocket('ws://localhost:8765');

ws.onmessage = function(event) {
  const apps = JSON.parse(event.data);
  const tableBody = document.getElementById('appsTableBody');
  tableBody.innerHTML = '';

  apps.forEach(app => {
    const row = document.createElement('tr');

    const nameCell = document.createElement('td');
    nameCell.textContent = app.name.replace(/\.exe$/i, '');

    const timeCell = document.createElement('td');
    timeCell.textContent = app.time;

    row.appendChild(nameCell);
    row.appendChild(timeCell);

    tableBody.appendChild(row);
  });
};
