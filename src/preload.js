/**
 * ASPV Tools Premium - Preload Script
 * =====================================
 * Secure bridge between renderer and main process.
 * Exposes only necessary APIs via contextBridge.
 */

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('aspv', {
  // ─── Window Controls ───
  minimize: () => ipcRenderer.send('window-minimize'),
  maximize: () => ipcRenderer.send('window-maximize'),
  close: () => ipcRenderer.send('window-close'),
  isMaximized: () => ipcRenderer.invoke('window-is-maximized'),

  // ─── Command Execution ───
  executeCommand: (opts) => ipcRenderer.invoke('execute-command', opts),
  executeCommandStream: (opts) => ipcRenderer.invoke('execute-command-stream', opts),
  terminalExecute: (opts) => ipcRenderer.invoke('terminal-execute', opts),

  // ─── Event Listeners ───
  onCommandOutput: (callback) => {
    ipcRenderer.on('command-output', (event, data) => callback(data));
  },
  onCommandComplete: (callback) => {
    ipcRenderer.on('command-complete', (event, data) => callback(data));
  },
  removeCommandListeners: () => {
    ipcRenderer.removeAllListeners('command-output');
    ipcRenderer.removeAllListeners('command-complete');
  },

  // ─── System Information ───
  getSystemInfo: () => ipcRenderer.invoke('get-system-info'),
  getDiskInfo: () => ipcRenderer.invoke('get-disk-info'),
  getUsbDevices: () => ipcRenderer.invoke('get-usb-devices'),

  // ─── File Operations ───
  selectFile: (opts) => ipcRenderer.invoke('select-file', opts),
  selectSaveFile: (opts) => ipcRenderer.invoke('select-save-file', opts),
  openExternal: (url) => ipcRenderer.invoke('open-external', url),
  openPath: (p) => ipcRenderer.invoke('open-path', p),

  // ─── ADB/Fastboot ───
  checkAdb: () => ipcRenderer.invoke('check-adb'),
  checkFastboot: () => ipcRenderer.invoke('check-fastboot'),
  adbDevices: () => ipcRenderer.invoke('adb-devices'),
  fastbootDevices: () => ipcRenderer.invoke('fastboot-devices'),

  // ─── ISO/Bootable ───
  listRemovableDrives: () => ipcRenderer.invoke('list-removable-drives'),
  createBootableUsb: (opts) => ipcRenderer.invoke('create-bootable-usb', opts),
  downloadRufus: () => ipcRenderer.invoke('download-rufus'),
  launchRufus: (p) => ipcRenderer.invoke('launch-rufus', p),

  // ─── Developer Tools ───
  checkToolInstalled: (name) => ipcRenderer.invoke('check-tool-installed', name),
  installPython: () => ipcRenderer.invoke('install-python'),
  installNodejs: () => ipcRenderer.invoke('install-nodejs'),
  installGit: () => ipcRenderer.invoke('install-git'),
  installVscode: () => ipcRenderer.invoke('install-vscode'),

  // ─── Settings ───
  getSettings: () => ipcRenderer.invoke('get-settings'),
  saveSettings: (s) => ipcRenderer.invoke('save-settings', s),

  // ─── App Info ───
  getAppInfo: () => ipcRenderer.invoke('get-app-info')
});
