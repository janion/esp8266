# Wifi-enabled RGB LED tabletop

This project is intended for a tabletop 10x10 array of WS2812B (Neopixel) LEDs.

The idea is to have an ESP8266 running micropython controlling the LEDs while also listeneing for socket connections to set the pattern currently being set.

New patterns can be added via this basic web interface and can be saved in the processor's file system for later retrieval.
The use of my function parsing library may be unnecessary since python has an intrinsic *eval()* method which does the same thing :(.

It would be good to have different functions for R, G & B such that any arbitrary pattern can be created.

It will be based off:
https://github.com/janion/EquationParser
https://github.com/janion/esp8266