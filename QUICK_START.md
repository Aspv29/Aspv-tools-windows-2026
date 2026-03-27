# 🚀 ASPV Tools Premium v3.0 - Quick Start Guide

## ⚡ Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
npm install
```

### Step 2: Run the Application
```bash
npm start
```

### Step 3: Build for Distribution
```bash
npm run build
```

---

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `npm start` | Run application in development mode |
| `npm run dev` | Same as start (with dev flag) |
| `npm run build` | Build installer + portable executable |
| `npm run dist` | Build NSIS installer only |
| `npm run pack` | Build portable executable only |
| `npm run build:dir` | Build unpacked (for testing) |

---

## 🎯 Quick Reference

### Project Structure
```
src/
├── main.js       → Main process (backend)
├── preload.js    → Secure bridge
├── renderer.js   → UI logic (frontend)
├── index.html    → HTML structure
└── styles.css    → Styling
```

### Key Files
- `package.json` - Dependencies & build config
- `build.bat` / `build.ps1` - Build scripts
- `README_ELECTRON.md` - Full documentation

---

## 🔧 Development Tips

### Hot Reload
The app doesn't have hot reload by default. Restart with `npm start` after changes.

### Debugging
- Press `Ctrl+Shift+I` to open DevTools
- Check Console for errors
- Use `console.log()` in renderer.js

### Adding New Section
1. Add to `NAVIGATION` array in renderer.js
2. Add to `SECTIONS` object in renderer.js
3. Implement `render()` function

---

## 📦 Building

### Windows
```bash
# Using npm
npm run build

# Using scripts
build.bat          # CMD
.\build.ps1        # PowerShell
```

### Output
- `dist/ASPV-Tools-Premium-Setup-3.0.0.exe` - Installer
- `dist/ASPV-Tools-Premium-3.0.0-portable.exe` - Portable

---

## ⚠️ Requirements

- **Node.js**: 18.0.0 or higher
- **npm**: 8.0.0 or higher
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4 GB minimum
- **Disk**: 500 MB free space

---

## 🐛 Troubleshooting

### Build Fails
```bash
# Clean and reinstall
rm -rf node_modules
npm install
npm run build
```

### App Won't Start
- Check Node.js version: `node --version`
- Reinstall dependencies: `npm install`
- Check for errors in terminal

### Commands Don't Work
- Run as Administrator
- Check Windows version (10/11 required)
- Verify PowerShell is enabled

---

## 📚 Learn More

- **Full Documentation**: `README_ELECTRON.md`
- **Migration Guide**: `MIGRATION_GUIDE.md`
- **Build Complete**: `ELECTRON_BUILD_COMPLETE.md`

---

## 🎉 You're Ready!

Start developing with:
```bash
npm start
```

Build for production with:
```bash
npm run build
```

**Happy coding! 🚀**
