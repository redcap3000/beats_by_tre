# beats_by_tre
Raspberry pi sense hat python project to use the accelerator to analyze vibration data (with the intention of pin-pointing sources of deep bass typically from a stereo or subwoofer)

# Why

I wanted something other than a microphone to visualize vibration data, and to record this data 24/7 and not have to worry about processing large files.
I am using this to soundproof my house and to compare 'before/after' but to also learn when my enviornments are the most non-vibrational.
# How it works

1) Poll the sensehat api (xyz), 
2) compare against previous values (percent change) 
3) notate when values are either zero, '100%', when they are '100%' per each line
4) Print a line per each analysis (once per second or less.)

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
