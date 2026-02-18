import json
import os
from pydantic import BaseModel, Field
from typing import List
from src.machine import Machine  # ייבוא המחלקה מהתיקייה שפתחנו
import subprocess

# 1. מודל האימות (Data Validation) - משאירים אותו פשוט
class VMData(BaseModel):
    name: str
    os: str
    cpu: int = Field(ge=1, le=4)
    ram: int = Field(ge=1, le=4)

def get_user_input() -> List[Machine]:
    machines = []
    # הלוגיקה של ה-while שכתבת מצוינת, נשתמש בה כדי למלא את האובייקטים
    num_machines = int(input("Enter the number of machines to create: "))
    
    for _ in range(num_machines):
        # כאן אוספים את הנתונים (כמו שעשית)
        name = input("Enter machine name: ")
        os_type = input("Choose OS (Ubuntu/CentOS): ")
        cpu = int(input("Enter CPU cores (1-4): "))
        ram = int(input("Enter RAM in GB (1-4): "))

        try:
            # אימות הנתונים בעזרת Pydantic
            data = VMData(name=name, os=os_type, cpu=cpu, ram=ram)
            
            # יצירת אובייקט מהמחלקה Machine (כפי שנדרש ב-src/machine.py)
            new_vm = Machine(data.name, data.os, data.cpu, data.ram)
            machines.append(new_vm)
            
        except Exception as e:
            print(f"Validation error: {e}")
            
    return machines

def save_configs(machines: List[Machine]):
    # יצירת רשימת מילונים לשמירה ב-JSON
    output_data = [m.to_dict() for m in machines]
    
    os.makedirs('configs', exist_ok=True) # יצירת התיקייה אם אינה קיימת
    with open('configs/instances.json', 'w') as f:
        json.dump(output_data, f, indent=4)

if __name__ == "__main__":
    vms = get_user_input()
    if vms:
        save_configs(vms)
        print(f"Successfully saved {len(vms)} machines to configs/instances.json")

def run_provisioning_script(machine_name):
    """מריץ את סקריפט ה-Bash עבור מכונה ספציפית"""
    print(f"\n[INFO] Provisioning service for {machine_name}...")
    
    try:
        # הרצת הסקריפט. אנחנו מעבירים את שם המכונה כארגומנט ($1 בסקריפט)
        result = subprocess.run(
            ['bash', 'scripts/install_nginx.sh', machine_name],
            check=True,          # יזרוק שגיאה אם הסקריפט נכשל (exit code לא 0)
            text=True,           # יחזיר את הפלט כטקסט ולא כבייטים
            capture_output=True  # תופס את מה שהסקריפט הדפיס (stdout/stderr)
        )
        
        # הדפסת הפלט של הסקריפט
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Script failed for {machine_name}: {e.stderr}")
    except FileNotFoundError:
        print("[ERROR] Could not find the bash script in scripts/ folder.")

if __name__ == "__main__":
    # 1. קבלת קלט מהמשתמש
    vms = get_user_input()
    
    if vms:
        # 2. שמירת הקונפיגורציה
        save_configs(vms)
        
        # 3. הרצת סקריפט ההתקנה לכל מכונה ברשימה (השלב החדש)
        for vm in vms:
            run_provisioning_script(vm.name)
            
        print("\n--- All tasks completed! ---")