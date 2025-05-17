from flask import Flask, render_template
import usb.core
import usb.util

app = Flask(__name__)

# USB class codes
usb_classes = {
    0x00: "Defined at Interface Level",
    0x01: "Audio",
    0x02: "Communications",
    0x03: "Human Interface Device (e.g., keyboard, mouse)",
    0x05: "Physical",
    0x06: "Image",
    0x07: "Printer",
    0x08: "Mass Storage (e.g., USB flash drive)",
    0x09: "Hub",
    0x0A: "CDC-Data",
    0x0B: "Smart Card",
    0x0D: "Content Security",
    0x0E: "Video (e.g., webcam)",
    0x0F: "Personal Healthcare",
    0x10: "Audio/Video Devices",
    0xDC: "Diagnostic Device",
    0xE0: "Wireless Controller",
    0xEF: "Miscellaneous",
    0xFE: "Application Specific",
    0xFF: "Vendor Specific"
}

def get_usb_devices():
    devices = []
    for dev in usb.core.find(find_all=True):
        try:
            vendor_id = hex(dev.idVendor)
            product_id = hex(dev.idProduct)
            manufacturer = usb.util.get_string(dev, dev.iManufacturer) or "Unknown"
            product = usb.util.get_string(dev, dev.iProduct) or "Unknown"
            device_class = dev.bDeviceClass
            device_type = usb_classes.get(device_class, "Unknown")

            devices.append({
                "vendor_id": vendor_id,
                "product_id": product_id,
                "manufacturer": manufacturer,
                "product": product,
                "device_type": device_type
            })
        except usb.core.USBError:
            continue
    return devices

@app.route("/")
def index():
    devices = get_usb_devices()
    return render_template("index.html", devices=devices)

if __name__ == "__main__":
    app.run(debug=True)
