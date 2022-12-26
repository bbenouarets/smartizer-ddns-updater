#!/bin/bash
mkdir -p /etc/smartizer/{ddns,analytics,log}
mkdir -p /var/log/smartizer/{ddns,analytics,log}

PREFIX="DDNS"
DIR="/etc/smartizer/ddns"
BINARY="$DIR/ddns"
LINK="/usr/bin/ddns"
REPO="https://github.com/bbenouarets/smartizer-ddns-updater/archive/main.zip"

function log() {
  local type=$1
  local message=$2
  local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  type=$(echo "$type" | tr "[:lower:]" "[:upper:]")
  # Check if the type is "error"
  if [ "$type" = "error" ]; then
    # Write the log message to the errors.log file in the /var/log/smartizer directory
    # Precede the message with "ERROR"
    echo "$PREFIX: $timestamp - [$type] $message" >> /var/log/smartizer/errors.log
    exit 1
  else
    # Write the log message to the output.log file in the /var/log/smartizer directory
    echo "$PREFIX: $timestamp - [$type] $message" >> /var/log/smartizer/output.log
  fi
  echo "$message"
}

function download() {
  log "info" "Downloading repository..."
  log "info" $REPO
  curl -L $REPO -o /tmp/ddns.zip > /dev/null 2>&1
  log "info" "Download successful!"
  log "info" "Extracting download..."
  unzip /tmp/ddns.zip -d /tmp > /dev/null 2>&1
  cp -r /tmp/smartizer-ddns-updater-main/* /etc/smartizer/ddns > /dev/null 2>&1
  log "info" "Extract to /etc/smartizer/ddns successful!"
  log "info" "Clearing..."
  rm /tmp/ddns.zip > /dev/null 2>&1
  rm -r /tmp/smartizer* > /dev/null 2>&1
  log "info" "Clear successful!"
}

function download_error() {
  log "error" "Error downloading and unpacking the repository"
}

# Check if the current user is root
if [ "$EUID" -ne 0 ]; then
  log "error" "Please run the script as root."
fi

# Check if the group already exists
if getent group smartizer > /dev/null 2>&1; then
  log "info" "Group smartizer already exists."
else
  # Create the new group
  groupadd smartizer > /dev/null 2>&1
fi

# Check if the user already exists
if getent passwd smartizer > /dev/null 2>&1; then
  log "info" "User smartizer already exists."
else
  # Create a new user with a custom home directory and shell
  useradd -d /etc/smartizer -s /bin/bash -g smartizer smartizer > /dev/null 2>&1
fi

chown -R smartizer:smartizer /etc/smartizer /var/log/smartizer > /dev/null 2>&1
chmod -R 750 /etc/smartizer /var/log/smartizer > /dev/null 2>&1

# Check if curl is installed
dpkg -s curl &> /dev/null
if [ $? -eq 0 ]; then
  # curl is installed
  log "info" "curl is already installed."
else
  # git is not installed
  log "info" "curl is not installed. Install..."
  apt-get install curl -y > /dev/null 2>&1
fi

# Check if unzip is installed
dpkg -s unzip &> /dev/null
if [ $? -eq 0 ]; then
  # git is installed
  log "info" "unzip is already installed."
else
  # git is not installed
  log "info" "unzip is not installed. Install..."
  apt-get install unzip -y > /dev/null 2>&1
fi

# Check if git is installed
dpkg -s git &> /dev/null
if [ $? -eq 0 ]; then
  # git is installed
  log "info" "git is already installed."
else
  # git is not installed
  log "info" "git is not installed. Install..."
  apt-get install git -y > /dev/null 2>&1
fi

# Check if python3 is installed
dpkg -s python3 &> /dev/null
if [ $? -eq 0 ]; then
  # python3 is installed
  log "info" "python3 is already installed."
else
  # python3 is not installed
  log "info" "python3 is not installed. Install..."
  apt-get install python3 -y > /dev/null 2>&1
fi

# Check if python3-venv is installed
dpkg -s python3-venv &> /dev/null
if [ $? -eq 0 ]; then
  # python3-venv is installed
  log "info" "python3-venv is already installed."
else
  # python3-venv is not installed
  log "info" "python3-venv is not installed. Install..."
  apt-get install python3-venv -y > /dev/null 2>&1
fi

# Check if python3-pip is installed
dpkg -s python3-pip &> /dev/null
if [ $? -eq 0 ]; then
  # python3-pip is installed
  log "info" "python3-pip is already installed."
else
  # python3-pip is not installed
  log "info" "python3-pip is not installed. Install..."
  apt-get install python3-pip -y > /dev/null 2>&1
fi

# Check if python3-dev is installed
dpkg -s python3-dev &> /dev/null
if [ $? -eq 0 ]; then
  # python3-dev is installed
  log "info" "python3-dev is already installed."
else
  # python3-dev is not installed
  log "info" "python3-dev is not installed. Install..."
  apt-get install python3-dev -y > /dev/null 2>&1
fi

download || download_error

if [ ! -x "$BINARY" ]; then
  chmod -x "$BINARY"
fi

# Check if the link already exists
if [ ! -L "$LINK" ]; then
  # Create the symbolic link if it doesn't exist
  ln -s "$BINARY" "$LINK"
fi

python3 -m pip install -r /etc/smartizer/ddns/requirements.txt > /dev/null 2>&1