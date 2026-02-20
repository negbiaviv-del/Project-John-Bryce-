#!/bin/bash

# הגדרת נתיב לקובץ הלוג
LOG_FILE="logs/provisioning.log"
GREEN='\033[0;32m'
NC='\033[0m'

# פונקציה לכתיבת לוגים (מדפיסה למסך עם צבע ולקובץ בלי צבע)
log_message() {
    local TYPE=$1
    local MESSAGE=$2
    # כתיבה לקובץ הלוג
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $TYPE - [BASH] $MESSAGE" >> "$LOG_FILE"
    # הדפסה למסך (עם צבע ירוק אם זו הצלחה)
    if [ "$TYPE" == "SUCCESS" ]; then
        echo -e "${GREEN}$MESSAGE${NC}"
    else
        echo "$MESSAGE"
    fi
}

# --- תחילת הביצוע ---

log_message "INFO" "Starting configuration for machine: $1"

# בדיקה אם החבילה כבר מותקנת (ה-Hint מהפרויקט)
if command -v nginx >/dev/null 2>&1; then
    log_message "SUCCESS" "Nginx is already installed on $1. Skipping installation."
else
    log_message "INFO" "Nginx not found. Installing..."
    
    # דימוי התקנה (כאן אפשר להריץ sudo apt install nginx -y אם רוצים)
    sleep 2
    
    # בדיקת סטטוס היציאה של הפקודה האחרונה
    if [ $? -eq 0 ]; then
        log_message "SUCCESS" "Nginx installed successfully on $1!"
    else
        log_message "ERROR" "Installation failed on $1."
        exit 1
    fi
fi

log_message "INFO" "Provisioning ended for $1."
exit 0