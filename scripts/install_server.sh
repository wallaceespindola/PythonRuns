#!/bin/bash

#================================================================
# FastAPI Skipy Backend - Ubuntu VPS Installation Script
#================================================================
# This script automates the complete setup of the Skipy backend
# on Ubuntu 20.04+ VPS, including all dependencies, services,
# and production configurations.
#
# Author: Wallace Espindola (Skipy Team)
# Date: September 2025
# Version: 1.0
#
# URLs:
# - FastAPI Backend: https://api.skipy.com.br
# - React Client App: https://client.skipy.com.br
# - React Manager App: https://manager.skipy.com.br
#
# IMPORTANT: Run this script as root or with sudo privileges
# Usage: chmod +x install_server.sh && sudo ./install_server.sh
#================================================================

set -e  # Exit on any error

#================================================================
# SCRIPT CONFIGURATION
#================================================================

# Color codes for better output visibility
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Application configuration
APP_NAME="skipy"
APP_USER="skipy"
APP_GROUP="skipy"
APP_HOME="/home/$APP_USER"
APP_DIR="$APP_HOME/fast-api-skipy"
PYTHON_VERSION="3.11"
NODE_VERSION="18"
MONGODB_VERSION="7.0"

# Default configuration - can be overridden by user input
DEFAULT_DOMAIN="api.skipy.com.br"
DEFAULT_EMAIL="info@skipy.io"
DEFAULT_SERVER_IP="72.60.141.252"

# Runtime variables (populated during execution)
DOMAIN=""
EMAIL=""
SERVER_IP=""

# Installation progress tracking
TOTAL_STEPS=15
CURRENT_STEP=0

#================================================================
# UTILITY FUNCTIONS
#================================================================

# Progress tracking function
step() {
    CURRENT_STEP=$((CURRENT_STEP + 1))
    echo -e "${PURPLE}[STEP $CURRENT_STEP/$TOTAL_STEPS]${NC} ${CYAN}$1${NC}"
    echo "================================================================"
}

# Success logging function
log() {
    echo -e "${GREEN}✓ [$(date +'%H:%M:%S')] $1${NC}"
}

# Warning logging function
warn() {
    echo -e "${YELLOW}⚠ [WARNING] $1${NC}"
}

# Error logging function
error() {
    echo -e "${RED}✗ [ERROR] $1${NC}"
    exit 1
}

# Information logging function
info() {
    echo -e "${BLUE}ℹ [INFO] $1${NC}"
}

# Task completion logging
task_complete() {
    echo -e "${GREEN}✅ COMPLETED: $1${NC}"
    echo ""
}

#================================================================
# VALIDATION FUNCTIONS
#================================================================

# Check if running as root
check_root() {
    step "Validating System Permissions"

    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root or with sudo privileges"
    fi

    log "Running as root - permissions validated"
    log "Current user: $(whoami)"
    log "System: $(uname -a | cut -d' ' -f1-3)"
    task_complete "System validation"
}

#================================================================
# USER INPUT COLLECTION
#================================================================

# Collect configuration from user
collect_input() {
    step "Collecting Installation Configuration"

    echo -e "\n${BLUE}=== Skipy Backend Installation Configuration ===${NC}"
    echo "Please provide the following information (press Enter for defaults):"
    echo ""

    # Domain configuration
    echo -e "${CYAN}Domain Configuration:${NC}"
    read -p "Enter your domain name [$DEFAULT_DOMAIN]: " DOMAIN
    if [[ -z "$DOMAIN" ]]; then
        DOMAIN="$DEFAULT_DOMAIN"
        log "Using default domain: $DOMAIN"
    else
        log "Domain set to: $DOMAIN"
    fi

    # Email configuration for SSL
    if [[ "$DOMAIN" != "localhost" ]]; then
        echo -e "\n${CYAN}SSL Certificate Email:${NC}"
        read -p "Enter your email for SSL certificate [$DEFAULT_EMAIL]: " EMAIL
        if [[ -z "$EMAIL" ]]; then
            EMAIL="$DEFAULT_EMAIL"
            log "Using default email: $EMAIL"
        else
            log "Email set to: $EMAIL"
        fi
    else
        EMAIL=""
        warn "Localhost domain detected - SSL certificate will be skipped"
    fi

    # Server IP configuration
    echo -e "\n${CYAN}Server IP Configuration:${NC}"
    read -p "Enter your server IP address [$DEFAULT_SERVER_IP]: " SERVER_IP
    if [[ -z "$SERVER_IP" ]]; then
        SERVER_IP="$DEFAULT_SERVER_IP"
        log "Using default server IP: $SERVER_IP"
    else
        log "Server IP set to: $SERVER_IP"
    fi

    # Display configuration summary
    echo -e "\n${YELLOW}=== Installation Summary ===${NC}"
    echo "Domain: $DOMAIN"
    echo "Email: $EMAIL"
    echo "Server IP: $SERVER_IP"
    echo "Application user: $APP_USER"
    echo "Installation directory: $APP_DIR"
    echo "Python version: $PYTHON_VERSION"
    echo "MongoDB version: $MONGODB_VERSION"
    echo ""

    # Final confirmation
    read -p "Continue with installation? [Y/n]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        error "Installation cancelled by user"
    fi

    log "Configuration confirmed - proceeding with installation"
    task_complete "Configuration collection"
}

#================================================================
# SYSTEM PREPARATION
#================================================================

# Update system packages and install essentials
update_system() {
    step "Updating System Packages"

    log "Updating package lists..."
    apt update

    log "Upgrading existing packages..."
    apt upgrade -y

    log "Installing essential system packages..."
    apt install -y \
        curl \
        wget \
        git \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release \
        htop \
        tree \
        vim \
        nano \
        ufw \
        fail2ban \
        logrotate

    log "Essential packages installed successfully"
    log "System updated and prepared for installation"
    task_complete "System package updates"
}

#================================================================
# PYTHON INSTALLATION
#================================================================

