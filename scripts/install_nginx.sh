#!/bin/bash

# הגדרת צבעים להדפסה יפה
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "Starting configuration for machine: $1"

# בדיקה אם החבילה כבר מותקנת (כפי שנדרש ב-Hint)
if command -v nginx >/dev/null 2>&1; then
    echo -e "${GREEN}Nginx is already installed. Skipping installation.${NC}"
else
    echo "Nginx not found. Installing..."
    # כאן תבוא פקודת ההתקנה האמיתית (למשל sudo apt install nginx -y)
    # לצורך הפרויקט אנחנו נדמה הצלחה:
    sleep 2
    echo -e "${GREEN}Nginx installed successfully on $1!${NC}"
fi

exit 0