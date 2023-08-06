import re
from datetime import datetime
import csv
# Function to extract timestamp from a line using regex


def extract_timestamp(line):
    pattern = r"Timestamp: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    return None


# Initialize dictionary to store results
time_durations = {}
csv_rows = []

# Process each file
for i in range(1, 11):
    filename = f"P{i}ds.txt"
    participant_key = f"P{i}"

    with open(filename, 'r') as file:
        lines = file.readlines()

        start_timestamp = None
        stop_timestamp = None

        # Find last index of "Start" and "Stop"
        for line in reversed(lines):
            if "Start" in line:
                start_timestamp = extract_timestamp(line)
                break

        for line in reversed(lines):
            if "Stop" in line and "Command" in line:
                stop_timestamp = extract_timestamp(line)
                break
        line_count = 0
        counting = False
        for line in reversed(lines):
            if "Stop" in line and "Command" in line:
                counting = True
            if counting:
                line_count += 1
            if "Start" in line:
                counting = False
                break
        # Calculate time duration if both timestamps are found
        if start_timestamp and stop_timestamp:
            start_datetime = datetime.strptime(
                start_timestamp, "%Y-%m-%d %H:%M:%S")
            stop_datetime = datetime.strptime(
                stop_timestamp, "%Y-%m-%d %H:%M:%S")
            duration = stop_datetime - start_datetime
            time_durations[participant_key] = duration
            duration_seconds = (stop_datetime - start_datetime).total_seconds()
            csv_rows.append([participant_key, duration,
                            duration_seconds, line_count])

# Print the results
for participant, duration in time_durations.items():
    print(f"Participant: {participant}, Duration: {duration}")


# Write the CSV file
csv_filename = "time_durations.csv"
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ["Participant", "Duration", "Duration (seconds)", "Steps"])  # Write header
    csv_writer.writerows(csv_rows)  # Write rows
