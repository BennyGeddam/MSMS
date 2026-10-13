import faker
import csv

fake = faker.Faker()

# Create a CSV file and write header + rows
with open("customerrequests.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "phone", "status"])  # Header row
    for i in range(1, 101):
        writer.writerow([i, fake.name(), fake.phone_number(), "Pending"])

print("Clean CSV data saved to customerrequests.csv")
