import subprocess

# Install required packages
subprocess.run(["sudo", "pip", "install", "paho-mqtt"])
subprocess.run(["sudo", "pip", "install", "flask"])
subprocess.run(["sudo", "pip", "install", "flask-sqlalchemy"])
subprocess.run(["sudo", "pip", "install", "sqlalchemy"])

# Start the mosquitto service
subprocess.run(["sudo", "systemctl", "start", "mosquitto.service"])
