# Linux-Mint-Mirrors-Upstream-Updater

A program which updates the official upstream mirrors source to be the nearest one and backs up the old one.

The python file extract all the mirrors from the Mint official site and saves it to a file.

# In process
The bash file pings each mirror and replaces the existing one with the nearest one (the one with the minimal ping time).
The bash file also logs all the process.
