# ScopeDog

![IMG_5439](https://github.com/user-attachments/assets/37c39503-d6f9-4fa0-a640-b8cd1eb91413)

code for AltAz telescopes (primarily Dobsonians) to provide tracking, goto and utilise plate-solving to improve pointing accuracy.

Requires:
- Raspberry Pi (4 or 5) running Bookworm 64 bit OS
- A custom hand box (Raspberry Pi Pico, OLED display and switches) connected via USB
- A Nexus DSC with optical encoders, connected with a ttl to USB cable from TXD0 & RXD0
- An ASI Camera (Suggest ASI120MM-S or mini), with 50mm f1.8 or faster cctv lens
- Stepper motors driving through suitable gear reduction.

Full details at [
](https://astrokeith.com/equipment/scopedog/)https://astrokeith.com/equipment/scopedog/

Note: As of September 2024 uart3 is used instead of uart0. Old hardware builds will need to be modified (switch two pairs of wires on the GPIO)

# Install
- Use Raspberry Pi Imager to create a fresh 32gb sdCard with the latest 64bit Bookworm OS. Make sure username is 'scopedog' and hostname 'scopedogmk3'
- Boot the Pi and from the command line run the install.sh script. This will install all dependencies (Phidget support, astrometry.net, camera drivers, webpage server, etc) plus the ScopeDog specific code.
- ScopeDog requires a bespoke handbox (refer to [
](https://astrokeith.com/equipment/scopedog/scopedog-mk3-hand-box)https://astrokeith.com/equipment/scopedog/scopedog-mk3-hand-box
- The code for the hand box Pico is main_eF4_1.py
- The install script enables VNC which can be reached from a browser at scopedogmk3.local
- If a Nexus DSC is connected and the hand box is found, the ScopeDog starts automatically at power up.
- A 'Lite' variant that runs without a Nexus DSC and encoders is now available. Refer to the readme in the /lite folder.
- An attempt to start the Lite variant will be made if no Nexus DSC is found on starting scopedogmk3.py.
  
## Operation
Refer to system description at  [
](https://astrokeith.com/equipment/scopedog/)https://astrokeith.com/equipment/scopedog/


