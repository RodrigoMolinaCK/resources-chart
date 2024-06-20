import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

log_file = 'server_resources.log'

timestamps = []
cpu_usages = []
memory_usages = []
disk_usages = []

timestamp_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
cpu_pattern = re.compile(r'%Cpu\(s\):\s+(.*)')
memory_pattern = re.compile(r'Memory Usage:\s+(\d+)/\d+MB \((\d+\.\d+)%\)')
disk_pattern = re.compile(r'Disk Usage:\s+(\d+)/\d+GB \((\d+)%\)')

with open(log_file, 'r') as file:
    lines = file.readlines()
    current_timestamp = None
    
    for line in lines:
        timestamp_match = timestamp_pattern.match(line)
        if timestamp_match:
            current_timestamp = timestamp_match.group()
            timestamps.append(datetime.strptime(current_timestamp, '%Y-%m-%d %H:%M:%S'))
        
        cpu_match = cpu_pattern.search(line)
        if cpu_match:
            cpu_values = [float(x) for x in re.findall(r'\d+\.\d+', cpu_match.group(1))]
            if len(cpu_values) >= 4:
                cpu_usages.append(100 - cpu_values[3]) 
        
        memory_match = memory_pattern.search(line)
        if memory_match:
            memory_usages.append(float(memory_match.group(2)))
        
        disk_match = disk_pattern.search(line)
        if disk_match:
            disk_usages.append(float(disk_match.group(2)))

min_length = min(len(timestamps), len(cpu_usages), len(memory_usages), len(disk_usages))
timestamps = timestamps[:min_length]
cpu_usages = cpu_usages[:min_length]
memory_usages = memory_usages[:min_length]
disk_usages = disk_usages[:min_length]

data = {
    'Timestamp': timestamps,
    'CPU Usage (%)': cpu_usages,
    'Memory Usage (%)': memory_usages,
    'Disk Usage (%)': disk_usages
}
df = pd.DataFrame(data)

# Plot the data
plt.figure(figsize=(14, 7))

plt.subplot(3, 1, 1)
plt.plot(df['Timestamp'], df['CPU Usage (%)'], label='CPU Usage (%)', color='b')
plt.xlabel('Time')
plt.ylabel('CPU Usage (%)')
plt.title('CPU Usage Over Time')
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(df['Timestamp'], df['Memory Usage (%)'], label='Memory Usage (%)', color='g')
plt.xlabel('Time')
plt.ylabel('Memory Usage (%)')
plt.title('Memory Usage Over Time')
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(df['Timestamp'], df['Disk Usage (%)'], label='Disk Usage (%)', color='r')
plt.xlabel('Time')
plt.ylabel('Disk Usage (%)')
plt.title('Disk Usage Over Time')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()