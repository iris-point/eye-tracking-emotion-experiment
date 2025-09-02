/**
 * Standalone server for Emotion Regulation Experiment
 * 情绪调节实验独立服务器
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const PORT = process.argv[2] || 8080;
const HOST = '0.0.0.0';

const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.JPG': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
    console.log(`Request for ${req.url}`);
    
    // Decode URL to handle Chinese characters and spaces
    let filePath = decodeURIComponent(req.url);
    
    // Default to index.html
    if (filePath === '/') {
        filePath = '/index.html';
    }
    
    // Handle paths
    if (filePath.startsWith('/dist/')) {
        // Serve from parent directory for SDK files
        filePath = path.join(__dirname, '..', filePath);
    } else if (filePath.startsWith('/jspsych-plugin/')) {
        // Serve jsPsych plugins from parent
        filePath = path.join(__dirname, '..', filePath);
    } else if (filePath.startsWith('/jspsych-extension/')) {
        // Serve jsPsych extensions from parent
        filePath = path.join(__dirname, '..', filePath);
    } else {
        // Everything else from current directory
        filePath = path.join(__dirname, filePath);
    }
    
    const extname = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes[extname] || 'application/octet-stream';
    
    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end('<h1>404 - 文件未找到 File Not Found</h1>', 'utf-8');
            } else {
                res.writeHead(500);
                res.end(`Server Error: ${error.code}`, 'utf-8');
            }
        } else {
            res.writeHead(200, { 
                'Content-Type': contentType,
                'Access-Control-Allow-Origin': '*'
            });
            res.end(content, 'utf-8');
        }
    });
});

// Get local IP addresses
function getLocalIPs() {
    const interfaces = os.networkInterfaces();
    const addresses = [];
    
    for (const name of Object.keys(interfaces)) {
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal) {
                addresses.push(iface.address);
            }
        }
    }
    
    return addresses;
}

server.listen(PORT, HOST, () => {
    const localIPs = getLocalIPs();
    
    console.log(`
╔════════════════════════════════════════════════════════╗
║  情绪调节实验服务器                                      ║
║  Emotion Regulation Experiment Server                  ║
║                                                        ║
║  服务器运行端口 Server port: ${PORT}                       ║
║                                                        ║
║  本机访问 Local access:                                ║
║  → http://localhost:${PORT}/                               ║
║                                                        ║`);
    
    if (localIPs.length > 0) {
        console.log(`║  网络访问 Network access:                             ║`);
        localIPs.forEach(ip => {
            console.log(`║  → http://${ip}:${PORT}/                              ║`);
        });
        console.log(`║                                                        ║`);
    }
    
    console.log(`║  按 Ctrl+C 停止服务器                                  ║
║  Press Ctrl+C to stop the server                      ║
║                                                        ║
║  确保防火墙允许端口 ${PORT} 访问                           ║
║  Ensure firewall allows port ${PORT} access               ║
╚════════════════════════════════════════════════════════╝
    `);
});