# Install Python and development tools
install_python() {
    step "Installing Python $PYTHON_VERSION and Development Tools"

    # Fix common apt issues first
    log "Fixing potential apt_pkg and command-not-found issues..."

    # Temporarily disable problematic command-not-found hook
    if [[ -f "/etc/apt/apt.conf.d/50command-not-found" ]]; then
        mv /etc/apt/apt.conf.d/50command-not-found /etc/apt/apt.conf.d/50command-not-found.bak
        log "Temporarily disabled command-not-found hook"
    fi

    # Fix broken python3-apt if needed
    log "Attempting to fix python3-apt package..."
    apt update --fix-missing 2>/dev/null || true
    apt install -y --reinstall --fix-broken python3-apt python3-apt-dev 2>/dev/null || {
        warn "Could not reinstall python3-apt - continuing with alternative method"
    }

    # Disable problematic cnf-update-db script
    if [[ -f "/usr/lib/cnf-update-db" ]]; then
        chmod -x /usr/lib/cnf-update-db 2>/dev/null || true
        log "Disabled problematic cnf-update-db script"
    fi

    # Try deadsnakes PPA method first
    log "Attempting to install Python $PYTHON_VERSION from deadsnakes PPA..."

    if command -v add-apt-repository &> /dev/null && add-apt-repository --help &> /dev/null 2>&1; then
        export APT_LISTCHANGES_FRONTEND=none
        export DEBIAN_FRONTEND=noninteractive

        if add-apt-repository ppa:deadsnakes/ppa -y 2>/dev/null; then
            log "Successfully added deadsnakes PPA"

            apt update 2>/dev/null || {
                warn "apt update had warnings - continuing anyway"
            }

            log "Installing Python $PYTHON_VERSION and development packages..."
            if apt install -y \
                python$PYTHON_VERSION \
                python$PYTHON_VERSION-dev \
                python$PYTHON_VERSION-venv \
                python$PYTHON_VERSION-distutils \
                python3-pip \
                build-essential \
                libssl-dev \
                libffi-dev \
                libbz2-dev \
                libreadline-dev \
                libsqlite3-dev \
                libncurses5-dev \
                libncursesw5-dev \
                xz-utils \
                tk-dev \
                libxml2-dev \
                libxmlsec1-dev \
                liblzma-dev \
                2>/dev/null; then

                log "Python $PYTHON_VERSION installed successfully from PPA"

                # Set as default python3
                if command -v python$PYTHON_VERSION &> /dev/null; then
                    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python$PYTHON_VERSION 1
                    log "Set Python $PYTHON_VERSION as default python3"
                fi
            else
                warn "PPA installation failed - falling back to default repositories"
                install_default_python
            fi
        else
            warn "Could not add deadsnakes PPA - using default Python"
            install_default_python
        fi
    else
        warn "add-apt-repository not available - using default Python installation"
        install_default_python
    fi

    # Restore command-not-found hook
    if [[ -f "/etc/apt/apt.conf.d/50command-not-found.bak" ]]; then
        mv /etc/apt/apt.conf.d/50command-not-found.bak /etc/apt/apt.conf.d/50command-not-found
        log "Restored command-not-found hook"
    fi

    # Upgrade pip and essential Python packages
    log "Upgrading pip and essential Python packages..."
    python3 -m pip install --upgrade pip --break-system-packages 2>/dev/null || \
    python3 -m pip install --upgrade pip 2>/dev/null || {
        warn "Could not upgrade pip via python3 -m pip - trying alternative method"
        if command -v pip3 &> /dev/null; then
            pip3 install --upgrade pip 2>/dev/null || true
        fi
    }

    python3 -m pip install --upgrade setuptools wheel --break-system-packages 2>/dev/null || \
    python3 -m pip install --upgrade setuptools wheel 2>/dev/null || {
        warn "Could not upgrade setuptools and wheel - continuing anyway"
    }

    # Verify Python installation
    if python3 --version &> /dev/null; then
        INSTALLED_VERSION=$(python3 --version)
        log "Python installation verified: $INSTALLED_VERSION"
        log "Pip version: $(python3 -m pip --version | cut -d' ' -f1-2)"
    else
        error "Python installation failed - python3 command not available"
    fi

    task_complete "Python $PYTHON_VERSION installation"
}

# Fallback Python installation from default repositories
install_default_python() {
    log "Installing Python from default Ubuntu repositories..."

    DEBIAN_FRONTEND=noninteractive apt install -y \
        python3 \
        python3-dev \
        python3-venv \
        python3-pip \
        build-essential \
        libssl-dev \
        libffi-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        libncurses5-dev \
        libncursesw5-dev \
        xz-utils \
        tk-dev \
        libxml2-dev \
        libxmlsec1-dev \
        liblzma-dev \
        2>/dev/null || {
            error "Failed to install Python from default repositories"
        }

    INSTALLED_PYTHON_VERSION=$(python3 --version 2>/dev/null | cut -d' ' -f2 | cut -d'.' -f1,2)
    log "Installed Python version: $INSTALLED_PYTHON_VERSION"

    if [[ "$INSTALLED_PYTHON_VERSION" < "3.10" ]]; then
        warn "Python version is older than 3.10 - application may have compatibility issues"
        warn "Recommend upgrading to Python 3.10+ for best performance"
    else
        log "Python version is compatible with Skipy requirements"
    fi
}

#================================================================
# SHELL ENHANCEMENT
#================================================================

# Install Oh My Zsh with Jonathan theme
install_ohmyzsh() {
    step "Installing Oh My Zsh with Jonathan Theme"

    # Install Zsh shell
    if ! command -v zsh &> /dev/null; then
        log "Installing Zsh shell..."
        apt install -y zsh
        log "Zsh shell installed successfully"
    else
        log "Zsh shell already installed"
    fi

    # Install Oh My Zsh for root user
    log "Setting up Oh My Zsh for root user..."
    if [[ ! -d "/root/.oh-my-zsh" ]]; then
        log "Downloading and installing Oh My Zsh for root..."

        # Non-interactive installation
        RUNZSH=no CHSH=no sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" 2>/dev/null || {
            warn "Standard Oh My Zsh installation failed - trying manual installation"

            # Manual fallback
            if git clone https://github.com/ohmyzsh/ohmyzsh.git /root/.oh-my-zsh 2>/dev/null; then
                log "Manual Oh My Zsh installation successful for root"
            else
                warn "Could not install Oh My Zsh for root user"
                return 0
            fi
        }

        log "Creating Zsh configuration with Jonathan theme for root..."
        # Create .zshrc configuration with Jonathan theme and useful aliases
        cat > /root/.zshrc << 'EOF'
# Oh My Zsh configuration for Skipy server management
export ZSH="$HOME/.oh-my-zsh"

# Set Jonathan theme for clean, informative prompt
ZSH_THEME="jonathan"

# Useful plugins for server management
plugins=(git sudo history-substring-search colored-man-pages command-not-found)

# Load Oh My Zsh
source $ZSH/oh-my-zsh.sh

# Environment configuration
export LANG=en_US.UTF-8
export EDITOR='nano'

# Standard aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Skipy server management aliases
alias skipy-logs='journalctl -u skipy -f --no-pager'
alias skipy-status='systemctl status skipy'
alias skipy-restart='systemctl restart skipy'
alias skipy-reload='systemctl reload skipy'
alias skipy-stop='systemctl stop skipy'
alias skipy-start='systemctl start skipy'
alias nginx-logs='tail -f /var/log/nginx/error.log'
alias nginx-access='tail -f /var/log/nginx/access.log'
alias mongo-logs='journalctl -u mongod -f --no-pager'
alias mongo-status='systemctl status mongod'

# System monitoring aliases
alias monitor='watch -n 2 "systemctl status skipy mongod nginx --no-pager -l"'
alias ports='netstat -tulpn | grep LISTEN'
alias disk='df -h'
alias mem='free -h'

# History configuration for better command recall
HISTSIZE=10000
SAVEHIST=10000
setopt HIST_IGNORE_DUPS
setopt HIST_FIND_NO_DUPS
setopt HIST_IGNORE_SPACE
setopt SHARE_HISTORY
EOF

        log "Setting Zsh as default shell for root..."
        chsh -s $(which zsh) root 2>/dev/null || {
            warn "Could not change default shell for root user"
        }

        log "Oh My Zsh with Jonathan theme configured for root user"
    else
        log "Oh My Zsh already installed for root user"
    fi

    # Note: App user setup will be done after user creation
    log "Oh My Zsh setup for root user completed"
    task_complete "Oh My Zsh installation with Jonathan theme"
}

