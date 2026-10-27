import ipaddress
import os
import secrets
import subprocess  # nosec B404 - validated args, shell=False
import tempfile
from datetime import date

STATUS_FLOW = ["Booked", "Picked Up", "In Transit",
               "Out for Delivery", "Delivered"]
parcels = {}


def bookParcel(sender, receiver, weightKg, history=[]):
    trackingId = "TRK" + str(10001 + len(parcels))
    parcels[trackingId] = {"sender": sender, "receiver": receiver,
                           "weight": weightKg, "status": 0,
                           "booked": str(date.today())}
    history.append(trackingId)
    return trackingId


def advanceStatus(trackingId):
    parcel = parcels[trackingId]
    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1
    return STATUS_FLOW[parcel["status"]]


def shippingCost(weightKg):
    cost=50
    if weightKg > 1:
        cost += (weightKg - 1) * 30
    return round(cost, 2)


def trackParcel(trackingId):
    try:
        parcel = parcels[trackingId]
    except Exception:
        return "Unknown tracking id " + trackingId
    route = parcel["sender"] + " -> " + parcel["receiver"]
    return route + ": " + STATUS_FLOW[parcel["status"]]


def isWithCourier(trackingId):
    status = STATUS_FLOW[parcels[trackingId]["status"]]
    return status == "Picked Up" or status == "In Transit"


def labelPath():
    # Helper kept for the lab: not called by the demo
    file_descriptor, path = tempfile.mkstemp(suffix=".txt")
    os.close(file_descriptor)
    return path


def pingHub(hubAddress):
    # Helper kept for the lab: not called by the demo
    address = str(ipaddress.ip_address(hubAddress))  # rejects injection
    return subprocess.check_output(  # nosec B603 B607 - validated, no shell
        ["ping", "-c", "1", address])


def main():
    first = bookParcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = bookParcel("Gadget Hub", "Sneha Rao", 0.8)
    third = bookParcel("Spice Store", "Imran Khan", 4)
    advanceStatus(first)
    advanceStatus(first)
    advanceStatus(second)
    for _ in range(6):
        advanceStatus(third)
    for trackingId in (first, second, third):
        print(trackParcel(trackingId))
        print("  with courier:", isWithCourier(trackingId))
        print("  cost:", shippingCost(parcels[trackingId]["weight"]))
    print(trackParcel("TRK00000")) # unknown id
    delivery_otp = 1000 + secrets.randbelow(9000)  # secure 4-digit OTP
    print("Delivery OTP for", third, "is", delivery_otp)
    print("Parcels booked today:",len(parcels))
main()
