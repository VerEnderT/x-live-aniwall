x-live-aniwall for Debian
==========================

x-live-aniwall is a lightweight tool that provides animated desktop wallpapers for XFCE on Debian-based systems.  
It launches a PyQt5-based application that integrates seamlessly with the XFCE environment.

This tool is especially useful for users who want a more dynamic and visually engaging desktop without heavy background daemons or compositors.

Features:
---------

 - Simple PyQt5-based GUI
 - Displays animated wallpapers in the XFCE desktop
 - Starts automatically via `.desktop` entry if enabled
 - Designed for lightweight systems and live environments (e.g. X-Live)

Dependencies:
-------------

The following packages are required and are declared in the control file:

 - python3
 - python3-pyqt5
 - ffmpeg
 - wmctrl
 - xfconf

These will be installed automatically with the `.deb` package on supported systems.

Usage:
------

To run the application, execute:

    x-live-aniwall

Alternatively, launch it from your applications menu under  
"Utilities" or "X-Live Apps" as **X-Live Aniwall**.

Project Source:
---------------

GitHub repository:  
https://github.com/VerEnderT/x-live-aniwall

Bug reports, feature requests, and contributions are welcome!

Author:
-------

Frank Maczollek aka VerEnderT  
<chaosz932@gmail.com>

License:
--------

This program is licensed under the GNU General Public License version 3 or later.  
See `/usr/share/doc/x-live-aniwall/copyright` for full licensing details.
