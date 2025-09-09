import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
from collections import Counter

FILENAME = "coop_applications.csv"
HEADERS = ['Company', 'Job Title', 'Date Applied', 'Status', 'Notes']
ALLOWED_STATUSES = {'Applied', 'Interviewing', 'Offer', 'Rejected'}
COMMANDS = {
    'a': 'add',
    'l': 'list',
    's': 'search',
    'stats': 'stats',
    'q': 'quit'
}

def ensure_file() -> None:
    """Make sure csv file exists and has headers."""
    # Check if file doesn't exist or is empty
    is_new_file = not os.path.exists(FILENAME) or os.path.getsize(FILENAME) == 0
    
    if is_new_file:
        # Create new file with headers only if it's new or empty
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
        print("📝 Created new applications file.")

def validate_date(date_str: str) -> Optional[str]:
    """Validate and format date string."""
    try:
        if not date_str:
            return datetime.now().strftime("%Y-%m-%d")
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return None

def add_entry() -> None:
    """Add new entry to the csv file."""
    # Get required fields
    company = input("Company: ").strip()
    while not company:
        print("❌ Company name is required")
        company = input("Company: ").strip()
    
    title = input("Job Title: ").strip()
    while not title:
        print("❌ Job title is required")
        title = input("Job Title: ").strip()
    
    # Date with default to today
    while True:
        date = input("Date Applied (YYYY-MM-DD) [Today]: ").strip()
        validated_date = validate_date(date)
        if validated_date:
            break
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
    
    # Status with tab completion
    status_list = sorted(ALLOWED_STATUSES)
    while True:
        status = input(f"Status ({'/'.join(status_list)}): ").strip().title()
        if status in ALLOWED_STATUSES:
            break
        print(f"❌ Status must be one of: {', '.join(status_list)}")
    
    notes = input("Notes (optional): ").strip()

    try:
        with open(FILENAME, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([company, title, validated_date, status, notes])
        print("✅ Application saved successfully!")
    except Exception as e:
        print(f"❌ Error saving application: {e}")

def get_entries() -> List[Dict]:
    """Read all entries from the CSV file."""
    try:
        with open(FILENAME, newline='') as f:
            return list(csv.DictReader(f))
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return []

def search_entries(query: str) -> None:
    """Search through applications."""
    entries = get_entries()
    if not entries:
        print("⚠️ No applications to search through.")
        return

    query = query.lower()
    matches = [
        entry for entry in entries
        if query in entry['Company'].lower() or
           query in entry['Job Title'].lower() or
           query in entry['Notes'].lower()
    ]

    if not matches:
        print(f"🔍 No applications found matching '{query}'")
        return

    print(f"\n🔍 Found {len(matches)} matching applications:")
    display_entries(matches)

def display_entries(entries: List[Dict], sort_by: str = 'Date Applied') -> None:
    """Display entries in a formatted way."""
    if not entries:
        print("⚠️ No applications to display.")
        return

    # Sort entries by date (newest first) or specified field
    entries.sort(key=lambda x: x[sort_by], reverse=True)
    
    print(f"\n📋 Applications (Total: {len(entries)}):")
    for i, entry in enumerate(entries, 1):
        print(f"{i}. {entry['Company']} - {entry['Job Title']}")
        print(f"   📅 {entry['Date Applied']} → {entry['Status']}")
        if entry.get('Notes'):
            print(f"   📝 {entry['Notes']}")
        print()

def show_statistics() -> None:
    """Display application statistics."""
    entries = get_entries()
    if not entries:
        print("⚠️ No applications yet.")
        return

    # Count applications by status
    status_counts = Counter(entry['Status'] for entry in entries)
    
    # Get date range
    dates = [datetime.strptime(entry['Date Applied'], "%Y-%m-%d") for entry in entries]
    date_range = (max(dates) - min(dates)).days + 1 if dates else 0
    
    # Calculate statistics
    print("\n📊 Application Statistics:")
    print(f"Total Applications: {len(entries)}")
    print(f"Time Span: {date_range} days")
    if date_range > 0:
        print(f"Average: {len(entries)/date_range:.1f} applications per day")
    
    print("\nStatus Breakdown:")
    for status, count in sorted(status_counts.items()):
        percentage = (count / len(entries)) * 100
        print(f"{status}: {count} ({percentage:.1f}%)")

def list_entries(sort_by: str = 'Date Applied') -> None:
    """List all applications stored in the CSV."""
    entries = get_entries()
    display_entries(entries, sort_by)

def main() -> None:
    """Main program loop."""
    ensure_file()
    while True:
        print("\nChoose an option:")
        print("  [a]dd application")
        print("  [l]ist applications")
        print("  [s]earch applications")
        print("  [stats] view statistics")
        print("  [q]uit")
        
        cmd = input("> ").strip().lower()
        
        if cmd in ('a', 'add'):
            add_entry()
        elif cmd in ('l', 'list'):
            list_entries()
        elif cmd in ('s', 'search'):
            query = input("Enter search term: ").strip()
            search_entries(query)
        elif cmd == 'stats':
            show_statistics()
        elif cmd in ('q', 'quit', 'exit'):
            print("👋 Goodbye!")
            break
        else:
            print("❌ Unknown command, try again.")

if __name__ == "__main__":
    main()
    #End of Program
    