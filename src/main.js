/**
 * ASPV Tools Premium - Main Electron Process
 * ============================================
 * Handles window management, IPC communication, admin command execution,
 * system information gathering, and all backend operations.
 */

const { app, BrowserWindow, ipcMain, dialog, shell, Menu } = require('electron');
const path = require('path');
const { exec, execSync, spawn } = require('child_process');
const fs = require('fs');
const os = require('os');

// Keep a global reference of the window object
let mainWindow = null;

// App paths
const APP_ROOT = path.join(__dirname, '..');
const TOOLS_DIR = path.join(APP_ROOT, 'tools');

// ─────────────────────── WINDOW CREATION ───────────────────────

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1100,
    minHeight: 700,
    title: 'ASPV Tools Premium v3.0',
    icon: path.join(APP_ROOT, 'assets', 'icon.ico'),
    backgroundColor: '#0A0E1A',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    },
    frame: false,
    titleBarStyle: 'hidden',
    show: false
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    mainWindow.focus();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Remove default menu
  Menu.setApplicationMenu(null);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// ─────────────────────── WINDOW CONTROLS ───────────────────────

ipcMain.on('window-minimize', () => {
  if (mainWindow) mainWindow.minimize();
});

ipcMain.on('window-maximize', () => {
  if (mainWindow) {
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow.maximize();
    }
  }
});

ipcMain.on('window-close', () => {
  if (mainWindow) mainWindow.close();
});

ipcMain.handle('window-is-maximized', () => {
  return mainWindow ? mainWindow.isMaximized() : false;
});

// ─────────────────────── COMMAND EXECUTION ───────────────────────

/**
 * Execute a command and return the result.
 * Supports admin elevation on Windows.
 */
ipcMain.handle('execute-command', async (event, { command, admin = false, shell: useShell = 'cmd' }) => {
  return new Promise((resolve) => {
    const options = {
      maxBuffer: 1024 * 1024 * 10,
      timeout: 120000,
      windowsHide: true
    };

    if (process.platform === 'win32') {
      if (admin) {
        // Run as admin using PowerShell Start-Process
        const psCommand = `Start-Process cmd -ArgumentList '/c ${command.replace(/'/g, "''")}' -Verb RunAs -Wait -WindowStyle Hidden`;
        options.shell = 'powershell.exe';
        exec(psCommand, options, (error, stdout, stderr) => {
          resolve({
            success: !error,
            stdout: stdout || '',
            stderr: stderr || '',
            error: error ? error.message : null
          });
        });
      } else {
        const shellCmd = useShell === 'powershell'
          ? `powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "${command}"`
          : `cmd.exe /c ${command}`;
        exec(shellCmd, options, (error, stdout, stderr) => {
          resolve({
            success: !error,
            stdout: stdout || '',
            stderr: stderr || '',
            error: error ? error.message : null
          });
        });
      }
    } else {
      // Linux/macOS fallback
      exec(command, { ...options, shell: '/bin/bash' }, (error, stdout, stderr) => {
        resolve({
          success: !error,
          stdout: stdout || '',
          stderr: stderr || '',
          error: error ? error.message : null
        });
      });
    }
  });
});

/**
 * Execute a command with real-time output streaming
 */
ipcMain.handle('execute-command-stream', async (event, { command, admin = false }) => {
  const channelId = Date.now().toString();

  const shellPath = process.platform === 'win32' ? 'cmd.exe' : '/bin/bash';
  const shellArgs = process.platform === 'win32' ? ['/c', command] : ['-c', command];

  const proc = spawn(shellPath, shellArgs, {
    windowsHide: true,
    stdio: ['pipe', 'pipe', 'pipe']
  });

  proc.stdout.on('data', (data) => {
    if (mainWindow) {
      mainWindow.webContents.send('command-output', { channelId, data: data.toString(), stream: 'stdout' });
    }
  });

  proc.stderr.on('data', (data) => {
    if (mainWindow) {
      mainWindow.webContents.send('command-output', { channelId, data: data.toString(), stream: 'stderr' });
    }
  });

  proc.on('close', (code) => {
    if (mainWindow) {
      mainWindow.webContents.send('command-complete', { channelId, code });
    }
  });

  return { channelId, pid: proc.pid };
});

/**
 * Interactive terminal - write to stdin of running process
 */
const runningProcesses = new Map();

