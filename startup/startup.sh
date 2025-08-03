#!/bin/sh

screen -dmS cameraStream bash -c "bash /home/cyberman/RemoteRobot/startup/camera-screen.sh"
screen -dmS webServer bash -c "bash /home/cyberman/RemoteRobot/startup/webserver-screen.sh"

# Wait forever so systemd service doesn’t exit
tail -f /dev/null
