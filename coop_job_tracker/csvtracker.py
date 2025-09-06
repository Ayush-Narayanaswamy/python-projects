import csv
import os
import datetime

FILENAME = "coop_applications.csv" 
HEADERS = ['Company', 'Job Title', 'Date Applied', 'Status', 'Notes']
ALLOWED_STATUSES = {'Applied', 'Interviewing', 'Offer', 'Rejected'}

def ensure_file():
    """Make sure csv file exists and has headers."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)

def add_entry():
    """ add new entry to the csv file."""
    company = input("Company: ").strip()
    title = input("Job Title: ").strip()
    # Validate date
    while True:
        date = input("Date Applied (YYYY-MM-DD): ").strip()
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
    # Validate status
    while True:
        status = input("Status (Applied/Interviewing/Offer/Rejected): ").strip()
        if status in ALLOWED_STATUSES:
            break
        print(f"❌ Status must be one of: {', '.join(ALLOWED_STATUSES)}")
    notes = input("Notes (optional): ").strip()

    try:
        with open(FILENAME, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([company, title, date, status, notes])
        print("✅ Application saved.")
    except Exception as e:
        print(f"❌ Error saving application: {e}")

def list_entries():
    """List all applications stored in the CSV."""
    try:
        with open(FILENAME, newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    if not rows:
        print("⚠️ No applications yet.")
        return

    print(f"\n📋 Current Applications (Total: {len(rows)}):")
    for i, row in enumerate(rows, 1):
        print(f"{i}. {row['Company']} - {row['Job Title']} ({row['Date Applied']}) → {row['Status']}")
        if row.get('Notes'):
            print("   Notes:", row['Notes'])

def main():
    ensure_file()
    while True:
        print("\nChoose: [a]dd application, [l]ist applications, [q]uit")
        cmd = input("> ").strip().lower()
        if cmd == 'a':
            add_entry()
        elif cmd == 'l':
            list_entries()
        elif cmd == 'q':
            print("👋 Goodbye.")
            break
        else:
            print("❌ Unknown command, try again.")

if __name__ == "__main__":
    main()