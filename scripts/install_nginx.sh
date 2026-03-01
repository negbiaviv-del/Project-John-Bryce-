#!/bin/bash

LOG_FILE="logs/provisioning.log"
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log_message() {
    local TYPE=$1
    local MESSAGE=$2
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $TYPE - [BASH] $MESSAGE" >> "$LOG_FILE"
    
    if [ "$TYPE" == "SUCCESS" ]; then
        echo -e "${GREEN}✅ $MESSAGE${NC}"
    elif [ "$TYPE" == "ERROR" ]; then
        echo -e "${RED}❌ $MESSAGE${NC}"
    else
        echo "ℹ️  $MESSAGE"
    fi
}

if [ -z "$1" ]; then
    log_message "ERROR" "No machine name provided."
    exit 1
fi

log_message "INFO" "Starting real configuration for machine: $1"

if command -v nginx >/dev/null 2>&1; then
    log_message "SUCCESS" "Nginx is already installed on $1."
else
    log_message "INFO" "Nginx not found. Identifying Package Manager..."

    if [ -x "$(command -v apt-get)" ]; then
        log_message "INFO" "Using APT (Ubuntu/Debian). Updating and installing..."
        sudo apt-get update -y >/dev/null
        sudo apt-get install nginx -y >/dev/null
    elif [ -x "$(command -v yum)" ]; then
        log_message "INFO" "Using YUM (CentOS/RHEL). Installing..."
        sudo yum install epel-release -y >/dev/null
        sudo yum install nginx -y >/dev/null
    else
        log_message "ERROR" "No supported package manager found (apt or yum)."
        exit 1
    fi

    if [ $? -eq 0 ]; then
        sudo systemctl enable nginx >/dev/null 2>&1
        sudo systemctl start nginx >/dev/null 2>&1
    else
        log_message "ERROR" "Installation failed on $1."
        exit 1
    fi
fi

log_message "INFO" "Verifying service status for $1..."
sleep 2 

SERVICE_STATUS=$(systemctl is-active nginx)

if [ "$SERVICE_STATUS" == "active" ]; then
    log_message "SUCCESS" "Nginx is ACTIVE and running on $1!"
    
    if command -v curl >/dev/null 2>&1; then
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost)
        if [ "$HTTP_CODE" == "200" ]; then
            log_message "SUCCESS" "Health Check passed! HTTP 200 OK."
        else
            log_message "WARNING" "Service is running but returned HTTP $HTTP_CODE."
        fi
    fi
else
    log_message "ERROR" "Nginx is NOT running. Status: $SERVICE_STATUS"
    exit 1
fi

log_message "INFO" "Provisioning process finished for $1."
exit 0