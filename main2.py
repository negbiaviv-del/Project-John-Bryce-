import json
import os
import subprocess
import logging
import uuid
from pydantic import BaseModel, Field, ValidationError
from typing import List, Literal
from src.machine import Machine

# 1. הגדרת מערכת הלוגים 📝
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/provisioning.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 2. מודל אימות נתונים 🛡️
class VMData(BaseModel):
    name: str
    os: Literal["Ubuntu", "CentOS"]
    cpu: int = Field(ge=1, le=4)
    ram: int = Field(ge=1, le=4)

def get_user_input() -> List[dict]:
    aws_formatted_machines = []
    
    # שלב א: כמות מכונות (1-10) 🔢
    while True:
        try:
            val = input("🔢 Enter number of machines to create (1-10): ")
            num = int(val)
            if 1 <= num <= 10:
                break
            err = f"Invalid count {num}: Please stay between 1 and 10."
            logger.error(f"❌ {err}")
            print(f"❌ {err}")
        except ValueError:
            err = "User entered non-numeric value for machine count"
            logger.error(f"❌ {err}")
            print(f"❌ {err}")

    # שלב ב: הגדרת כל מכונה בנפרד 🛠️
    for i in range(num):
        print(f"\n--- 🖥️  Configuring Machine #{i+1} ---")
        
        while True:
            name = input("🏷️  Enter machine name: ").strip()
            if name: break
            print("❌ Name cannot be empty.")

        while True:
            os_choice = input("💿 Choose OS (Ubuntu/CentOS): ").strip()
            if os_choice in ["Ubuntu", "CentOS"]: break
            print("❌ Invalid OS. Choose 'Ubuntu' or 'CentOS'.")

        while True:
            try:
                cpu_val = int(input("⚡ Enter CPU (1-4): "))
                if 1 <= cpu_val <= 4: break
                err = f"CPU {cpu_val} out of range (1-4)."
                logger.error(f"❌ {err}")
                print(f"❌ {err}")
            except ValueError:
                err = "Non-integer entered for CPU"
                logger.error(f"❌ {err}")
                print("❌ CPU must be a whole number.")

        while True:
            try:
                ram_val = int(input("🧠 Enter RAM (1-4): "))
                if 1 <= ram_val <= 4: break
                err = f"RAM {ram_val} out of range (1-4)."
                logger.error(f"❌ {err}")
                print(f"❌ {err}")
            except ValueError:
                err = "Non-integer entered for RAM"
                logger.error(f"❌ {err}")
                print("❌ RAM must be a whole number.")

        # יצירת מבנה AWS ☁️
        aws_vm = {
            "InstanceId": f"i-{uuid.uuid4().hex[:8]}",
            "InstanceName": name,
            "InstanceType": f"t2.{cpu_val}cpu.{ram_val}ram",
            "ImageId": "ami-012345" if os_choice == "Ubuntu" else "ami-067890",
            "State": "Pending"
        }
        aws_formatted_machines.append(aws_vm)
        logger.info(f"✅ Machine '{name}' added to configuration.")
                
    return aws_formatted_machines

if __name__ == "__main__":
    logger.info("🚀 Application starting...")
    vms = get_user_input()
    
    if vms:
        # שמירת JSON 💾
        os.makedirs('configs', exist_ok=True)
        with open('configs/instances.json', 'w') as f:
            json.dump(vms, f, indent=4)
        logger.info("💾 Saved configuration to configs/instances.json")

        # הרצת פרוויז'נינג ⚙️
        print("\n--- 🚀 Starting Deployment Phase ---")
        for vm in vms:
            logger.info(f"⚙️  Provisioning {vm['InstanceName']}...")
            try:
                # הרצת הסקריפט
                subprocess.run(['bash', 'scripts/install_nginx.sh', vm['InstanceName']], check=True)
                logger.info(f"✨ SUCCESS: {vm['InstanceName']} deployed successfully!")
            except Exception as e:
                logger.error(f"💥 FAILED: {vm['InstanceName']} deployment error: {e}")

    logger.info("🏁 Application finished.")
    print("\n📂 Check logs/provisioning.log for full details.")