# Setup Oh My Zsh for application user (called after user creation)
setup_app_user_zsh() {
    if id "$APP_USER" &>/dev/null; then
        log "Setting up Oh My Zsh for $APP_USER user..."

        if [[ ! -d "$APP_HOME/.oh-my-zsh" ]]; then
            log "Installing Oh My Zsh for $APP_USER..."

            # Install for app user
            sudo -u "$APP_USER" sh -c 'RUNZSH=no CHSH=no sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"' 2>/dev/null || {
                warn "Standard installation failed for $APP_USER - trying manual setup"

                # Manual installation for app user
                sudo -u "$APP_USER" git clone https://github.com/ohmyzsh/ohmyzsh.git "$APP_HOME/.oh-my-zsh" 2>/dev/null || {
                    warn "Could not install Oh My Zsh for $APP_USER"
                    return 0
                }
            }

            log "Creating Zsh configuration for $APP_USER..."
            # Create .zshrc for app user
            sudo -u "$APP_USER" cat > "$APP_HOME/.zshrc" << 'EOF'
# Oh My Zsh configuration for Skipy application user
export ZSH="$HOME/.oh-my-zsh"

# Jonathan theme for consistent experience
ZSH_THEME="jonathan"

# Application-focused plugins
plugins=(git sudo history-substring-search colored-man-pages)

# Load Oh My Zsh
source $ZSH/oh-my-zsh.sh

# Environment configuration
export LANG=en_US.UTF-8
export EDITOR='nano'

# Standard aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'

# Application management aliases
alias app-logs='journalctl -u skipy -f --no-pager'
alias app-status='systemctl status skipy'
alias activate='source venv/bin/activate'
alias app-dir='cd /home/skipy/fast-api-skipy'
alias venv-activate='source /home/skipy/fast-api-skipy/venv/bin/activate'

# Development aliases
alias serve='cd /home/skipy/fast-api-skipy && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000'
alias test='cd /home/skipy/fast-api-skipy && source venv/bin/activate && python -m pytest'

# History configuration
HISTSIZE=10000
SAVEHIST=10000
setopt HIST_IGNORE_DUPS
setopt HIST_FIND_NO_DUPS
setopt HIST_IGNORE_SPACE
setopt SHARE_HISTORY
EOF

            # Set correct ownership
            chown "$APP_USER:$APP_GROUP" "$APP_HOME/.zshrc"

            log "Setting Zsh as default shell for $APP_USER..."
            chsh -s $(which zsh) "$APP_USER" 2>/dev/null || {
                warn "Could not change default shell for $APP_USER"
            }

            log "Oh My Zsh configured successfully for $APP_USER"
        else
            log "Oh My Zsh already installed for $APP_USER"
        fi
    fi
}

#================================================================
# DATABASE INSTALLATION
#================================================================

# Install and configure MongoDB
install_mongodb() {
    step "Installing MongoDB $MONGODB_VERSION Database"

    # Detect Ubuntu version for repository compatibility
    UBUNTU_CODENAME=$(lsb_release -cs)
    log "Detected Ubuntu codename: $UBUNTU_CODENAME"

    # Handle Ubuntu Noble (24.04) compatibility
    if [[ "$UBUNTU_CODENAME" == "noble" ]]; then
        MONGO_UBUNTU_VERSION="jammy"
        warn "Ubuntu Noble detected - using MongoDB repository for Jammy (22.04) compatibility"
    else
        MONGO_UBUNTU_VERSION="$UBUNTU_CODENAME"
    fi

    # Import MongoDB GPG key
    log "Adding MongoDB GPG key..."
    curl -fsSL https://www.mongodb.org/static/pgp/server-$MONGODB_VERSION.asc | \
        gpg -o /usr/share/keyrings/mongodb-server-$MONGODB_VERSION.gpg --dearmor
    log "MongoDB GPG key imported successfully"

    # Clean up existing repository files
    rm -f /etc/apt/sources.list.d/mongodb-org-*.list
    log "Cleaned up existing MongoDB repository files"

    # Add MongoDB repository
    log "Adding MongoDB repository for Ubuntu $MONGO_UBUNTU_VERSION..."
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-$MONGODB_VERSION.gpg ] \
        https://repo.mongodb.org/apt/ubuntu $MONGO_UBUNTU_VERSION/mongodb-org/$MONGODB_VERSION multiverse" | \
        tee /etc/apt/sources.list.d/mongodb-org-$MONGODB_VERSION.list
    log "MongoDB repository added successfully"

    # Update package lists
    log "Updating package lists with MongoDB repository..."
    apt update 2>/dev/null || {
        warn "apt update had warnings - continuing with installation"
    }

    # Try MongoDB installation with fallbacks
    log "Installing MongoDB packages..."
    if apt install -y mongodb-org 2>/dev/null; then
        log "MongoDB installed successfully from official repository"
        MONGODB_SERVICE="mongod"
    else
        warn "Official MongoDB installation failed - trying alternative methods"

        # Fallback 1: Ubuntu repository
        log "Attempting installation from Ubuntu repositories..."
        if apt install -y mongodb 2>/dev/null; then
            log "MongoDB installed from Ubuntu repositories"
            MONGODB_SERVICE="mongodb"
        else
            # Fallback 2: Snap installation
            warn "Standard repositories failed - trying snap installation"
            if command -v snap &> /dev/null; then
                if snap install mongodb --channel=6.0/stable 2>/dev/null; then
                    log "MongoDB installed successfully via snap"
                    MONGODB_SERVICE="snap.mongodb.mongod"
                else
                    error "All MongoDB installation methods failed - manual installation required"
                fi
            else
                error "Could not install MongoDB - snap not available"
            fi
        fi
    fi

    # Configure MongoDB
    log "Configuring MongoDB service..."
    configure_mongodb_service

    task_complete "MongoDB $MONGODB_VERSION installation and configuration"
}