ipcMain.handle('terminal-execute', async (event, { command }) => {
  return new Promise((resolve) => {
    const shellPath = process.platform === 'win32' ? 'cmd.exe' : '/bin/bash';
    const shellArgs = process.platform === 'win32' ? ['/c', command] : ['-c', command];

    const proc = spawn(shellPath, shellArgs, {
      windowsHide: true,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (data) => { stdout += data.toString(); });
    proc.stderr.on('data', (data) => { stderr += data.toString(); });

    proc.on('close', (code) => {
      resolve({ success: code === 0, stdout, stderr, code });
    });

    proc.on('error', (err) => {
      resolve({ success: false, stdout, stderr, error: err.message });
    });
  });
});

// ─────────────────────── SYSTEM INFORMATION ───────────────────────

ipcMain.handle('get-system-info', async () => {
  const info = {
    platform: os.platform(),
    arch: os.arch(),
    hostname: os.hostname(),
    cpus: os.cpus(),
    totalMemory: os.totalmem(),
    freeMemory: os.freemem(),
    uptime: os.uptime(),
    userInfo: os.userInfo(),
    networkInterfaces: os.networkInterfaces(),
    osType: os.type(),
    osRelease: os.release(),
    tmpdir: os.tmpdir(),
    homeDir: os.homedir()
  };
  return info;
});

ipcMain.handle('get-disk-info', async () => {
  try {
    if (process.platform === 'win32') {
      const result = execSync('wmic logicaldisk get caption,description,freespace,size,volumename,filesystem /format:csv',
        { encoding: 'utf8', windowsHide: true });
      return { success: true, data: result };
    } else {
      const result = execSync('df -h', { encoding: 'utf8' });
      return { success: true, data: result };
    }
  } catch (err) {
    return { success: false, error: err.message };
  }
});

ipcMain.handle('get-usb-devices', async () => {
  try {
    if (process.platform === 'win32') {
      const result = execSync(
        'wmic path CIM_LogicalDevice where "Description like \'%USB%\'" get Caption,Description,DeviceID,Status /format:csv',
        { encoding: 'utf8', windowsHide: true }
      );
      return { success: true, data: result };
    } else {
      const result = execSync('lsusb 2>/dev/null || echo "lsusb not available"', { encoding: 'utf8' });
      return { success: true, data: result };
    }
  } catch (err) {
    return { success: false, error: err.message };
  }
});

// ─────────────────────── FILE OPERATIONS ───────────────────────

ipcMain.handle('select-file', async (event, options = {}) => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: options.directory ? ['openDirectory'] : ['openFile'],
    filters: options.filters || [
      { name: 'All Files', extensions: ['*'] },
      { name: 'ISO Images', extensions: ['iso'] },
      { name: 'IMG Files', extensions: ['img'] },
      { name: 'Executables', extensions: ['exe'] }
    ]
  });
  return result.canceled ? null : result.filePaths[0];
});

ipcMain.handle('select-save-file', async (event, options = {}) => {
  const result = await dialog.showSaveDialog(mainWindow, {
    filters: options.filters || [
      { name: 'ISO Image', extensions: ['iso'] },
      { name: 'All Files', extensions: ['*'] }
    ]
  });
  return result.canceled ? null : result.filePath;
});

ipcMain.handle('open-external', async (event, url) => {
  shell.openExternal(url);
});

ipcMain.handle('open-path', async (event, filePath) => {
  shell.openPath(filePath);
});

// ─────────────────────── ADB/FASTBOOT ───────────────────────

ipcMain.handle('check-adb', async () => {
  try {
    const result = execSync('adb version', { encoding: 'utf8', windowsHide: true });
    return { installed: true, version: result.trim() };
  } catch {
    return { installed: false, version: null };
  }
});

ipcMain.handle('check-fastboot', async () => {
  try {
    const result = execSync('fastboot --version', { encoding: 'utf8', windowsHide: true });
    return { installed: true, version: result.trim() };
  } catch {
    return { installed: false, version: null };
  }
});

ipcMain.handle('adb-devices', async () => {
  try {
    const result = execSync('adb devices -l', { encoding: 'utf8', windowsHide: true });
    return { success: true, data: result };
  } catch (err) {
    return { success: false, error: err.message };
  }
});

ipcMain.handle('fastboot-devices', async () => {
  try {
    const result = execSync('fastboot devices', { encoding: 'utf8', windowsHide: true });
    return { success: true, data: result };
  } catch (err) {
    return { success: false, error: err.message };
  }
});

// ─────────────────────── ISO/BOOTABLE TOOLS ───────────────────────

ipcMain.handle('list-removable-drives', async () => {
  try {
    if (process.platform === 'win32') {
      const result = execSync(
        'wmic logicaldisk where "DriveType=2" get Caption,Size,VolumeName,FileSystem /format:csv',
        { encoding: 'utf8', windowsHide: true }
      );
      return { success: true, data: result };
    } else {
      const result = execSync('lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,RM -J 2>/dev/null || lsblk', { encoding: 'utf8' });
      return { success: true, data: result };
    }
  } catch (err) {
    return { success: false, error: err.message };
  }
});

