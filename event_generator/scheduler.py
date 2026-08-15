import time
from event_generator.generate_events import generate_event

INTERVAL = 5  # seconds

print("=" * 60)
print("Enterprise SOC Event Scheduler Started")
print("Press CTRL + C to stop")
print("=" * 60)

try:

    while True:

        generate_event()

        time.sleep(INTERVAL)

except KeyboardInterrupt:

    print("\nScheduler stopped.")