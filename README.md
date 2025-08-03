# RemoteRobot

The back and front end of a 4 wheeled robot that can be controlled remotely through network ports.

A Flask server is hosted on port 5000, a videostream is hosted on port 8888 (and 8889, though its unused).
The videostream is hosted by a media-routing software called [MediaMTX](https://github.com/bluenviron/mediamtx). These ports are then routed
through a reverse-proxy software called [Nginx](https://nginx.org/), this way the website is available on port 80. The main
page is located at "/" and the videostream is located at "/video".

This project didnt end up working, we had trouble with the continous servos. These issues could
probably have been worked out, but we ran out of time. The (unavailable) CAD files used in this project
were made by my brother.

---

## Current setup:

### Hardware:

Four contious servo motors are connected to an [SSC32](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/servo-erector-set-system/ses-electronics/ses-modules/ssc-32/ssc-32-manual/) servo controller. The SSC32 recieves commands from a Raspberry Pi 4B.

### Software

Three pieces of software run on the Pi, the webserver (port 5000), a MediaMTX server hosting a HLS
videostream (port 888) and Nginx making the whole thing accessible on port 80.

To access the server from the internet, you must either forward port 80 on the Pi or access the local network through a VPN.