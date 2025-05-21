const ws = new WebSocket('ws://localhost:8765');

const toggle = document.getElementById('toggleView');
const appsView = document.getElementById('appsView');
const graficoView = document.getElementById('graficoView');

toggle.addEventListener('change', () => {
  if (toggle.checked) {
    appsView.classList.remove('active');
    graficoView.classList.add('active');
  } else {
    graficoView.classList.remove('active');
    appsView.classList.add('active');
  }
});

// Crear grafico vacío
let grafico = null;
const ctx = document.getElementById('graficoConsumo').getContext('2d');

function crearGrafico(data) {
  if (grafico) {
    grafico.destroy();
  }
  grafico = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [
        {
          label: 'GPU (%)',
          data: data.gpu,
          backgroundColor: '#4caf50'
        },
        {
          label: 'CPU (%)',
          data: data.cpu,
          backgroundColor: '#2196f3'
        },
        {
          label: 'RAM (MB)',
          data: data.memoria,
          backgroundColor: '#ff9800'
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

ws.onmessage = function(event) {
  const paquete = JSON.parse(event.data);
  const apps = paquete.apps_tiempo;
  const consumo = paquete.apps_consumo;

  // Actualizar tabla
  const tableBody = document.getElementById('appsTableBody');
  tableBody.innerHTML = '';
  apps.forEach(app => {
    const row = document.createElement('tr');
    const nameCell = document.createElement('td');
    nameCell.textContent = app.name.replace(/\.exe$/i, '');
    const categoryCell = document.createElement('td');
    categoryCell.textContent = app.category;
    const timeCell = document.createElement('td');
    const date = new Date(app.start_time * 1000);
    timeCell.textContent = date.toLocaleString();
    row.appendChild(nameCell);
    row.appendChild(categoryCell);
    row.appendChild(timeCell);
    tableBody.appendChild(row);
  });

  // Actualizar gráfico
  if (consumo && consumo.length > 0) {
    const labels = consumo.map(app => app.name.replace(/\.exe$/i, ''));
    const cpuData = consumo.map(app => app.cpu);
    const memData = consumo.map(app => app.ram);
    const gpuData = consumo.map(app => app.gpu);

    crearGrafico({
      labels: labels,
      cpu: cpuData,
      memoria: memData,
      gpu: gpuData
    });
  } else {
    console.warn("Sin datos de consumo recibidos.");
  }
};
