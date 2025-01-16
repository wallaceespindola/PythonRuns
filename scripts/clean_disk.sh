#!/bin/bash

echo ""
echo ">>> Starting full system cleanup..."

echo ""
echo ">>> Displaying current disk usage before cleanup..."
df -h

echo ""
echo ">>> Cleaning journal logs (keeping logs from the last 2 days)..."
sudo journalctl --vacuum-time=2d

echo ""
echo ">>> Cleaning journal logs larger than 50MB..."
sudo journalctl --vacuum-size=50M  # Adjust size limit as necessary

echo ""
echo ">>> Removing old Snap packages..."
sudo snap remove --purge lxd
sudo snap remove --purge core
sudo snap set system refresh.retain=2
sudo snap refresh

echo ""
echo ">>> Removing old revisions of snaps (make sure all snaps are closed)..."
# CLOSE ALL SNAPS BEFORE RUNNING THIS
set -eu
LANG=en_US.UTF-8 snap list --all | awk '/disabled/{print $1, $3}' |
    while read snapname revision; do
        echo ""
        echo ">>> Removing Snap $snapname revision $revision..."
        sudo snap remove "$snapname" --revision="$revision"
    done

echo ""
echo ">>> Cleaning Flutter cache..."
rm -rf /root/flutter/bin/cache/*
rm -rf /root/flutter/.pub-preload-cache/*

echo ""
echo ">>> Cleaning APT package cache..."
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*

echo ""
echo ">>> Removing unused APT auto-remove packages to clean unused dependencies..."
sudo apt-get autoremove -y
sudo apt-get autoclean

echo ""
echo ">>> Cleaning unused thumbnail cache..."
rm -rf ~/.cache/thumbnails/*

echo ""
echo ">>> Removing temporary files..."
sudo rm -rf /tmp/*

echo ""
echo ">>> Removing old crash reports..."
sudo rm -rf /var/crash/*

if command -v docker &> /dev/null; then
    echo ""
    echo ">>> Cleaning up Docker system (remove stopped containers, dangling images, and unused networks)..."
    sudo docker system prune -af
fi

echo ""
echo ">>> Removing orphaned packages..."
sudo deborphan | xargs sudo apt-get -y remove --purge

echo ""
echo ">>> Removing old kernel versions (use with caution, ensure you're not removing the current kernel)..."
sudo apt-get autoremove --purge

if command -v npm &> /dev/null; then
    echo ""
    echo ">>> Cleaning npm cache (if Node.js is used)..."
    npm cache clean --force
fi

echo ""
echo ">>> Cleaning Dart SDK cache..."
rm -rf /root/flutter/bin/cache/dart-sdk/bin/snapshots/*

echo ""
echo ">>> Removing log files older than 7 days..."
find /var/log -type f -name "*.log" -mtime +7 -exec rm -f {} \;

echo ""
echo ">>> Removing orphaned symlinks..."
#find / -xtype l -exec rm -f {} \;

echo ""
echo ">>> Removing Python cache files..."
#find / -name "__pycache__" -type d -exec rm -rf {} +

echo ""
echo ">>> Removing core dumps..."
sudo find / -type f -name "core" -exec rm -f {} \;

echo ""
echo ">>> Removing mysql logs..."
rm -rf /var/lib/mysql/binlog.*

echo ""
echo ">>> Removing mongodb journal logs..."
rm -rf /var/lib/mongodb/journal/*

echo ""
echo ">>> Displaying current disk usage after cleanup..."
df -h

# Display the top big files after cleanup
echo ""
echo ">>> Displaying top big files on disk..."
sudo find / -type f -exec du -h {} + | sort -rh | head -n 25

echo ""
echo ">>> System cleanup complete."