# Configure MongoDB service and security
configure_mongodb_service() {
    log "Setting up MongoDB configuration files..."

    # Determine configuration paths based on installation method
    if [[ "$MONGODB_SERVICE" == "mongodb" ]]; then
        MONGO_CONFIG="/etc/mongodb.conf"
        MONGO_DATA_PATH="/var/lib/mongodb"
        MONGO_LOG_PATH="/var/log/mongodb/mongodb.log"
    else
        MONGO_CONFIG="/etc/mongod.conf"
        MONGO_DATA_PATH="/var/lib/mongodb"
        MONGO_LOG_PATH="/var/log/mongodb/mongod.log"
    fi

    log "Using configuration file: $MONGO_CONFIG"
    log "Data directory: $MONGO_DATA_PATH"
    log "Log file: $MONGO_LOG_PATH"

    # Create MongoDB data directory
    mkdir -p "$MONGO_DATA_PATH"
    chown mongodb:mongodb "$MONGO_DATA_PATH" 2>/dev/null || {
        log "Creating mongodb user..."
        useradd -r -s /bin/false -d "$MONGO_DATA_PATH" mongodb || true
        chown mongodb:mongodb "$MONGO_DATA_PATH"
    }
    log "MongoDB data directory created and configured"

    # Create log directory
    mkdir -p "$(dirname "$MONGO_LOG_PATH")"
    chown mongodb:mongodb "$(dirname "$MONGO_LOG_PATH")" 2>/dev/null || true
    log "MongoDB log directory created"

    # Create MongoDB configuration file
    log "Creating MongoDB configuration..."
    cat > "$MONGO_CONFIG" << EOF
# MongoDB configuration file for Skipy application

# Storage configuration
storage:
  dbPath: $MONGO_DATA_PATH
  journal:
    enabled: true

# Logging configuration
systemLog:
  destination: file
  logAppend: true
  path: $MONGO_LOG_PATH

# Network configuration
net:
  port: 27017
  bindIp: 127.0.0.1  # Secure: localhost only

# Process management
processManagement:
  timeZoneInfo: /usr/share/zoneinfo

# Security configuration
security:
  authorization: enabled  # Require authentication

# Performance monitoring
operationProfiling:
  slowOpThresholdMs: 100
EOF
    log "MongoDB configuration file created"

    # Start MongoDB service
    log "Starting MongoDB service: $MONGODB_SERVICE"
    systemctl daemon-reload
    systemctl enable "$MONGODB_SERVICE" 2>/dev/null || {
        warn "Could not enable $MONGODB_SERVICE service"
    }
    systemctl start "$MONGODB_SERVICE" 2>/dev/null || {
        warn "Standard service start failed - trying alternative methods"

        if [[ "$MONGODB_SERVICE" == "mongodb" ]]; then
            service mongodb start 2>/dev/null || {
                warn "Could not start MongoDB service"
            }
        fi
    }

    # Wait for MongoDB to initialize
    log "Waiting for MongoDB to initialize..."
    sleep 10

    # Verify MongoDB is running
    if systemctl is-active --quiet "$MONGODB_SERVICE" 2>/dev/null || \
       pgrep -f "mongod\|mongodb" > /dev/null; then
        log "MongoDB service is running successfully"
        setup_mongodb_users
    else
        warn "MongoDB service may not be running properly - attempting manual setup"
        manual_mongodb_setup
    fi
}

# Setup MongoDB database users and security
setup_mongodb_users() {
    log "Setting up MongoDB database users..."

    # Determine MongoDB client command
    MONGO_CMD=""
    if command -v mongosh &> /dev/null; then
        MONGO_CMD="mongosh"
        log "Using mongosh client"
    elif command -v mongo &> /dev/null; then
        MONGO_CMD="mongo"
        log "Using legacy mongo client"
    else
        warn "No MongoDB client found - skipping user creation"
        return 0
    fi

    # Generate secure passwords
    MONGO_ADMIN_PASSWORD=$(openssl rand -base64 32)
    MONGO_APP_PASSWORD=$(openssl rand -base64 32)
    log "Generated secure passwords for MongoDB users"

    # Create admin user
    log "Creating MongoDB admin user..."
    $MONGO_CMD admin --eval "
        try {
            db.createUser({
                user: 'admin',
                pwd: '$MONGO_ADMIN_PASSWORD',
                roles: [
                    { role: 'userAdminAnyDatabase', db: 'admin' },
                    { role: 'readWriteAnyDatabase', db: 'admin' },
                    { role: 'dbAdminAnyDatabase', db: 'admin' }
                ]
            });
            print('MongoDB admin user created successfully');
        } catch (e) {
            print('Admin user creation result: ' + e.message);
        }
    " 2>/dev/null || {
        warn "Could not create MongoDB admin user"
    }

    # Create application user
    log "Creating Skipy application database user..."
    $MONGO_CMD skipy_db --eval "
        try {
            db.createUser({
                user: 'skipy_user',
                pwd: '$MONGO_APP_PASSWORD',
                roles: [
                    { role: 'readWrite', db: 'skipy_db' }
                ]
            });
            print('Skipy application user created successfully');
        } catch (e) {
            print('Application user creation result: ' + e.message);
        }
    " 2>/dev/null || {
        warn "Could not create MongoDB application user"
    }

    # Store credentials securely for later use
    cat > /tmp/mongo_credentials << EOF
MONGO_ADMIN_PASSWORD=$MONGO_ADMIN_PASSWORD
MONGO_APP_PASSWORD=$MONGO_APP_PASSWORD
EOF
    chmod 600 /tmp/mongo_credentials
    log "MongoDB credentials stored securely for application configuration"

    log "MongoDB user setup completed successfully"
}

# Manual MongoDB setup fallback
manual_mongodb_setup() {
    if command -v mongod &> /dev/null; then
        log "Attempting manual MongoDB startup for initial setup..."
        mongod --fork --logpath /tmp/mongod-setup.log --dbpath "$MONGO_DATA_PATH" --bind_ip 127.0.0.1 2>/dev/null && {
            sleep 5
            setup_mongodb_users
            # Stop manual instance
            pkill -f "mongod.*fork" 2>/dev/null || true
            sleep 2
            # Try to start service again
            systemctl start "$MONGODB_SERVICE" 2>/dev/null || true
        } || {
            error "Could not start MongoDB for initial setup"
        }
    else
        error "MongoDB installation appears to have failed completely"
    fi
}

#================================================================
# WEB SERVER INSTALLATION
#================================================================

# Install and configure Nginx
install_nginx() {
    step "Installing and Configuring Nginx Web Server"

    log "Installing Nginx..."
    apt install -y nginx

    log "Removing default Nginx configuration..."
    rm -f /etc/nginx/sites-enabled/default

    # Create Nginx configuration for Skipy
    log "Creating Nginx configuration for Skipy..."
    cat > /etc/nginx/sites-available/$APP_NAME << EOF
# Skipy FastAPI Backend Configuration
# Rate limiting
limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone \$binary_remote_addr zone=auth:10m rate=5r/s;

# Upstream for load balancing (if needed in future)
upstream skipy_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name $DOMAIN;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # File upload size limit
    client_max_body_size 50M;

    # Rate limiting
    location /api/v1/auth/ {
        limit_req zone=auth burst=10 nodelay;
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }

    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://skipy_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files
    location /static/ {
        alias $APP_DIR/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # File uploads
    location /uploads/ {
        alias $APP_DIR/uploads/;
        expires 7d;
    }

    # API documentation (optional - remove in production)
    location /docs {
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }

    location /redoc {
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }

    # Health check
    location /health {
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }

    # All other requests to FastAPI
    location / {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }
}
EOF

    # Create proxy_params if it doesn't exist
    cat > /etc/nginx/proxy_params << EOF
proxy_set_header Host \$host;
proxy_set_header X-Real-IP \$remote_addr;
proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto \$scheme;
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
proxy_buffering off;
EOF

    # Enable site
    ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/

    # Test Nginx configuration
    nginx -t

    # Start and enable Nginx
    systemctl start nginx
    systemctl enable nginx
    log "Nginx installed and configured successfully"
    task_complete "Nginx installation and configuration"
}