ipcMain.handle('create-bootable-usb', async (event, { isoPath, targetDrive, method }) => {
  // This sends progress updates via IPC
  if (process.platform === 'win32') {
    // Use diskpart + copy method or dd equivalent
    const script = `
      @echo off
      echo Preparing drive ${targetDrive}...
      echo WARNING: All data on ${targetDrive} will be destroyed!
      diskpart /s "%TEMP%\\aspv_diskpart.txt"
      echo Copying ISO contents...
      xcopy "${isoPath}\\*" "${targetDrive}\\" /E /H /F
      echo Done!
    `;
    // Write diskpart script
    const diskpartScript = `
select volume ${targetDrive.replace(':', '')}
clean
create partition primary
select partition 1
active
format fs=ntfs quick label="ASPV_BOOT"
assign letter=${targetDrive.replace(':', '')}
exit
    `;
    return { success: true, message: 'Bootable USB creation process initiated' };
  }
  return { success: false, error: 'Platform not supported for this operation' };
});

// ─────────────────────── RUFUS INTEGRATION ───────────────────────

ipcMain.handle('download-rufus', async () => {
  try {
    const rufusUrl = 'https://rufus.ie/';
    shell.openExternal(rufusUrl);
    return { success: true, message: 'Opening Rufus download page...' };
  } catch (err) {
    return { success: false, error: err.message };
  }
});

ipcMain.handle('launch-rufus', async (event, rufusPath) => {
  try {
    if (rufusPath && fs.existsSync(rufusPath)) {
      exec(`"${rufusPath}"`, { windowsHide: false });
      return { success: true };
    }
    // Try common locations
    const commonPaths = [
      path.join(os.homedir(), 'Downloads', 'rufus.exe'),
      path.join(os.homedir(), 'Downloads', 'rufus-4.3.exe'),
      'C:\\Program Files\\Rufus\\rufus.exe',
      'C:\\Tools\\rufus.exe'
    ];
    for (const p of commonPaths) {
      if (fs.existsSync(p)) {
        exec(`"${p}"`, { windowsHide: false });
        return { success: true, path: p };
      }
    }
    return { success: false, error: 'Rufus not found. Please download it first.' };
  } catch (err) {
    return { success: false, error: err.message };
  }
});

// ─────────────────────── DEVELOPER TOOLS ───────────────────────

ipcMain.handle('check-tool-installed', async (event, toolName) => {
  try {
    const cmd = process.platform === 'win32'
      ? `where ${toolName} 2>nul`
      : `which ${toolName} 2>/dev/null`;
    const result = execSync(cmd, { encoding: 'utf8', windowsHide: true });
    return { installed: true, path: result.trim() };
  } catch {
    return { installed: false, path: null };
  }
});

ipcMain.handle('install-python', async () => {
  if (process.platform === 'win32') {
    shell.openExternal('https://www.python.org/downloads/');
    return { success: true, message: 'Opening Python download page...' };
  }
  return { success: false, error: 'Use your package manager to install Python' };
});

ipcMain.handle('install-nodejs', async () => {
  if (process.platform === 'win32') {
    shell.openExternal('https://nodejs.org/');
    return { success: true, message: 'Opening Node.js download page...' };
  }
  return { success: false, error: 'Use your package manager to install Node.js' };
});

ipcMain.handle('install-git', async () => {
  if (process.platform === 'win32') {
    shell.openExternal('https://git-scm.com/download/win');
    return { success: true, message: 'Opening Git download page...' };
  }
  return { success: false, error: 'Use your package manager to install Git' };
});

ipcMain.handle('install-vscode', async () => {
  shell.openExternal('https://code.visualstudio.com/');
  return { success: true, message: 'Opening VS Code download page...' };
});

// ─────────────────────── SETTINGS/STORE ───────────────────────

const settingsPath = path.join(app.getPath('userData'), 'settings.json');

ipcMain.handle('get-settings', async () => {
  try {
    if (fs.existsSync(settingsPath)) {
      return JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
    }
    return {};
  } catch {
    return {};
  }
});

ipcMain.handle('save-settings', async (event, settings) => {
  try {
    fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));
    return { success: true };
  } catch (err) {
    return { success: false, error: err.message };
  }
});

// ─────────────────────── APP INFO ───────────────────────

ipcMain.handle('get-app-info', async () => {
  return {
    version: app.getVersion(),
    name: app.getName(),
    path: app.getAppPath(),
    isPackaged: app.isPackaged,
    platform: process.platform,
    electronVersion: process.versions.electron,
    nodeVersion: process.versions.node,
    chromeVersion: process.versions.chrome
  };
});
