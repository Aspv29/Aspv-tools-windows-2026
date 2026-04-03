const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files
app.use(express.static(path.join(__dirname)));
app.use('/firmware', express.static(path.join(__dirname, 'firmware')));

// Main route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Top rated firmware page
app.get('/top-rated', (req, res) => {
    res.sendFile(path.join(__dirname, 'top-rated.html'));
});

// API endpoint for firmware list
app.get('/api/firmware', (req, res) => {
    res.json({
        status: 'ok',
        message: 'Mvps Hacking Mods - Firmware API',
        count: 15,
        note: 'Firmware binaries must be downloaded from their respective GitHub releases'
    });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`\x1b[32m`);
    console.log(`  ╔══════════════════════════════════════════╗`);
    console.log(`  ║     Mvps Hacking Mods - Server Active    ║`);
    console.log(`  ║     http://localhost:${PORT}               ║`);
    console.log(`  ║     ESP32-S3 Flasher Ready               ║`);
    console.log(`  ╚══════════════════════════════════════════╝`);
    console.log(`\x1b[0m`);
});
