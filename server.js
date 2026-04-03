const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.bin': 'application/octet-stream'
};

const server = http.createServer((req, res) => {
    let filePath = req.url === '/' ? '/mvps-hacking-mods.html' : req.url;
    filePath = path.join(__dirname, filePath);

    const ext = path.extname(filePath);
    const contentType = mimeTypes[ext] || 'application/octet-stream';

    fs.readFile(filePath, (err, content) => {
        if (err) {
            if (err.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end(`
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>404 - Not Found</title>
                        <style>
                            body { background: #0a0a0a; color: #00ff00; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                            .error { text-align: center; border: 1px solid #00ff00; padding: 40px; }
                            h1 { text-shadow: 0 0 10px #00ff00; }
                            a { color: #00ff00; }
                        </style>
                    </head>
                    <body>
                        <div class="error">
                            <h1>ERROR 404</h1>
                            <p>File not found: ${req.url}</p>
                            <a href="/">Return to Home</a>
                        </div>
                    </body>
                    </html>
                `);
            } else {
                res.writeHead(500);
                res.end('Server Error');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content);
        }
    });
});

server.listen(PORT, () => {
    console.log(`
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   Mvps Hacking mods - Server Running                  ║
    ║                                                       ║
    ║   Local:   http://localhost:${PORT}                     ║
    ║                                                       ║
    ║   Web Serial API required for OTG support             ║
    ║   Use Chrome or Edge browser                           ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    `);
});
