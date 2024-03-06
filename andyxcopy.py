#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from pathlib import Path
import tempfile

def check_and_install_packages():
    # Check system distribution
    distro = subprocess.check_output("cat /etc/*-release", shell=True).decode().lower()
    package_manager = None
    if "ubuntu" in distro or "debian" in distro:
        package_manager = "apt-get"
    elif "rhel" in distro or "centos" in distro or "fedora" in distro:
        package_manager = "yum"
    elif "suse" in distro:
        package_manager = "zypper"
    else:
        print("Unsupported Linux distribution")
        sys.exit(1)

    # Check if rsync and parallel are installed
    rsync_installed = subprocess.call("which rsync", shell=True) == 0
    parallel_installed = subprocess.call("which parallel", shell=True) == 0

    # Decide action based on installation status
    if not rsync_installed or not parallel_installed:
        response = input("rsync or parallel is not installed. Would you like to install them? (y/n): ")
        if response.lower() == 'y':
            if not rsync_installed:
                subprocess.call(f"{package_manager} install rsync -y", shell=True)
            if not parallel_installed:
                subprocess.call(f"{package_manager} install parallel -y", shell=True)
        else:
            print("Operation cancelled by the user")
            sys.exit(1)

def generate_rsync_commands(source, target, batch, depth, quiet):
    # Generate list of rsync commands
    rsync_commands = []
    source_path = Path(source).resolve()
    target_path = Path(target).resolve()
    for root, dirs, files in os.walk(source, topdown=True):
        root_path = Path(root).resolve()
        relative_depth = len(root_path.relative_to(source_path).parts)
        if relative_depth <= depth:
            for dir in dirs:
                src_dir_path = root_path / dir
                relative_path = src_dir_path.relative_to(source_path)
                tgt_dir_path = target_path / relative_path
                cmd = f"rsync -avh {'--quiet' if quiet else ''} {src_dir_path}/ {tgt_dir_path}/\n"
                rsync_commands.append(cmd)
    return rsync_commands

def run_parallel_commands(commands, batch):
    # Execute commands using parallel
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmpfile:
        tmpfile.writelines(commands)
        tmpfile_name = tmpfile.name
    cmd = f"parallel -j {batch} < {tmpfile_name}"
    subprocess.call(cmd, shell=True)
    os.remove(tmpfile_name)

def main():
    parser = argparse.ArgumentParser(description="AndyXcopY is a Python script for efficient concurrent local file copying on Linux, utilizing rsync and parallel for effective file synchronization. ")
    parser.add_argument("--batch", "-b", type=int, default=4, help="Number of concurrent operations, default is 4")
    parser.add_argument("--depth", "-d", type=int, default=4, help="Scan depth, default is 4")
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet mode, no detailed output")
    parser.add_argument("source", type=str, help="Source directory")
    parser.add_argument("target", type=str, help="Target directory")
    args = parser.parse_args()

    check_and_install_packages()
    commands = generate_rsync_commands(str(args.source), str(args.target), args.batch, args.depth, args.quiet)
    run_parallel_commands(commands, args.batch)

if __name__ == "__main__":
    main()
