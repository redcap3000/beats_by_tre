# beats_by_tre
Raspberry pi sense hat python project to use the accelerator to analyze vibration data (with the intention of pin-pointing sources of deep bass typically from a stereo or subwoofer) 

# WAIT THERES MORE

Monitor 'loud noises' using TPlink smarthome devices via blinking of its LED (in progress).

# Why

I wanted something other than a microphone to visualize vibration data, and to record this data 24/7 and not have to worry about processing large files.
I am using this to soundproof my house and to compare 'before/after' but to also learn when my enviornments are the most non-vibrational.
# How it works

1) Poll the sensehat api (xyz), 
2) compare against previous values (percent change) 
3) notate when values are either zero, '100%', when they are '100%' per each line
4) Print a line per each analysis (once per second or less.)

# Notes uses tplink-smarthome API

If you have TPlink smarthome devices, this project can send a 'blink command' to those devices, given its connected to the same network.

install with

`npm install -g tplink-smarthome-api`


## Requirements

1) Raspberry Pi with Sensehat
2) TPLink Smart Plug HS100 series (required for LED display output)

## Getting Started

1) Calibrate your Sensehat accelerometer

https://www.raspberrypi.org/documentation/hardware/sense-hat/

2) Place your raspberry pi

Location should be 'nearish' to the vibrations you are attempting to collect and be free from 'regular' external vibrations.
Examples, perhaps the corner of the room which is closest to the offending vibrations, on solid floor. If you are using carpet
place a board or something similar to ensure steady placement.

3) Place your TPLink Smart Plug

You'll want to put this somewhere you can see it easily, unobstructed, and preferably in proximity to the wifi router. You can notice when the raspberry pi sends data to a smart plug by monitoring 'top' for node processes, or monitoring the ethernet/network LED.

4) Modify /etc/rc.local to point to a simple startup.sh to launch the process (optional)

## Whats going on here

The sensehat accelerometer is polled at a regular interval comparing each new reading with the previous and applying a percent change formula to the values. If the percent change is equal or 100% on an axis an 'event' is notated, if all three have 'events' in a polling cycle then the smart plug blinks twice, if only two have 'events' then it blinks once.

## Rationale

Regular changes in the accelerometer values from one period to the next denotes a 'beat' or a cycle of a drone. I am trying to capture low frequency buzzing that is difficult to hear, but easy to 'feel.' If the threshold is crossed then a visual indication should occur.

## What shouldn't register

Hopefully most external vibrations wont register - only ones that constitute a 'beat' or other low frequency vibration.

# Roadmap
 * Basic statistical analysis
 * Simple historical LED output?
 * Adjustable parameters (sample rate/g force tolerance, display raw data etc.)
 * Better console output with keyboard commands (gettin all up into python!!)
 * Solid data storage structure including time date
 * Eventually have data stored via mongo db (probably locally) to be accessed via web app for more advanced analytics.
 * Potentially track other sensehat sensors (space permitting.)
 * Permit multiple sense hats to report data and organize.
 * Web app; probably using node/express.js
