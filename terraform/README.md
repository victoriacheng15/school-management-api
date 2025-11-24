# 🧪 Terraform Sandbox: Azure Backend Provisioning

This folder contains a **learning experiment** to explore Infrastructure-as-Code (IaC) using Terraform with Azure.

## 🎯 Purpose

- Understand how to provision Azure resources declaratively
- Compare manual (GUI) vs code-driven infrastructure
- Learn Terraform fundamentals: state, providers, dependencies, plans

## 🛠 Resources Created

- Azure Resource Group
- PostgreSQL Flexible Server (v16, public access)
- Firewall rules (local IP: `190.12.150.123` + Azure services)
- Linux Web App (Python 3.10, B1 SKU)

## ▶️ How to Run

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
terraform destroy -auto-approve
```
