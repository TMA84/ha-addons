#!/bin/sh
# Fix API paths for Home Assistant ingress compatibility

echo "Fixing API paths for ingress compatibility..."

# Find all JavaScript files in www directory and replace ../api/ with api/
for file in $(find /app/www -name "*.js" -type f); do
    sed -i 's|"\.\./api/|"api/|g' "$file"
    sed -i "s|'\.\./api/|'api/|g" "$file"
    sed -i 's|"/api/|"api/|g' "$file"
    sed -i "s|'/api/|'api/|g" "$file"
done

echo "API paths fixed successfully"
