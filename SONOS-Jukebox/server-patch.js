// Patch server.js to bind to 0.0.0.0 and fix static serving
const fs = require('fs');
const serverFile = '/app/server.js';

let content = fs.readFileSync(serverFile, 'utf8');

// Replace the listen call to bind to all interfaces
content = content.replace(
  /app\.listen\(8200\);/,
  'app.listen(8200, "0.0.0.0");'
);

content = content.replace(
  /console\.log\("App listening on port 8200"\);/,
  'console.log("App listening on 0.0.0.0:8200");'
);

// Ensure static files are served correctly
content = content.replace(
  /app\.use\(express\.static\(path\.join\(__dirname, 'www'\)\)\);/,
  'app.use(express.static(path.join(__dirname, "www"), { index: "index.html" }));'
);

fs.writeFileSync(serverFile, content);
console.log('Server patched for 0.0.0.0:8200 and static file serving');