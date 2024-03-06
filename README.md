# andyxcopy

**Introduction:**

AndyXcopy is an advanced local file copying tool for Linux environments, developed using Python scripts and leveraging the capabilities of rsync and GNU parallel. This tool is designed to enhance file copying operations by enabling high-efficiency file synchronization and concurrent execution.

AndyXcopy是一种适用于Linux环境的高级本地文件复制工具，使用Python脚本开发，并利用rsync和parallel功能。此工具旨在通过实现更高效的文件同步和并发执行来增强文件复制操作。

----------

**Installation:**

wget https://raw.githubusercontent.com/AndyX-Net/andyxcopy/main/andyxcopy.py && chmod +x andyxcopy.py

----------

**Usage:**

positional arguments:

    source                Source directory
  
    target                Target directory

options:

    -h, --help            show this help message and exit
  
    --batch BATCH, -b BATCH
  
                        Number of concurrent operations, default is 4
                        
    --depth DEPTH, -d DEPTH
  
                        Scan depth, default is 4
                        
    --quiet, -q           Quiet mode, no output
  


----------

**Example:**

andyxcopy.py -b 8 -p 10 -q /ai /ai2

----------

**Screenshots:**

Thread utilization
![image](https://github.com/AndyX-Net/andyxcopy/assets/27819097/7c3d9a8f-069e-4bc6-9481-4fbb409bb4b7)

**Disk utilization (Standard HDD throughput 60MB/s)**
![image](https://github.com/AndyX-Net/andyxcopy/assets/27819097/efaddf43-d8d3-42b5-bdad-7bbdc8bc5452)



