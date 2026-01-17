// Patch server.js for Home Assistant addon and ingress compatibility
const fs = require('fs');
const serverFile = '/app/server.js';

let content = fs.readFileSync(serverFile, 'utf8');

// Replace the listen call to bind to all interfaces with environment variables
content = content.replace(
  /app\.listen\(port, \(\) => \{/,
  'app.listen(port, process.env.HOST || "0.0.0.0", () => {'
);

// Update console log to show correct binding
content = content.replace(
  /console\.log\(\`Server running on port \$\{port\}\`\);/,
  'console.log(`Server running on ${process.env.HOST || "0.0.0.0"}:${port}`);'
);

fs.writeFileSync(serverFile, content);
console.log('Server patched for Home Assistant addon compatibility');
