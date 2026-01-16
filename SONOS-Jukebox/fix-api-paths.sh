#!/bin/sh
# Fix API paths for Home Assistant ingress compatibility

echo "Fixing API paths for ingress compatibility..."

# Find all JavaScript files in www directory and replace ../api/ with api/
find /app/www -name "*.js" -type f -exec sed -i 's|"\.\./api/|"api/|g' {} \;
find /app/www -name "*.js" -type f -exec sed -i "s|'\.\./api/|'api/|g" {} \;

# Also fix /api/ to api/ for consistency
find /app/www -name "*.js" -type f -exec sed -i 's|"/api/|"api/|g' {} \;
find /app/www -name "*.js" -type f -exec sed -i "s|'/api/|'api/|g" {} \;

echo "API paths fixed successfully"
