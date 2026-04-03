# ⚡ MVPS HACKING MODS - ESP32-S3 Firmware Flasher ⚡

## 🎯 Overview

**Mvps Hacking Mods** is a professional web-based firmware flasher designed specifically for LILYGO T-Embed ESP32-S3 devices. This tool provides a complete hacking firmware library with direct USB-OTG device detection, firmware downloads, and one-click flashing capabilities.

## ✨ Features

### 🔌 USB-OTG Device Detection
- **Web Serial API Integration**: Direct browser-to-device communication
- **Real-time Device Status**: Visual indicators for connection status
- **Multi-vendor Support**: Compatible with Espressif, Silicon Labs, and QinHeng chips
- **Automatic Detection**: Scan and identify connected ESP32-S3 devices

### 📚 Premium Firmware Library
The tool includes **12 premium hacking firmware** options:

#### ⭐ Premium Firmware (Highlighted)
1. **Marauder ESP32-S3** - WiFi/Bluetooth pentesting suite
2. **FlipperZero WiFi Dev** - Advanced wireless capabilities
3. **Evil Portal** - Captive portal attack framework
4. **NRF24 Scanner** - 2.4GHz spectrum analyzer
5. **Bluetooth Sniffer** - BLE packet capture tool
6. **GPS Spoofer** - GPS signal generation
7. **BadUSB Payload** - USB HID attack framework
8. **SubGHz Analyzer** - Sub-1GHz frequency analyzer
9. **Network Sniffer Pro** - Advanced packet capture

#### 🔧 Standard Firmware
10. **WiFi Deauther** - WiFi deauthentication tool
11. **RFID Cloner** - RFID tag read/write/clone
12. **IR Transceiver** - Infrared signal capture/replay

### ⚡ Flash Capabilities
- **One-Click Flashing**: Flash firmware directly from the browser
- **Custom Firmware Upload**: Support for .bin files
- **Progress Tracking**: Real-time progress bars and console output
- **Flash Erase**: Complete flash memory wipe functionality
- **Verification**: Automatic firmware verification after flashing

### 🎨 Hacker-Themed Interface
- **Matrix Effect**: Animated Matrix-style background
- **Terminal Commands**: Scrolling hacking commands background
- **Glowing Effects**: Neon green cyberpunk aesthetic
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Console**: Live logging of all operations

## 🚀 Getting Started

### Prerequisites
- **Browser**: Chrome, Edge, or Opera (Web Serial API support required)
- **Device**: LILYGO T-Embed ESP32-S3
- **Connection**: USB-OTG cable
- **Permissions**: USB device access

### Installation

1. **Open the HTML file**:
   ```bash
   # Simply open esp32-flasher.html in your browser
   # Or serve it with a local server:
   python -m http.server 8000
   # Then navigate to: http://localhost:8000/esp32-flasher.html
   ```

2. **No installation required** - It's a standalone HTML file!

## 📖 Usage Guide

### Step 1: Connect Your Device
1. Connect your ESP32-S3 device via USB-OTG cable
2. Click **"Request USB Permission"** button
3. Select your device from the browser popup
4. Click **"Detect Device"** to verify connection

### Step 2: Choose Firmware
You have two options:

#### Option A: Use Premium Firmware Library
1. Browse the firmware list
2. Click **"📥 Download"** to download firmware (optional)
3. Click **"⚡ Flash Now"** to flash directly

#### Option B: Upload Custom Firmware
1. Click **"📁 Select Custom Firmware"**
2. Choose your .bin file
3. Click **"Flash Firmware"**

### Step 3: Flash Process
1. The tool will automatically:
   - Enter bootloader mode
   - Erase flash (if needed)
   - Write firmware
   - Verify installation
   - Reboot device

2. Monitor progress via:
   - Progress bar (visual percentage)
   - Console output (detailed logs)

### Additional Operations

#### Erase Flash
- Click **"Erase Flash"** button
- Confirm the operation
- Wait for completion

#### Clear Console
- Click **"Clear Console"** to reset the log output

## 🔧 Technical Details

### Web Serial API
The tool uses the Web Serial API for direct USB communication:
- **Vendor IDs Supported**:
  - `0x303A` - Espressif Systems
  - `0x10C4` - Silicon Labs
  - `0x1A86` - QinHeng Electronics

### Browser Compatibility
| Browser | Support | Notes |
|---------|---------|-------|
| Chrome | ✅ Yes | Recommended |
| Edge | ✅ Yes | Full support |
| Opera | ✅ Yes | Full support |
| Firefox | ❌ No | Web Serial API not supported |
| Safari | ❌ No | Web Serial API not supported |

### Security
- **HTTPS Required**: For production use, serve over HTTPS
- **User Permissions**: Explicit user consent required for USB access
- **Sandboxed**: Runs entirely in browser sandbox

