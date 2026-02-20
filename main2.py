import json
import os
import subprocess
import logging
from pydantic import BaseModel, Field, ValidationError
from typing import List, Literal
from src.machine import Machine

# 1. הגדרת מערכת הלוגים (Logging)
# הקוד הזה דואג שהלוגים ייכתבו גם למסך וגם לקובץ בתיקיית logs

os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/provisioning.log"), # כאן היה התיקון (FileHandler במקום FileStreamHandler)
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 2. מודל אימות נתונים
class VMData(BaseModel):
    name: str
    os: Literal["Ubuntu", "CentOS"] # רק הערכים האלו יתקבלו
    cpu: int = Field(ge=1, le=4)
    ram: int = Field(ge=1, le=4)

# 3. פונקציה להרצת Bash
def run_provisioning_script(machine_name):
    # תיעוד תחילת התהליך (דרישה: "When provisioning starts")
    logger.info(f">>> Provisioning STARTED for machine: {machine_name}")
    
    try:
        # הרצת הסקריפט
        result = subprocess.run(
            ['bash', 'scripts/install_nginx.sh', machine_name],
            check=True,
            text=True,
            capture_output=True
        )
        
        # אם הגענו לכאן, הסקריפט הצליח (Success message)
        logger.info(f"SUCCESS: Provisioning completed for {machine_name}.")
        
    except subprocess.CalledProcessError as e:
        # תיעוד שגיאות מהסקריפט (Any errors encountered)
        logger.error(f"FAILED: Provisioning error on {machine_name}. Error: {e.stderr}")
    except Exception as e:
        # תיעוד שגיאות פייתון כלליות
        logger.error(f"CRITICAL: Unexpected exception for {machine_name}: {str(e)}")
    finally:
        # תיעוד סיום התהליך (דרישה: "When provisioning ends")
        logger.info(f"<<< Provisioning ENDED for machine: {machine_name}")

# 4. פונקציה לקבלת קלט


# def get_user_input() -> List[Machine]:
#     machines = []
    
#     # בקשת מספר המכונות הכולל
#     while True:
#         try:
#             num_input = input("Enter number of machines to create: ")
#             num = int(num_input)
#             if num <= 0: raise ValueError
#             break
#         except ValueError:
#             print("Invalid input. Please enter a positive number.")

#     for i in range(num):
#         print(f"\n--- Configuring Machine #{i+1} ---")
        
#         while True: # לולאת תיקון עבור כל מכונה
#             try:
#                 name = input("Enter machine name: ")
#                 os_choice = input("Choose OS (Ubuntu/CentOS): ")
#                 cpu_val = int(input("Enter CPU (1-4): "))
#                 ram_val = int(input("Enter RAM (1-4): "))

#                 # כאן מתבצעת הבדיקה של Pydantic
#                 data = VMData(name=name, os=os_choice, cpu=cpu_val, ram=ram_val)
                
#                 # אם עברנו את השורה הקודמת, הכל תקין
#                 new_vm = Machine(data.name, data.os, data.cpu, data.ram)
#                 machines.append(new_vm)
#                 break # יוצאים מהלולאה הפנימית ועוברים למכונה הבאה
                
#             except (ValidationError, ValueError) as e:
#                 print("\n" + "!"*30)
#                 print(" ERROR IN DETAILS! Please note:")
#                 print(" - OS must be EXACTLY 'Ubuntu' or 'CentOS'")
#                 print(" - CPU & RAM must be a whole number between 1 and 4")
#                 print("!"*30 + "\n")
                
#     return machines


def get_user_input() -> List[Machine]:
    machines = []
    
    # שאלה ראשונה: כמה מכונות?
    while True:
        try:
            num = int(input("Enter number of machines to create: "))
            if num <= 0: raise ValueError
            break
        except ValueError:
            print("❌ Invalid input: Please enter a positive number.")

    for i in range(num):
        print(f"\n--- Configuring Machine #{i+1} ---")
        
        # 1. קלט שם (לא יכול להיות ריק)
        while True:
            name = input("Enter machine name: ").strip()
            if name: break
            print("❌ Name cannot be empty.")

        # 2. קלט OS (חייב להיות Ubuntu או CentOS)
        while True:
            os_choice = input("Choose OS (Ubuntu/CentOS): ").strip()
            if os_choice in ["Ubuntu", "CentOS"]: break
            print("❌ Invalid OS: Please choose exactly 'Ubuntu' or 'CentOS'.")

        # 3. קלט CPU (חייב להיות מספר בין 1 ל-4)
        while True:
            try:
                cpu_val = int(input("Enter CPU (1-4): "))
                if 1 <= cpu_val <= 4: break
                print("❌ Out of range: CPU must be between 1 and 4.")
            except ValueError:
                print("❌ Invalid input: Please enter a number.")

        # 4. קלט RAM (חייב להיות מספר בין 1 ל-4)
        while True:
            try:
                ram_val = int(input("Enter RAM (1-4): "))
                if 1 <= ram_val <= 4: break
                print("❌ Out of range: RAM must be between 1 and 4.")
            except ValueError:
                print("❌ Invalid input: Please enter a number.")

        # יצירת האובייקט (כאן אנחנו בטוחים שהכל תקין)
        data = VMData(name=name, os=os_choice, cpu=cpu_val, ram=ram_val)
        new_vm = Machine(data.name, data.os, data.cpu, data.ram)
        machines.append(new_vm)
        print(f"✅ Machine '{name}' added successfully!")
                
    return machines

# 5. שמירה ל-JSON
def save_configs(machines: List[Machine]):
    output = [m.to_dict() for m in machines]
    os.makedirs('configs', exist_ok=True)
    with open('configs/instances.json', 'w') as f:
        json.dump(output, f, indent=4)
    logger.info(f"Saved {len(machines)} configurations to configs/instances.json")

# 6. המנוע הראשי
if __name__ == "__main__":
    logger.info("Infrastructure tool started.")
    vms = get_user_input()
    
    if vms:
        save_configs(vms)
        for vm in vms:
            run_provisioning_script(vm.name)
    
    logger.info("Infrastructure tool finished.")
    print("\nCheck logs/provisioning.log for full details.")