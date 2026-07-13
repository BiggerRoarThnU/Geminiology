#!/bin/bash
LOG_FILE="~/SovereignNexus/science_logs/vitals_$(date +%Y%m%d_%H%M).csv"
echo "Timestamp,CPU_Usage(%),Mem_Usage(MB),Load_1m" > $LOG_FILE
while true; do
    TIMESTAMP=$(date +%H:%M:%S)
    CPU=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    MEM=$(free -m | awk '/Mem:/ {print $3}')
    LOAD=$(cat /proc/loadavg | awk '{print $1}')
    echo "$TIMESTAMP,$CPU,$MEM,$LOAD" >> $LOG_FILE
    sleep 10
done