#================================================================
# SSL CERTIFICATE INSTALLATION
#================================================================

# Install SSL certificate with Let's Encrypt
install_ssl() {
    if [[ "$DOMAIN" == "localhost" ]] || [[ -z "$EMAIL" ]]; then
        warn "Skipping SSL certificate installation (localhost or no email provided)"
        return 0
    fi

    step "Installing SSL Certificate for $DOMAIN"
    log "Using email: $EMAIL"

    # Check domain resolution first
    log "Checking domain resolution for $DOMAIN..."
    DOMAIN_IP=$(dig +short $DOMAIN 2>/dev/null | head -n1)
    SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || echo "$DEFAULT_SERVER_IP")

    if [[ -z "$DOMAIN_IP" ]]; then
        warn "Domain $DOMAIN does not resolve to any IP address (NXDOMAIN)"
        warn "DNS Configuration Required:"
        warn "1. Create an A record for $DOMAIN pointing to: $SERVER_IP"
        warn "2. Wait for DNS propagation (5-60 minutes)"
        warn "3. Then run SSL installation manually:"
        warn "   sudo certbot --nginx -d $DOMAIN --email $EMAIL"
        warn ""
        warn "Continuing installation without SSL certificate..."
        warn "Your API will be available at: http://$DOMAIN"
        return 1
    elif [[ -n "$SERVER_IP" && "$DOMAIN_IP" != "$SERVER_IP" ]]; then
        warn "Domain $DOMAIN resolves to $DOMAIN_IP but server IP is $SERVER_IP"
        warn "DNS Configuration Issue:"
        warn "1. Update A record for $DOMAIN to point to: $SERVER_IP"
        warn "2. Wait for DNS propagation (5-60 minutes)"
        warn "3. Then run SSL installation manually:"
        warn "   sudo certbot --nginx -d $DOMAIN --email $EMAIL"
        warn ""
        warn "Continuing installation without SSL certificate..."
        return 1
    else
        log "Domain resolution looks correct ($DOMAIN -> $SERVER_IP)"
    fi

    # Fix Python cryptography issues first
    log "Fixing potential Python cryptography module issues..."
    apt install -y python3-cffi python3-cffi-backend libffi-dev build-essential python3-dev 2>/dev/null || {
        warn "Could not install all cryptography dependencies"
    }

    # Remove potentially corrupted packages and reinstall
    apt remove -y python3-cryptography python3-pyopenssl --purge 2>/dev/null || true
    apt install -y python3-cryptography python3-pyopenssl 2>/dev/null || {
        warn "Could not reinstall cryptography packages via apt"
    }

    # Try multiple Certbot installation methods
    CERTBOT_INSTALLED=false

    # Method 1: Try snap installation (most reliable)
    if command -v snap &> /dev/null; then
        log "Installing Certbot via snap (recommended method)..."

        # Remove any existing certbot installations
        apt remove -y certbot python3-certbot-nginx --purge 2>/dev/null || true

        # Install certbot via snap
        if snap install --classic certbot 2>/dev/null; then
            # Create symlink
            ln -sf /snap/bin/certbot /usr/bin/certbot

            # Verify installation
            if certbot --version &>/dev/null; then
                log "Certbot installed successfully via snap"
                CERTBOT_INSTALLED=true
            fi
        fi
    fi

    # Method 2: Virtual environment installation
    if [[ "$CERTBOT_INSTALLED" == "false" ]]; then
        log "Installing Certbot in isolated virtual environment..."

        # Create virtual environment
        if python3 -m venv /opt/certbot-venv 2>/dev/null; then
            /opt/certbot-venv/bin/pip install --upgrade pip setuptools wheel 2>/dev/null
            if /opt/certbot-venv/bin/pip install certbot certbot-nginx 2>/dev/null; then
                # Create wrapper script
                cat > /usr/local/bin/certbot << 'EOF'
#!/bin/bash
/opt/certbot-venv/bin/certbot "$@"
EOF
                chmod +x /usr/local/bin/certbot

                # Verify installation
                if /usr/local/bin/certbot --version &>/dev/null; then
                    log "Certbot installed successfully in virtual environment"
                    CERTBOT_INSTALLED=true
                fi
            fi
        fi
    fi

    # Method 3: Fallback to apt installation with fixes
    if [[ "$CERTBOT_INSTALLED" == "false" ]]; then
        log "Attempting apt installation with cryptography fixes..."

        # Try to fix cryptography with pip
        python3 -m pip install --upgrade --force-reinstall cryptography pyopenssl cffi --break-system-packages 2>/dev/null || {
            warn "Could not reinstall cryptography via pip"
        }

        # Install certbot via apt
        if apt install -y certbot python3-certbot-nginx 2>/dev/null; then
            if certbot --version &>/dev/null; then
                log "Certbot installed successfully via apt"
                CERTBOT_INSTALLED=true
            fi
        fi
    fi

    # Check if any method succeeded
    if [[ "$CERTBOT_INSTALLED" == "false" ]]; then
        warn "Could not install Certbot using any method."
        warn "You can manually install SSL later using: sudo snap install --classic certbot"
        return 1
    fi

    # Try to obtain SSL certificate
    log "Obtaining SSL certificate from Let's Encrypt..."

    # Method 1: Try nginx plugin first
    if certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email $EMAIL --redirect 2>/dev/null; then
        log "SSL certificate obtained successfully with nginx plugin!"

        # Test auto-renewal
        if certbot renew --dry-run 2>/dev/null; then
            log "Auto-renewal test passed"
        else
            warn "Auto-renewal test failed, but certificate is installed"
        fi
        return 0
    fi

    # Method 2: Try webroot method if nginx method failed
    warn "Nginx plugin failed. Trying webroot method..."

    # Create webroot directory
    mkdir -p /var/www/html/.well-known/acme-challenge
    chown -R www-data:www-data /var/www/html/.well-known 2>/dev/null || true

    # Create temporary nginx config for challenge
    cat > /etc/nginx/sites-available/temp-ssl << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
        allow all;
    }

    location / {
        return 200 'SSL Challenge Server - Skipy';
        add_header Content-Type text/plain;
    }
}
EOF

    # Enable temporary config
    rm -f /etc/nginx/sites-enabled/$APP_NAME
    ln -sf /etc/nginx/sites-available/temp-ssl /etc/nginx/sites-enabled/temp-ssl
    nginx -t && nginx -s reload 2>/dev/null

    # Try webroot method
    if certbot certonly --webroot -w /var/www/html -d $DOMAIN --non-interactive --agree-tos --email $EMAIL 2>/dev/null; then
        log "SSL certificate obtained using webroot method!"

        # Remove temporary config
        rm -f /etc/nginx/sites-enabled/temp-ssl

        # Update nginx config with SSL
        update_nginx_ssl_config

        # Test auto-renewal
        if certbot renew --dry-run 2>/dev/null; then
            log "Auto-renewal test passed"
        else
            warn "Auto-renewal test failed, but certificate is installed"
        fi

        return 0
    else
        # Clean up temporary config
        rm -f /etc/nginx/sites-enabled/temp-ssl
        # Restore original nginx config
        ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/$APP_NAME
        nginx -s reload 2>/dev/null

        warn "SSL certificate installation failed due to DNS issues."
        warn "Please configure DNS first, then run SSL installation manually:"
        warn "  sudo certbot --nginx -d $DOMAIN --email $EMAIL"
        warn ""
        warn "Continuing with HTTP-only configuration..."

        return 1
    fi
}

