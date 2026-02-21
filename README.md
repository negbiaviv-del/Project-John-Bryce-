# 🛠 DevOps Infrastructure Provisioning Tool

A modular Python application designed to automate virtual machine configuration and service deployment. This tool combines **Object-Oriented Programming (OOP)**, **Data Validation (Pydantic)**, and **Bash Automation**.

---

## 📋 Project Overview & Objectives
The goal of this project is to create a reliable and validated pipeline for infrastructure management, bridging the gap between high-level logic and system-level execution.

### Key Objectives:
* **Infrastructure as Code (IaC):** Programmatic definition of machine configurations.
* **Strict Data Validation:** Hardware specs (CPU/RAM) enforcement via Pydantic.
* **Process Automation:** Automated Nginx installation and status checks.
* **Auditability:** Centralized logging for all actions and errors.

---

### 📂 Project Structure
```text
INFRA/
├── main2.py              # Main application logic & CLI
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
├── src/
│   └── machine.py        # Machine class (OOP)
├── scripts/
│   └── install_nginx.sh  # Bash provisioning script
├── configs/
│   └── instances.json    # JSON storage for VMs
└── logs/
    └── provisioning.log  # Centralized execution logs

--- 

#### Environment Setup

Clone the repository and prepare the virtual environment:
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# 2. Permissions
Ensure the automation script is executable:
Bash
chmod +x scripts/install_nginx.sh

# 3. Running the Tool
Start the interactive provisioning process:
Bash
python3 main2.py

🖥 Example Expected Output:

Enter number of machines to create: 1

--- Configuring Machine #1 ---
Enter machine name: Web-Server-01
Choose OS (Ubuntu/CentOS): Ubuntu
Enter CPU (1-4): 2
Enter RAM (1-4): 4
✅ Machine 'Web-Server-01' added successfully!

[2026-02-21 12:00:00] INFO: Starting Bash provisioning for: Web-Server-01
[2026-02-21 12:00:02] SUCCESS: Nginx installed successfully on Web-Server-01!

--- All tasks completed! ---
Check logs/provisioning.log for full details.

---

## 🚀 Future Enhancements & Roadmap
This project is designed as a modular foundation for more advanced cloud automation. Future iterations will include:

* **Cloud Integration (AWS):** Replacing mock provisioning with real **AWS EC2** instances using the `boto3` library.
* **Infrastructure as Code (Terraform):** Using Python to trigger **Terraform** plans for automated resource management.
* **Advanced Orchestration:** Expanding configurations to support multi-node clusters and complex microservices.
* **Containerization:** Incorporating Docker setup via the existing Bash automation layer.

---
*Developed as a foundation for professional DevOps workflows.*