import usb.core
import usb.util
from time import sleep

def try_connect_controller(idVendor, idProduct, configuration_index, interface_index, endpoint_index):
    try:
        device = usb.core.find(idVendor=idVendor, idProduct=idProduct)
        if device.is_kernel_driver_active(interface_index):
            device.detach_kernel_driver(interface_index)
        usb.util.claim_interface(device, interface_index)
        interface = device[configuration_index].interfaces()[interface_index]
        endpoint = interface.endpoints()[endpoint_index]
        print(f"reading from endpoint 0x{endpoint.bEndpointAddress:02x} on {device.manufacturer} {device.product} at {idVendor:04x}:{idProduct:04x} on /dev/bus/usb/{device.bus:03d}/{device.address:03d}")
        return endpoint
    except ValueError as e:
        print(f"cannot access the device strings, probably needs sudo: {e}")
        exit(1)
    except AttributeError:
        pass # device not found...

    return None

idVendor = 0x2563
idProduct = 0x0526

endpoint = None
while True:
    try:
        if endpoint is None:
            # Try to find the controller and see if we can connect. If not,
            # sleep a little and then break out of the loop to retry later.
            endpoint = try_connect_controller(idVendor, idProduct, 0, 0, 0) # gamepad buttons and joysticks
            # endpoint = try_connect_controller(idVendor, idProduct, 0, 0, 1) # [Errno 32] Pipe error
            # endpoint = try_connect_controller(idVendor, idProduct, 0, 1, 0) # [Errno 110] Operation timed out
            if endpoint is None:
                sleep(1)
                continue

        packet = endpoint.read(endpoint.wMaxPacketSize)
        # print(f"game packet {packet}")

        joy_l_x = packet[1]
        joy_l_y = packet[2]
        joy_r_x = packet[3]
        joy_r_y = packet[4]
    
        print(f"    joystick L ({joy_l_x}, {joy_l_y})")
        print(f"    joystick R ({joy_r_x}, {joy_r_y})")

        if   packet[5] == 0b0000:
            print("    d-pad north")
        elif packet[5] == 0b0110:
                print("    d-pad west")
        elif packet[5] == 0b0010:
            print("    d-pad east")
        elif packet[5] == 0b0100:
            print("    d-pad south")

        if packet[6] & 0b10000000:
            print("    right trigger 1 on")
        if packet[6] & 0b01000000:
            print("    left trigger 1 on")
        if packet[6] & 0b00000001:
            print("    A on")
        if packet[6] & 0b00000010:
            print("    B on")
        if packet[6] & 0b00001000:
            print("    X on")
        if packet[6] & 0b00010000:
            print("    Y on")

        if packet[7] & 0b00000010:
            print(f"    right trigger 2 on, force {packet[8]}")
        if packet[7] & 0b00000001:
            print(f"    left trigger 2 on, force {packet[9]}")
        if packet[7] & 0b00100000:
            print("    left joystick on")
        if packet[7] & 0b01000000:
            print("    right joystick on")
    except usb.core.USBError as e:
        print(f"USB error, disconnecting: {e}")
        sleep(1)
        endpoint = None
