import logging

# הגדרת הלוגר (דרישה של הפרויקט)
logger = logging.getLogger(__name__)

class Machine:
    def __init__(self, name, os, cpu, ram):
        self.name = name
        self.os = os
        self.cpu = cpu
        self.ram = ram
        # לוג שמתעד יצירת מכונה חדשה
        logger.info(f"Machine object created: {self.name} ({self.os})")

    def to_dict(self):
        """מחזיר ייצוג של המכונה כמילון (מתאים לשמירה ב-JSON)"""
        return {
            "name": self.name,
            "os": self.os,
            "cpu": self.cpu,
            "ram": self.ram
        }