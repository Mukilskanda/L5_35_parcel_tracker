"""Courier and parcel tracking: booking, tracking, OTP and shipping cost."""
import ipaddress
import os
import secrets
import subprocess  # nosec B404 - used only with validated args, shell=False
import tempfile
from datetime import date

STATUS_FLOW = ["Booked", "Picked Up", "In Transit",
               "Out for Delivery", "Delivered"]
parcels = {}


def book_parcel(sender, receiver, weight_kg, history=None):
    """Book a parcel and return its new tracking id."""
    if history is None:
        history = []
    tracking_id = "TRK" + str(10001 + len(parcels))
    parcels[tracking_id] = {"sender": sender, "receiver": receiver,
                            "weight": weight_kg, "status": 0,
                            "booked": str(date.today())}
    history.append(tracking_id)
    return tracking_id


def advance_status(tracking_id):
    """Move a parcel to its next delivery stage and return the new stage."""
    parcel = parcels[tracking_id]
    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1
    return STATUS_FLOW[parcel["status"]]


def shipping_cost(weight_kg):
    """Return the shipping cost: base 50 plus 30 per kg above the first."""
    cost = 50
    if weight_kg > 1:
        cost += (weight_kg - 1) * 30
    return round(cost, 2)


def track_parcel(tracking_id):
    """Return a 'sender -> receiver: status' line for a parcel."""
    try:
        parcel = parcels[tracking_id]
    except KeyError:
        return "Unknown tracking id " + tracking_id
    route = parcel["sender"] + " -> " + parcel["receiver"]
    return route + ": " + STATUS_FLOW[parcel["status"]]


def is_with_courier(tracking_id):
    """Return True while the parcel is picked up or in transit."""
    status = STATUS_FLOW[parcels[tracking_id]["status"]]
    return status in ("Picked Up", "In Transit")


def label_path():
    """Create a unique temporary label file and return its path."""
    file_descriptor, path = tempfile.mkstemp(suffix=".txt")
    os.close(file_descriptor)
    return path


def ping_hub(hub_address):
    """Ping a hub once; the address must be a valid IP address."""
    address = str(ipaddress.ip_address(hub_address))  # rejects injection
    return subprocess.check_output(  # nosec B603 B607 - validated, no shell
        ["ping", "-c", "1", address])


def main():
    """Run a short demonstration of the parcel tracker."""
    first = book_parcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = book_parcel("Gadget Hub", "Sneha Rao", 0.8)
    third = book_parcel("Spice Store", "Imran Khan", 4)
    advance_status(first)
    advance_status(first)
    advance_status(second)
    for _ in range(6):
        advance_status(third)
    for tracking_id in (first, second, third):
        print(track_parcel(tracking_id))
        print("  with courier:", is_with_courier(tracking_id))
        print("  cost:", shipping_cost(parcels[tracking_id]["weight"]))
    print(track_parcel("TRK00000"))  # unknown id
    delivery_otp = 1000 + secrets.randbelow(9000)  # secure 4-digit OTP
    print("Delivery OTP for", third, "is", delivery_otp)
    print("Parcels booked today:", len(parcels))


if __name__ == "__main__":
    main()
