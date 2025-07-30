# RemoteRobot

The back and front end of a 4 wheeled robot that can be controlled remotely through network ports.

A webpage is hosted on port 5000, this page relies on a videostream being available on port 8889 on the same local ip.
This approach is flawed, if I got things to work properly, the videostream would be routed through the same port as the
webpage. This could be achieved though a reverse proxy using nginx, but i couldnt get that to work.

## Current setup:

### Hardware:

Four contious servo motors are connected to an SSC32 servo controller. The SSC32 recieves commands from a Raspberry Pi 4B.

### Software

Two pieces of software run on the Pi, the webserver (port 5000) and a MediaMTX server hosting a WebRTC videostream (port 8889).

Since this system is designed to run locally, the only ways to access this robot from another network is either though a VPN
on the same network as the Pi, or through accessing the ports on the Pi directly through an SSH proxy.