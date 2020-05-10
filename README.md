# Linux-Mint-Mirrors-Upstream-Updater

A program which updates the official upstream mirrors source to be the nearest one and backs up the old one.

The python file extract all the mirrors from the Mint official site and saves it to a file.

The bash file pings each mirror and replaces the existing one with the nearest one (the one with the minimal ping time), and also saves the old one as a backup - if the new source makes some problems for any reason, it reverts it to be as it was in the beginning.
The bash file also logs all the process.