# Update Nginx configuration for SSL
update_nginx_ssl_config() {
    log "Updating Nginx configuration for SSL..."

    # Check if SSL certificates exist
    if [[ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" && -f "/etc/letsencrypt/live/$DOMAIN/privkey.pem" ]]; then

        # Create enhanced SSL configuration
        cat > /etc/nginx/sites-available/$APP_NAME << EOF
# Skipy FastAPI Backend Configuration with SSL
# Rate limiting
limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone \$binary_remote_addr zone=auth:10m rate=5r/s;

# Upstream backend
upstream skipy_backend {
    server 127.0.0.1:8000;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$server_name\$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name $DOMAIN;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # File upload size limit
    client_max_body_size 50M;

    # Rate limiting for authentication endpoints
    location /api/v1/auth/ {
        limit_req zone=auth burst=10 nodelay;
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }

    # API endpoints with rate limiting
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://skipy_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files
    location /static/ {
        alias $APP_DIR/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # File uploads
    location /uploads/ {
        alias $APP_DIR/uploads/;
        expires 7d;
    }

    # API documentation (consider removing in production)
    location /docs {
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }

    location /redoc {
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }

    # Health check
    location /health {
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }

    # All other requests to FastAPI
    location / {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://skipy_backend;
        include /etc/nginx/proxy_params;
    }
}
EOF

        # Enable the new configuration
        ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/$APP_NAME

        # Test and reload nginx
        if nginx -t 2>/dev/null; then
            nginx -s reload
            log "Nginx configuration updated successfully with SSL"
        else
            warn "Nginx configuration test failed, keeping original configuration"
        fi
    else
        warn "SSL certificates not found, keeping HTTP configuration"
    fi
}

#================================================================
# APPLICATION SETUP
#================================================================

# Create application user and directories
create_app_user() {
    step "Creating Application User and Directories"

    log "Creating system user and group for Skipy application..."
    if ! id "$APP_USER" &>/dev/null; then
        useradd -m -s /bin/bash -G sudo $APP_USER
        log "Created user: $APP_USER"
    else
        warn "User $APP_USER already exists - skipping user creation"
    fi

    # Create necessary directories
    log "Creating necessary directories for application..."
    mkdir -p $APP_DIR
    mkdir -p $APP_HOME/logs
    mkdir -p $APP_HOME/backups
    mkdir -p $APP_DIR/uploads/products
    mkdir -p $APP_DIR/app/static

    # Set ownership
    log "Setting ownership for application directories..."
    chown -R $APP_USER:$APP_GROUP $APP_HOME
    log "Application user and directories setup completed"
    task_complete "Application user and directory creation"
}

# Clone and setup application
setup_application() {
    step "Cloning and Setting Up Skipy Application"

    log "Switching to app user for application setup..."
    sudo -u $APP_USER bash << EOF
set -e

# Clone repository if it doesn't exist
if [[ ! -d "$APP_DIR/.git" ]]; then
    cd $APP_HOME
    git clone https://github.com/your-username/fast-api-skipy.git || {
        echo "Failed to clone repository. Please update the repository URL."
        echo "Creating directory structure manually..."
        mkdir -p $APP_DIR
        cd $APP_DIR
        git init
    }
else
    cd $APP_DIR
    git pull origin main || echo "Could not pull latest changes"
fi

cd $APP_DIR

# Create virtual environment
if [[ ! -d "venv" ]]; then
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install Python dependencies
if [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Installing basic dependencies..."
    pip install fastapi uvicorn gunicorn motor pymongo pydantic python-jose passlib bcrypt python-multipart email-validator httpx stripe python-dotenv websockets aiohttp
fi

# Install additional production dependencies
pip install gunicorn[gevent] supervisor psutil
EOF

    log "Skipy application setup completed"
    task_complete "Skipy application cloning and setup"
}

# Create environment configuration
create_env_config() {
    step "Creating Environment Configuration"

    log "Generating secure keys for JWT and WebSocket..."
    JWT_SECRET=$(openssl rand -base64 64)
    WEBSOCKET_SECRET=$(openssl rand -base64 32)

    # Load MongoDB password
    if [[ -f "/tmp/mongo_credentials" ]]; then
        source /tmp/mongo_credentials
        rm -f /tmp/mongo_credentials
    else
        MONGO_APP_PASSWORD="your_mongo_password_here"
    fi

    # Create .env file
    log "Creating .env configuration file for Skipy..."
    sudo -u $APP_USER tee $APP_DIR/.env > /dev/null << EOF
# MongoDB
MONGO_URI=mongodb://skipy_user:$MONGO_APP_PASSWORD@localhost:27017/skipy_db
MONGO_DB=skipy_db

# JWT Auth
JWT_SECRET_KEY=$JWT_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# WebSocket
WEBSOCKET_SECRET_KEY=$WEBSOCKET_SECRET

# CORS origins - Skipy ecosystem domains
BACKEND_CORS_ORIGINS=https://api.skipy.com.br,https://client.skipy.com.br,https://manager.skipy.com.br,https://skipy.com.br,https://www.skipy.com.br,http://localhost:3000,http://localhost:3001,http://localhost:8080

# Base URL
BASE_URL=https://$DOMAIN

# Environment
ENVIRONMENT=production

# Image APIs (add your keys)
UNSPLASH_API_KEY=
PEXELS_API_KEY=
PIXABAY_API_KEY=

# Stripe (add your keys)
STRIPE_ENABLED=false
STRIPE_API_KEY=
STRIPE_PUBLIC_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_CONNECT_CLIENT_ID=
STRIPE_CONNECT_RETURN_URL=https://$DOMAIN/api/v1/payments/connect/return
STRIPE_PLATFORM_ACCOUNT=
STRIPE_APPLICATION_FEE_PERCENT=10.0

# Email / Brevo (add your keys)
USE_EMAIL_API=false
BREVO_API_KEY=
EMAILS_ENABLED=false
EMAILS_FROM_EMAIL=noreply@skipy.io
EMAILS_FROM_NAME=Skipy

# SMTP fallback
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=

# SMS (Bird.com) - add your keys
BIRD_API_KEY=
BIRD_API_URL=https://api.bird.com
BIRD_WORKSPACE_ID=
BIRD_CHANNEL_ID=
BIRD_SENDER_ID=SkipyApp

# Notifications
ADMIN_EMAIL=admin@skipy.io
RECIPIENT_EMAIL=orders@skipy.io
RECIPIENT_PHONE=+1234567890
EOF

    # Set proper permissions
    chown $APP_USER:$APP_GROUP $APP_DIR/.env
    chmod 600 $APP_DIR/.env

    log ".env configuration file created at $APP_DIR/.env"
    warn "Please update the .env file with your actual API keys and credentials!"
    task_complete "Environment configuration creation"
}

# Initialize database
init_database() {
    step "Initializing Database and Creating Indexes"

    log "Switching to app user for database initialization..."
    sudo -u $APP_USER bash << EOF
cd $APP_DIR
source venv/bin/activate

# Add current directory to Python path
export PYTHONPATH=\$PWD:\$PYTHONPATH

# Run database initialization if script exists
if [[ -f "scripts/create_indexes.py" ]]; then
    python scripts/create_indexes.py
else
    echo "Database initialization script not found. Creating basic indexes..."
    python -c "
import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

async def create_basic_indexes():
    try:
        # Import MongoDB connection
        from app.db.mongodb import db, connect_to_mongo

        # Connect to MongoDB
        await connect_to_mongo()

        # Create basic indexes
        print('Creating basic indexes for collections...')

        # Users collection indexes
        await db.db.users.create_index('email', unique=True)
        await db.db.users.create_index('created_at')
        print('✓ Users indexes created')

        # Stores collection indexes
        await db.db.stores.create_index('slug', unique=True)
        await db.db.stores.create_index('owner_id')
        await db.db.stores.create_index('created_at')
        print('✓ Stores indexes created')

        # Products collection indexes
        await db.db.products.create_index('store_id')
        await db.db.products.create_index('name')
        await db.db.products.create_index('status')
        await db.db.products.create_index('created_at')
        print('✓ Products indexes created')

        # Orders collection indexes
        await db.db.orders.create_index('store_id')
        await db.db.orders.create_index('customer.email')
        await db.db.orders.create_index('status')
        await db.db.orders.create_index('created_at')
        print('✓ Orders indexes created')

        # Categories collection indexes
        await db.db.categories.create_index('store_id')
        await db.db.categories.create_index('slug')
        print('✓ Categories indexes created')

        print('Database indexes created successfully')

    except ImportError as e:
        print(f'Import error - app modules not found: {e}')
        print('This is normal if app files are not present yet.')
        print('Database indexes will be created when the app starts.')
    except Exception as e:
        print(f'Database initialization failed: {e}')
        print('Database indexes will be created when the app starts.')

# Run the initialization
asyncio.run(create_basic_indexes())
"
fi
EOF

    log "Database initialization completed"
    task_complete "Database initialization and index creation"
}

# Create systemd service
create_systemd_service() {
    step "Creating Systemd Service for Skipy"

    log "Creating systemd service file..."
    cat > /etc/systemd/system/$APP_NAME.service << EOF
[Unit]
Description=Skipy FastAPI Backend
After=network.target mongod.service
Requires=mongod.service

[Service]
Type=exec
User=$APP_USER
Group=$APP_GROUP
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/gunicorn app.main:app \\
    --workers 4 \\
    --worker-class uvicorn.workers.UvicornWorker \\
    --bind 127.0.0.1:8000 \\
    --timeout 120 \\
    --keep-alive 2 \\
    --max-requests 1000 \\
    --max-requests-jitter 100 \\
    --access-logfile $APP_HOME/logs/access.log \\
    --error-logfile $APP_HOME/logs/error.log \\
    --log-level info
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$APP_HOME

[Install]
WantedBy=multi-user.target
EOF

    log "Enabling and starting Skipy service..."
    systemctl daemon-reload
    systemctl enable $APP_NAME
    systemctl start $APP_NAME

    log "Systemd service for Skipy created and started"
    task_complete "Systemd service creation"
}

# Configure firewall
configure_firewall() {
    step "Configuring Firewall"

    log "Enabling UFW firewall..."
    ufw --force enable

    log "Allowing SSH through firewall..."
    ufw allow OpenSSH

    log "Allowing HTTP and HTTPS through firewall..."
    ufw allow 'Nginx Full'

    log "Firewall configuration completed"
    task_complete "Firewall configuration"
}

# Setup log rotation
setup_log_rotation() {
    step "Setting Up Log Rotation"

    log "Creating logrotate configuration for Skipy..."
    cat > /etc/logrotate.d/$APP_NAME << EOF
$APP_HOME/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $APP_USER $APP_GROUP
    postrotate
        systemctl reload $APP_NAME
    endscript
}
EOF

    log "Log rotation configuration created"
    task_complete "Log rotation setup"
}

# Create backup script
create_backup_script() {
    step "Creating Backup Script"

    log "Creating backup script for MongoDB and application files..."
    cat > $APP_HOME/backup.sh << 'EOF'
#!/bin/bash
# Skipy Backup Script

BACKUP_DIR="/home/skipy/backups"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/home/skipy/fast-api-skipy"

# Create backup directory
mkdir -p $BACKUP_DIR

echo "Starting backup: $DATE"

# Backup MongoDB
echo "Backing up MongoDB..."
mongodump --host localhost --port 27017 --db skipy_db --out $BACKUP_DIR/mongo_$DATE

# Backup application files (excluding venv and cache)
echo "Backing up application files..."
tar -czf $BACKUP_DIR/app_$DATE.tar.gz \
    $APP_DIR \
    --exclude=venv \
    --exclude=__pycache__ \
    --exclude=.git \
    --exclude=node_modules \
    --exclude=*.pyc

# Backup environment and config files
echo "Backing up configuration..."
cp $APP_DIR/.env $BACKUP_DIR/env_$DATE.backup

# Clean old backups (keep last 7 days)
echo "Cleaning old backups..."
find $BACKUP_DIR -type f -mtime +7 -delete
find $BACKUP_DIR -type d -empty -delete

echo "Backup completed: $DATE"
echo "Backup location: $BACKUP_DIR"
EOF

    # Make executable
    chmod +x $APP_HOME/backup.sh
    chown $APP_USER:$APP_GROUP $APP_HOME/backup.sh

    # Add to crontab for daily backups at 2 AM
    sudo -u $APP_USER bash -c "(crontab -l 2>/dev/null; echo '0 2 * * * /home/skipy/backup.sh >> /home/skipy/logs/backup.log 2>&1') | crontab -"

    log "Backup script created and scheduled"
    task_complete "Backup script creation"
}

# Create monitoring script
create_monitoring_script() {
    step "Creating Monitoring Script"

    log "Creating system monitoring script..."
    cat > $APP_HOME/monitor.sh << 'EOF'
#!/bin/bash
# Skipy Monitoring Script

APP_NAME="skipy"
APP_URL="http://localhost:8000/health"

echo "=== Skipy System Status ==="
echo "Date: $(date)"
echo ""

# Check system resources
echo "=== System Resources ==="
echo "Memory Usage:"
free -h
echo ""
echo "Disk Usage:"
df -h / /home
echo ""
echo "CPU Load:"
uptime
echo ""

# Check services
echo "=== Service Status ==="
services=("mongod" "nginx" "$APP_NAME")
for service in "${services[@]}"; do
    if systemctl is-active --quiet $service; then
        echo "✅ $service: RUNNING"
    else
        echo "❌ $service: STOPPED"
    fi
done
echo ""

# Check application health
echo "=== Application Health ==="
if curl -s $APP_URL > /dev/null; then
    echo "✅ Application: HEALTHY"
else
    echo "❌ Application: UNHEALTHY"
fi
echo ""

# Check logs for errors
echo "=== Recent Errors ==="
echo "Application errors (last 10):"
tail -n 10 /home/skipy/logs/error.log 2>/dev/null || echo "No error log found"
echo ""

echo "System errors (last 5):"
journalctl -u $APP_NAME --no-pager -n 5 --since "1 hour ago" | grep -i error || echo "No recent errors"
EOF

    chmod +x $APP_HOME/monitor.sh
    chown $APP_USER:$APP_GROUP $APP_HOME/monitor.sh

    log "Monitoring script created"
    task_complete "Monitoring script creation"
}

# Start services
start_services() {
    step "Starting Services"

    log "Starting MongoDB service..."
    systemctl start mongod

    log "Starting Skipy application service..."
    systemctl start $APP_NAME

    log "Restarting Nginx to apply changes..."
    systemctl restart nginx

    # Check service status
    sleep 5

    services=("mongod" "nginx" "$APP_NAME")
    for service in "${services[@]}"; do
        if systemctl is-active --quiet $service; then
            info "✅ $service is running"
        else
            error "❌ $service failed to start"
        fi
    done

    log "All services started successfully"
    task_complete "Service start"
}

# Display completion information
show_completion_info() {
    log "Installation completed successfully!"

    echo -e "\n${GREEN}=== Installation Summary ===${NC}"
    echo "✅ System updated and secured"
    echo "✅ Python $PYTHON_VERSION installed"
    echo "✅ MongoDB $MONGODB_VERSION installed and configured"
    echo "✅ Nginx installed and configured"

    # Check if SSL was actually installed
    if [[ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]]; then
        echo "✅ SSL certificate installed and configured"
        SSL_INSTALLED=true
    else
        echo "⚠️  SSL certificate not installed (DNS configuration needed)"
        SSL_INSTALLED=false
    fi

    echo "✅ Application user '$APP_USER' created"
    echo "✅ Skipy application deployed"
    echo "✅ Systemd service created"
    echo "✅ Firewall configured"
    echo "✅ Log rotation configured"
    echo "✅ Backup system configured"

    echo -e "\n${YELLOW}=== Important Information ===${NC}"
    echo "🏠 Application directory: $APP_DIR"
    echo "👤 Application user: $APP_USER"
    echo "🌐 Domain: $DOMAIN"
    echo "📝 Environment file: $APP_DIR/.env"
    echo "📋 Logs directory: $APP_HOME/logs"
    echo "💾 Backups directory: $APP_HOME/backups"

    # Show different next steps based on SSL status
    if [[ "$SSL_INSTALLED" == "false" && "$DOMAIN" != "localhost" ]]; then
        echo -e "\n${RED}=== DNS Configuration Required ===${NC}"
        SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null)
        echo "To enable SSL certificate, configure DNS:"
        echo "1. Create an A record for $DOMAIN pointing to: $SERVER_IP"
        echo "2. Wait for DNS propagation (5-60 minutes)"
        echo "3. Run SSL installation manually:"
        echo "   sudo certbot --nginx -d $DOMAIN --email $EMAIL"
        echo "4. Restart Nginx: sudo systemctl reload nginx"
    fi

    echo -e "\n${BLUE}=== Next Steps ===${NC}"
    echo "1. Update environment variables in: $APP_DIR/.env"
    echo "   - Add your Stripe API keys"
    echo "   - Add your email service credentials"
    echo "   - Add your SMS service credentials"
    echo "   - Update notification emails/phones"

    echo -e "\n2. Restart the application after updating .env:"
    echo "   sudo systemctl restart $APP_NAME"

    echo -e "\n3. Test your installation:"
    if [[ "$SSL_INSTALLED" == "true" ]]; then
        echo "   curl https://$DOMAIN/health"
        echo "   curl https://$DOMAIN/api/v1/docs"
    else
        echo "   curl http://$DOMAIN/health"
        echo "   curl http://$DOMAIN/api/v1/docs"
    fi

    echo -e "\n${BLUE}=== Useful Commands ===${NC}"
    echo "📊 Check status:     sudo $APP_HOME/monitor.sh"
    echo "📋 View logs:        sudo journalctl -u $APP_NAME -f"
    echo "🔄 Restart app:      sudo systemctl restart $APP_NAME"
    echo "🔧 Update app:       cd $APP_DIR && git pull && sudo systemctl restart $APP_NAME"
    echo "💾 Manual backup:    sudo -u $APP_USER $APP_HOME/backup.sh"

    # Show appropriate URL based on SSL status
    if [[ "$SSL_INSTALLED" == "true" ]]; then
        echo -e "\n🌐 Your API is available at: https://$DOMAIN"
        echo "📖 API Documentation: https://$DOMAIN/api/v1/docs"
    else
        if [[ "$DOMAIN" != "localhost" ]]; then
            echo -e "\n🌐 Your API is currently available at: http://$DOMAIN"
            echo "📖 API Documentation: http://$DOMAIN/api/v1/docs"
            echo "🔒 After DNS configuration, it will be available at: https://$DOMAIN"
        else
            echo -e "\n🌐 Your API is available at: http://localhost"
            echo "📖 API Documentation: http://localhost/api/v1/docs"
        fi
    fi

    echo -e "\n${GREEN}Installation completed! 🎉${NC}"

    if [[ "$SSL_INSTALLED" == "false" && "$DOMAIN" != "localhost" ]]; then
        echo -e "\n${YELLOW}Note: Configure DNS and run SSL setup to enable HTTPS${NC}"
    fi
}

# Main installation function
main() {
    echo -e "${BLUE}"
    echo "================================================================"
    echo "         FastAPI Skipy Backend - Ubuntu VPS Installer"
    echo "         Complete Production Setup with Enhanced Shell"
    echo "================================================================"
    echo -e "${NC}"
    echo "This script will install and configure:"
    echo "• Python $PYTHON_VERSION with development tools"
    echo "• MongoDB $MONGODB_VERSION database"
    echo "• Nginx web server with SSL support"
    echo "• Oh My Zsh with Jonathan theme"
    echo "• Skipy FastAPI application"
    echo "• Production services and monitoring"
    echo ""

    check_root
    collect_input

    log "Starting comprehensive installation process..."
    log "Total steps to complete: $TOTAL_STEPS"
    echo ""

    # System preparation
    update_system
    install_python
    install_ohmyzsh

    # Database and web server
    install_mongodb
    install_nginx

    # Application setup
    create_app_user

    # Setup Oh My Zsh for application user after user creation
    log "Setting up Oh My Zsh for application user..."
    setup_app_user_zsh

    setup_application
    create_env_config
    init_database

    # Service configuration
    create_systemd_service
    configure_firewall
    setup_log_rotation

    # Operational tools
    create_backup_script
    create_monitoring_script

    # SSL and final service startup
    install_ssl  # This must come after nginx is configured
    start_services

    # Final summary and instructions
    show_completion_info

    echo -e "\n${GREEN}🎉 Installation process completed successfully!${NC}"
    echo -e "${CYAN}Skipy is now ready for production use.${NC}"
}

# Run main function
main "$@"
