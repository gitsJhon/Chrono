const { app, BrowserWindow, Menu } = require('electron');

function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
  });
  Menu.setApplicationMenu(null); // Hide the menu bar
  win.loadFile('index.html');
  win.setTitle(''); // Set the title of the window
}

app.whenReady().then(createWindow);
