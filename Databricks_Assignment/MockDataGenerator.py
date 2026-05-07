import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================

BOOKING_OUTPUT_DIR = "mock_zoomcar_bookings"
CUSTOMER_OUTPUT_DIR = "mock_zoomcar_customers"

FILES_TO_GENERATE = 10
CUSTOMERS_PER_FILE = 20
BOOKINGS_PER_FILE = 20

START_DATE = datetime(2026, 1, 1)

STATUSES_BOOKING = ["completed", "cancelled", "ongoing", "pending"]
STATUSES_CUSTOMER = ["active", "inactive", "suspended"]

FIRST_NAMES = [
    "John", "Jane", "Michael", "Emily", "Chris",
    "Sarah", "David", "Sophia", "Daniel", "Olivia",
    "Arjun", "Priya", "Rahul", "Ananya", "Vikram"
]

LAST_NAMES = [
    "Smith", "Johnson", "Brown", "Williams", "Jones",
    "Garcia", "Miller", "Davis", "Wilson", "Taylor",
    "Sharma", "Patel", "Reddy", "Kapoor", "Mehta"
]

# =========================================================
# HELPERS
# =========================================================

def random_customer_id(i):
    return f"C{i:06d}"

def random_booking_id(i):
    return f"B{i:06d}"

def random_car_id():
    return f"CAR{random.randint(100, 9999)}"

def random_name():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return first, last

def random_email(first, last, customer_id):
    domains = ["gmail.com", "yahoo.com", "example.com"]
    return (
        f"{first.lower()}.{last.lower()}"
        f"{customer_id[-3:]}@{random.choice(domains)}"
    )

def random_phone():
    return str(random.randint(6000000000, 9999999999))

def random_customer_status():
    return random.choices(
        STATUSES_CUSTOMER,
        weights=[0.8, 0.15, 0.05]
    )[0]

def random_booking_status():
    return random.choices(
        STATUSES_BOOKING,
        weights=[0.7, 0.1, 0.1, 0.1]
    )[0]

def random_signup_date(base_date):
    days_back = random.randint(0, 730)
    signup = base_date - timedelta(days=days_back)
    return signup.strftime("%Y-%m-%d")

def random_amount(hours):
    base_rate = random.randint(10, 25)
    return round(base_rate * hours + random.uniform(5, 50), 2)

# =========================================================
# CUSTOMER GENERATION
# =========================================================

all_customer_ids = []

def generate_customer(record_num, file_date):

    customer_id = random_customer_id(record_num)

    first, last = random_name()

    customer = {
        "customer_id": customer_id,
        "name": f"{first} {last}",
        "email": random_email(first, last, customer_id),
        "phone_number": random_phone(),
        "signup_date": random_signup_date(file_date),
        "status": random_customer_status()
    }

    all_customer_ids.append(customer_id)

    return customer

# =========================================================
# BOOKING GENERATION
# =========================================================

def generate_booking(record_num, booking_date):

    start_hour = random.randint(0, 20)
    duration_hours = random.randint(2, 12)

    start_dt = datetime.combine(
        booking_date,
        datetime.min.time()
    ) + timedelta(hours=start_hour)

    end_dt = start_dt + timedelta(hours=duration_hours)

    # IMPORTANT:
    # pick customer_id from generated customers
    mapped_customer_id = random.choice(all_customer_ids)

    return {
        "booking_id": random_booking_id(record_num),
        "customer_id": mapped_customer_id,
        "car_id": random_car_id(),
        "booking_date": booking_date.strftime("%Y-%m-%d"),
        "start_time": start_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_time": end_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_amount": random_amount(duration_hours),
        "status": random_booking_status()
    }

# =========================================================
# MAIN
# =========================================================

def generate_all_files():

    Path(BOOKING_OUTPUT_DIR).mkdir(exist_ok=True)
    Path(CUSTOMER_OUTPUT_DIR).mkdir(exist_ok=True)

    customer_counter = 1
    booking_counter = 1

    # -----------------------------------------
    # STEP 1: Generate Customer Files
    # -----------------------------------------

    for day in range(FILES_TO_GENERATE):

        current_date = START_DATE + timedelta(days=day)

        customer_filename = (
            f"zoom_car_customers_"
            f"{current_date.strftime('%Y%m%d')}.json"
        )

        customer_file_path = (
            Path(CUSTOMER_OUTPUT_DIR) / customer_filename
        )

        customer_records = []

        for _ in range(CUSTOMERS_PER_FILE):

            customer = generate_customer(
                customer_counter,
                current_date
            )

            customer_records.append(customer)

            customer_counter += 1

        with open(customer_file_path, "w") as f:
            json.dump(customer_records, f, indent=2)

        print(f"Generated Customers: {customer_file_path}")

    # -----------------------------------------
    # STEP 2: Generate Booking Files
    # -----------------------------------------

    for day in range(FILES_TO_GENERATE):

        current_date = START_DATE + timedelta(days=day)

        booking_filename = (
            f"zoom_car_bookings_"
            f"{current_date.strftime('%Y%m%d')}.json"
        )

        booking_file_path = (
            Path(BOOKING_OUTPUT_DIR) / booking_filename
        )

        booking_records = []

        for _ in range(BOOKINGS_PER_FILE):

            booking = generate_booking(
                booking_counter,
                current_date.date()
            )

            booking_records.append(booking)

            booking_counter += 1

        with open(booking_file_path, "w") as f:
            json.dump(booking_records, f, indent=2)

        print(f"Generated Bookings: {booking_file_path}")

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    generate_all_files()