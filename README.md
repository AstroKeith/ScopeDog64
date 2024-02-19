# ScopeDog
code for AltAz telescopes (primarily Dobsonians) to provide tracking, goto and utilise plate-solving to improve pointing accuracy.

Requires:
- Raspberry Pi (4 or 5) running Bookworm 64 bit OS
- A custom hand box (Raspberry Pi Pico, OLED display and switches) connected via USB
- A Nexus DSC with optical encoders, connected with a ttl to USB cable from TXD0 & RXD0
- An ASI Camera (Suggest ASI120MM-S), with 50mm f1.8 or faster cctv lens
- Stepper motors driving through suitable gear reduction.

Full details at [
](https://astrokeith.com/equipment/scopedog/)https://astrokeith.com/equipment/scopedog/

# Install
- Use Raspberry Pi Imager to create a fresh 32gb sdCard with the latest 64bit Bookworm OS. Make sure username is 'scopedog' and hostname 'scopedogmk3'
- Boot the Pi and from the command line run the install.sh script. This will install all dependencies (Phidget support, astrometry.net, camera drivers, webpage server, etc) plus the ScopeDog specific code.
- ScopeDog requires a bespoke handbox (refer to [
](https://astrokeith.com/equipment/scopedog/scopedog-mk3-hand-box)https://astrokeith.com/equipment/scopedog/scopedog-mk3-hand-box
- The code for the hand box Pico is main_eF1_?.py
- The install script enables VNC which can be reached from a browser at scopedogmk3.local
- If a Nexus DSC is connected and the hand box is found, the ScopeDog starts automatically at power up.
  
## Operation
Refer to system description at  [
](https://astrokeith.com/equipment/scopedog/)https://astrokeith.com/equipment/scopedog/


