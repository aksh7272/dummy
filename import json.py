import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Output folder
OUTPUT_DIR = "zoom_bookings_data"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# Sample values
statuses = ["completed", "cancelled", "confirmed", "ongoing"]
car_ids = [f"CAR{100+i}" for i in range(50)]
customer_ids = [f"C{str(i).zfill(3)}" for i in range(1, 500)]

def random_booking(booking_num, booking_date):
    start_hour = random.randint(0, 20)
    duration = random.randint(2, 12)

    start_dt = datetime.combine(
        booking_date,
        datetime.min.time()
    ) + timedelta(hours=start_hour)

    end_dt = start_dt + timedelta(hours=duration)

    return {
        "booking_id": f"B{booking_num:06}",
        "customer_id": random.choice(customer_ids),
        "car_id": random.choice(car_ids),
        "booking_date": booking_date.strftime("%Y-%m-%d"),
        "start_time": start_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_time": end_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_amount": round(random.uniform(50, 500), 2),
        "status": random.choice(statuses)
    }

# Generate files for many dates
start_date = datetime(2026, 1, 1)
num_days = 30  # number of files

booking_counter = 1

for i in range(num_days):
    current_date = start_date + timedelta(days=i)

    # Filename format
    filename = f"zoom_car_bookings_{current_date.strftime('%Y%m%d')}.json"
    filepath = Path(OUTPUT_DIR) / filename

    # Random number of bookings per file
    num_bookings = random.randint(20, 100)

    bookings = []
    for _ in range(num_bookings):
        bookings.append(random_booking(booking_counter, current_date.date()))
        booking_counter += 1

    # Write JSON file
    with open(filepath, "w") as f:
        json.dump(bookings, f, indent=2)

    print(f"Generated: {filepath}")

print("Done.")