## 🎨 Interface Features

### Visual Effects
1. **Matrix Background**: Animated falling characters
2. **Terminal Commands**: Scrolling hacking commands
3. **Glowing Text**: Pulsing neon green effects
4. **Hover Animations**: Interactive button and panel effects
5. **Status Indicators**: Pulsing connection status lights

### Color Scheme
- **Primary**: `#00ff00` (Matrix Green)
- **Background**: `#000000` (Black)
- **Accent**: `#ffff00` (Yellow for premium items)
- **Error**: `#ff0000` (Red)
- **Info**: `#00ccff` (Cyan)

## 📋 Firmware Details

### Marauder ESP32-S3
- **Purpose**: WiFi/Bluetooth pentesting
- **Features**: Packet capture, deauth attacks, beacon spam
- **Size**: 1.2 MB
- **Version**: v0.13.5

### FlipperZero WiFi Dev
- **Purpose**: Flipper Zero WiFi devboard
- **Features**: Advanced wireless capabilities
- **Size**: 1.1 MB
- **Version**: v2.8

### Evil Portal
- **Purpose**: Captive portal attacks
- **Features**: Credential harvesting
- **Size**: 980 KB
- **Version**: v3.1

*[Additional firmware details available in the interface]*

## ⚠️ Important Warnings

### Legal Notice
- **Educational Use Only**: This tool is for educational and authorized testing purposes
- **Authorization Required**: Only use on devices you own or have permission to test
- **Legal Compliance**: Ensure compliance with local laws and regulations

### Safety Precautions
- **Power Supply**: Ensure stable power during flashing
- **Connection**: Use quality USB cables
- **Backup**: Backup important data before flashing
- **Warranty**: Flashing may void device warranty
- **Bricking Risk**: Incorrect firmware may brick your device

## 🐛 Troubleshooting

### Device Not Detected
1. Check USB cable connection
2. Try a different USB port
3. Install CH340/CP2102 drivers if needed
4. Click "Request USB Permission" first
5. Ensure device is in bootloader mode

### Flash Failed
1. Verify firmware file is correct (.bin format)
2. Check device compatibility
3. Ensure stable power supply
4. Try erasing flash first
5. Restart browser and try again

### Browser Issues
1. Use Chrome, Edge, or Opera
2. Enable Web Serial API in browser flags
3. Clear browser cache
4. Disable browser extensions
5. Try incognito/private mode

## 🔄 Updates & Maintenance

### Firmware Updates
The firmware library is regularly updated with:
- Latest security patches
- New features and tools
- Bug fixes and improvements
- Community contributions

### Adding Custom Firmware
To add your own firmware to the library:
1. Edit the `firmwareDatabase` array in the HTML
2. Add firmware details (name, description, version, URL)
3. Set `premium: true` for highlighted items
4. Save and reload the page

## 📱 Mobile Support

### Android
- **Chrome Mobile**: Full support with USB-OTG adapter
- **Permissions**: Grant USB access when prompted
- **Connection**: Use USB-OTG cable

### iOS
- **Limited Support**: Web Serial API not available on iOS
- **Alternative**: Use desktop browser

## 🛠️ Development

### File Structure
```
esp32-flasher.html
├── HTML Structure
├── CSS Styling (embedded)
│   ├── Matrix effects
│   ├── Terminal animations
│   └── Responsive design
└── JavaScript (embedded)
    ├── Matrix canvas animation
    ├── USB Serial API integration
    ├── Firmware database
    └── Flash operations
```

### Customization
You can customize:
- **Colors**: Modify CSS color variables
- **Firmware List**: Edit `firmwareDatabase` array
- **Commands**: Update `commands` array for terminal background
- **Animations**: Adjust CSS keyframes and timing

## 📞 Support

### Resources
- **ESP32 Documentation**: https://docs.espressif.com/
- **Web Serial API**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API
- **LILYGO GitHub**: https://github.com/Xinyuan-LilyGO

### Community
- Share your custom firmware
- Report bugs and issues
- Contribute improvements
- Help other users

## 📄 License

This tool is provided "as-is" for educational purposes. Use at your own risk.

## 🎯 Credits

- **Interface Design**: Mvps Hacking Mods
- **Matrix Effect**: Classic Matrix animation
- **Firmware Sources**: Various open-source projects
- **ESP32 Support**: Espressif Systems

---

## 🚀 Quick Start Commands

```bash
# Serve the file locally
python -m http.server 8000

# Or with Node.js
npx http-server -p 8000

# Or with PHP
php -S localhost:8000
```

Then open: `http://localhost:8000/esp32-flasher.html`

---

**⚡ Happy Hacking! ⚡**

*Remember: With great power comes great responsibility. Use ethically and legally.*
