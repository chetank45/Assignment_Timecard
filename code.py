import pandas as pd
file_path = "Assignment_Timecard.xlsx"
df = pd.read_excel(file_path)

df = df.sort_values(by=['Employee Name', 'Pay Cycle Start Date']).reset_index(drop=True)


consecutive_days = 0
prev_entry = None

# Initialize variables for condition b and c
prev_time_out = None

# Create a list to store the output
output_lines = []

# Iterate through the DataFrame to find employees meeting the specified conditions
for index, row in df.iterrows():
    if prev_entry is None:
        prev_entry = row
        consecutive_days = 1
        prev_time_out = row['Time Out']
        continue

    # Check if the employee is the same as the previous entry
    if row['Employee Name'] == prev_entry['Employee Name']:
        # Check condition a: 7 consecutive days
        if (row['Time'] - prev_entry['Time']).days == 1:
            consecutive_days += 1
        else:
            consecutive_days = 1

        # Check condition b: Less than 10 hours between shifts but greater than 1 hour
        time_between_shifts = (row['Time'] - prev_time_out).seconds / 3600
        if 1 < time_between_shifts < 10:
            output_lines.append(f"Employee {row['Employee Name']} ({row['Position Status']}) has {time_between_shifts:.2f} hours between shifts.")

        # Check condition c: More than 14 hours in a single shift
        shift_duration = (row['Time Out'] - row['Time']).seconds / 3600
        if shift_duration > 14:
            output_lines.append(f"Employee {row['Employee Name']} ({row['Position Status']}) worked more than 14 hours in a single shift.")

    else:
        consecutive_days = 1

    prev_entry = row
    prev_time_out = row['Time Out']

    # If an employee has worked for 7 consecutive days, add to the output
    if consecutive_days == 7:
        output_lines.append(f"Employee {row['Employee Name']} ({row['Position Status']}) worked for 7 consecutive days.")

# Write the output to a text file
with open("output.txt", "w") as output_file:
    for line in output_lines:
        print(line)
        output_file.write(line + "\n")

print("Output written to output.txt")