terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "64fa42e1-96ef-4d78-849c-6cd49ff2bea7"  # ← your sub ID
}

variable "location" { default = "westus2" }
variable "resource_group_name" { default = "terraform-rg" }
variable "server_name" { default = "school-api-tf-flex" }
variable "admin_user" { default = "schooladmin" }
variable "admin_password" {
  default   = "seriousPassword123!"
  sensitive = true
}
variable "db_name" { default = "school-db" }

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

# PostgreSQL Flexible Server — PUBLIC ACCESS, NO VNET
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = var.server_name
  resource_group_name    = azurerm_resource_group.main.name
  location               = azurerm_resource_group.main.location
  version                = "16"
  administrator_login    = var.admin_user
  administrator_password = var.admin_password

  sku_name   = "B_Standard_B1ms"  # Burstable is cheapest for learning
  storage_mb = 32768

  # This enables public-only mode
  public_network_access_enabled = true

  backup_retention_days         = 7
  geo_redundant_backup_enabled  = false
  zone = 2
}

# Database
resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = var.db_name
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# 🔥 Firewall Rule: Allow your local IP (optional but recommended)
# Get your IP at https://ifconfig.me
# or use curl -4 ifconfig.me
resource "azurerm_postgresql_flexible_server_firewall_rule" "local" {
  name             = "AllowLocal"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = ""  # e.g., "24.123.45.67"
  end_ip_address   = ""
}

# Optional: Allow Azure services (e.g., GitHub Actions from Azure)
resource "azurerm_postgresql_flexible_server_firewall_rule" "azure" {
  name             = "AllowAzure"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# Outputs
output "fqdn" {
  value = azurerm_postgresql_flexible_server.main.fqdn
}

output "connection_string" {
  value = "postgresql://${var.admin_user}:${var.admin_password}@${azurerm_postgresql_flexible_server.main.fqdn}:5432/${var.db_name}"
  sensitive = true
}

# ===== AZURE WEB APP =====

variable "web_app_name" {
  default = "school-api-webapp"  # must be globally unique
}

variable "runtime_version" {
  default = "3.10"  # Python version
}

# App Service Plan (required for Web App)
resource "azurerm_service_plan" "main" {
  name                = "school-appservice-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "B1"  # Basic tier, cheap for learning
}

# Web App
resource "azurerm_linux_web_app" "main" {
  name                = var.web_app_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.main.id

  # Python runtime
  site_config {
    application_stack {
      python_version = var.runtime_version
    }
  }

  # App settings (e.g., DB connection)
  app_settings = {
    "DB_HOST"     = azurerm_postgresql_flexible_server.main.fqdn
    "DB_NAME"     = var.db_name
    "DB_USER"     = var.admin_user
    "DB_PASSWORD" = var.admin_password
    "WEBSITE_RUN_FROM_PACKAGE" = "0"  # if using local code deploy
  }

  # Optional: enable HTTPS only
  https_only = true
}

# Output Web App URL
output "web_app_url" {
  value = "https://${azurerm_linux_web_app.main.default_hostname}"
}