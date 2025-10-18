#!/bin/bash
# =============================================================================
# Azure Database Initialization Script
# =============================================================================
# This script initializes the Azure PostgreSQL Database

echo "🔵 Initializing AZURE PostgreSQL Database"
echo "========================================="

# Ensure we're using production environment
export FLASK_ENV=production

echo "🔗 Database: Azure Database for PostgreSQL"
echo ""

# Run the initialization script
python3 db/init.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Azure database initialization complete!"
    echo "🚀 Your Azure database is ready for production deployment"
else
    echo ""
    echo "❌ Azure database initialization failed!"
    echo "💡 Troubleshooting tips:"
    echo "   1. Check your Azure database password in .env"
    echo "   2. Ensure your IP is allowed in Azure firewall rules"
    echo "   3. Verify Azure database is running and accessible"
    echo "   4. Check SSL certificate requirements"
    exit 1
fi