# Python code for ShanWan PS3-style Controller

When I got my Waveshare Jetbot with Nvidia Jets Nano, I received one of those
crappy ShanWan PS3 controller clones with it. The demo code had me connect the
controller to my laptop and would relay the control signals to the robot. While
that is a nice demonstration of teleoperation, I'd much rather just plug the
controller into the Jetbot and control it directly.

The controller is not well supported, so I had to write my own code to be able
to use it from my Jetbot. This repository contains the code that I wrote to
support the controller.

## On Quality

The workmanship on this controller is not of a very high standard. It is clear
that when WaveShare commissioned these, they looked at price more than at
quality. Inside the controller you will find manual fixes to bad solder joints,
untightened metal lips that were intended to hold the joysticks in place and
missing internal screws.

My advice is to steer clear of these controllers. They are not going to be a
good experience. I only use this one because it came with the Jetbot and I don't
use controllers nearly enough to warrant buying one to replace it.

## USB Protocol Basics

Python has some quite decent support for low level USB operations, though it
assumes that you are familiar with the inner workings of the protocol. Since I
was not, I sat down to learn a bit about it. The following material got me
started:

[Brenden Adamczak](https://github.com/brendena) published a quick [tutorial on
USB protocol for developers](https://www.youtube.com/watch?v=fEDp9053eZs&list=PL2rtAVvB6y_SdtDvbr5ZOhNDIkFSCokyk&index=2).
With that under my belt, I found [Alex Lugo](https://github.com/alugocp)'s
videos on Python USB quite useful as a starting point. I had to add my own error
handling, though.

A neat trick is to enable the debug traces of `PYUSB_DEBUG` and `LIBUSB_DEBUG`
using the environment variable. This will give you heaps to tracing information.
Note the ordering in the example below. The environment variables for the
command are set _after_ the `sudo` and not before.

```
sudo PYUSB_DEBUG=debug LIBUSB_DEBUG=4 python3 game-controller.py
```

## Controller Output

To just test the controller, I wrote a small program that prints out what
buttons are pressed.

## Known Issues

The Y-axis of the left joystick influences the X-axis value of the right
joystick, but (weirdly) not the other way around. I could not find an obvious
cause for this, but I only did a quick inspection. I am curious if this is a
general problem, or just an issue with my actual device.

Not all buttons are being picked up by my code. Notably, the keyboard-style
buttons are not reflected in the packets I read. I tried accessing the endpoints
other than the `0x81` one, but I had no luck getting these to work. This is
probably due to my limited understanding of USB. Specifically, calling
`endpoint.read()` on endpoint `0x83` always gives me the error `[Errno 110]
Operation timed out`. Writing to endpoint `0x02` also gives me the error `[Errno
110] Operation timed out`. I have not tried control transfer requests yet.

Triggers 2 should be force-sensitive, but they are not. Inside the device, they
are just the same press buttons as all the others. In the USB messages, they do
report 255 as the force, but there is no force detection hardware, so this is
just the fixed force value.

The Linux kernel does not show this controller as a supported USB device. If I
knew what driver to specify for this device, I could send an upstream patch.

The controller seems to lose connection to its dongle a lot. That may be because
I am running it off of rechargeable batteries.

