Not compatible with python on windows, you'd have to build your own driver or figure out how to use the C++ dll at https://github.com/INNO-MAKER/USB2CAN-X2/blob/main/For%20Windows/InnoMakerUsb2Can-v.1.2.3/Lib/ReleaseX64/InnoMakerUsb2CanLib.dll

*WSL on windows:*
* Install wsl
* You must now enable socketcan on wsl. Follow these directions:
https://gist.github.com/yonatanh20/664f07d62eb028db18aa98b00afae5a6
* Also, enable the Geschwister Schneider UG interfaces usb drivers by following these directions (you'll have to rebuild the wsl linux kernel again if you didn't do this in the previous step):
https://github.com/INNO-MAKER/USB2CAN-X2/blob/main/Document/Advanced%20Document/If%20Can%20not%20find%20the%20Driver%20On%20your%20Linux/USB2CAN%20Module-Linux%20driver%20config.docx
* load the driver module by running this command in wsl (you must do this everytime you open a new wsl terminal): sudo modprobe gs_usb
* Check for the can interface by running: ls /sys/class/net
and 
ip link show