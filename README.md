WiFi Server
========

This started out as a webserver to control a WiFi module for OctoPrint on a raspberry pi, 
but we quickly realized it could act as a generic WiFi server for many other projects on the Raspberry Pi, 
or other similar devices.

We're trying to keep the dependencies to a minimum, and support as many configurations as possible. Currently we're
focused on making a standalone Access Point or Client, based on a jumper on the Raspberry Pi GPIO pins.

__We plan to support some or all of these other options moving forward:__

- bluetooth configuration from Android/iOS app
- led blink code / button for changing modes
- lcd panel [adafruit lcd panel] (http://www.adafruit.com/products/1115)
