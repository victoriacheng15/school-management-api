#!/bin/bash
# =============================================================================
# Azure Database Drop Tables Script
# =============================================================================
# This script drops all tables in the Azure PostgreSQL Database

export FLASK_ENV=production

echo "🔴 Dropping all tables in Azure PostgreSQL Database..."
python3 db/drop_all_tables.py

if [ $? -eq 0 ]; then
    echo "✅ All tables dropped from Azure DB."
else
    echo "❌ Failed to drop tables. Check connection and credentials."
    exit 1
fi
