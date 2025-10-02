import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
from collections import Counter

# ALWAYS use the CSV file in the same directory as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(SCRIPT_DIR, "coop_applications.csv")
HEADERS = ['Company', 'Job Title', 'Date Applied', 'Status', 'Notes']
ALLOWED_STATUSES = {'Applied', 'Interviewing', 'Offer', 'Rejected'}

def ensure_file() -> None:
    """Create CSV file with headers if it doesn't exist or is empty."""
    print(f"📁 Using CSV file: {FILENAME}")
    
    if not os.path.exists(FILENAME) or os.path.getsize(FILENAME) == 0:
        try:
            with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(HEADERS)
            print(f"✅ Created new CSV file with headers")
        except Exception as e:
            print(f"❌ Error creating CSV file: {e}")

def migrate_data_from_parent():
    """One-time migration: move data from parent directory to tracker directory."""
    parent_csv = r"c:\Users\Family\python projects\coop_applications.csv"
    
    if os.path.exists(parent_csv) and os.path.exists(FILENAME):
        print("🔄 Found data in parent directory. Migrating to tracker directory...")
        
        try:
            # Read existing data from both files
            tracker_entries = []
            parent_entries = []
            
            # Read tracker file
            if os.path.getsize(FILENAME) > 0:
                with open(FILENAME, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    tracker_entries = list(reader)
            
            # Read parent file
            with open(parent_csv, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                parent_entries = list(reader)
            
            # Combine and deduplicate
            all_entries = tracker_entries + parent_entries
            unique_entries = []
            seen = set()
            
            for entry in all_entries:
                key = (entry.get('Company', ''), entry.get('Job Title', ''), entry.get('Date Applied', ''))
                if key not in seen:
                    unique_entries.append(entry)
                    seen.add(key)
            
            # Write all data to tracker file
            with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=HEADERS)
                writer.writeheader()
                writer.writerows(unique_entries)
            
            print(f"✅ Migrated {len(unique_entries)} entries to tracker directory")
            
            # Remove the parent file
            os.remove(parent_csv)
            print(f"🗑️ Removed old file from parent directory")
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")

def validate_date(date_str: str) -> Optional[str]:
    """Validate date format and return standardized date or None if invalid."""
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        return None

def add_entry() -> None:
    """Add new entry to the CSV file."""
    print("\n📝 Adding New Application")
    print("-" * 30)
    
    company = input("Company: ").strip()
    if not company:
        print("❌ Company name is required")
        return
    
    title = input("Job Title: ").strip()
    if not title:
        print("❌ Job title is required")
        return
    
    # Date validation
    while True:
        date = input("Date Applied (YYYY-MM-DD) [Today]: ").strip()
        validated_date = validate_date(date)
        if validated_date:
            break
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
    
    # Status validation
    print(f"Available statuses: {', '.join(sorted(ALLOWED_STATUSES))}")
    while True:
        status = input("Status: ").strip()
        if status in ALLOWED_STATUSES:
            break
        print(f"❌ Status must be one of: {', '.join(sorted(ALLOWED_STATUSES))}")
    
    notes = input("Notes (optional): ").strip()
    if not notes:
        notes = "N/A"

    try:
        with open(FILENAME, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([company, title, validated_date, status, notes])
        print("✅ Application saved successfully!")
    except Exception as e:
        print(f"❌ Error saving application: {e}")

def get_entries() -> List[Dict]:
    """Read all entries from CSV file."""
    try:
        with open(FILENAME, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return []

def search_entries(query: str) -> None:
    """Search through applications."""
    entries = get_entries()
    if not entries:
        print("⚠️ No applications found.")
        return
    
    query = query.lower()
    matches = []
    
    for entry in entries:
        if any(query in str(value).lower() for value in entry.values()):
            matches.append(entry)
    
    if matches:
        print(f"\n🔍 Found {len(matches)} matching applications:")
        display_entries(matches)
    else:
        print(f"❌ No applications found matching '{query}'")

def display_entries(entries: List[Dict], sort_by: str = 'Date Applied') -> None:
    """Display entries in a formatted way."""
    if not entries:
        print("⚠️ No applications to display.")
        return
    
    # Sort entries by date (newest first)
    try:
        entries.sort(key=lambda x: datetime.strptime(x.get(sort_by, '1900-01-01'), '%Y-%m-%d'), reverse=True)
    except ValueError:
        pass  # If date parsing fails, keep original order
    
    print(f"\n📋 Applications (Total: {len(entries)}):")
    print("=" * 80)
    
    for i, entry in enumerate(entries, 1):
        status_emoji = {
            'Applied': '📤',
            'Interviewing': '🎤', 
            'Offer': '🎉',
            'Rejected': '❌'
        }.get(entry.get('Status', ''), '📝')
        
        print(f"{i:2d}. {status_emoji} {entry.get('Company', 'N/A')} - {entry.get('Job Title', 'N/A')}")
        print(f"    📅 Applied: {entry.get('Date Applied', 'N/A')} | Status: {entry.get('Status', 'N/A')}")
        if entry.get('Notes') and entry.get('Notes') != 'N/A':
            print(f"    📝 Notes: {entry.get('Notes')}")
        print()

def show_statistics() -> None:
    """Show application statistics."""
    entries = get_entries()
    if not entries:
        print("⚠️ No applications found.")
        return
    
    status_counts = Counter(entry.get('Status', 'Unknown') for entry in entries)
    
    print(f"\n📊 Application Statistics (Total: {len(entries)}):")
    print("=" * 50)
    for status, count in status_counts.most_common():
        percentage = (count / len(entries)) * 100
        print(f"{status:12} : {count:3d} ({percentage:5.1f}%)")

def main():
    """Main program loop."""
    print("🎯 Co-op Job Application Tracker")
    print("=" * 40)
    
    # One-time data migration from parent directory
    migrate_data_from_parent()
    
    # Ensure the CSV file exists in tracker directory
    ensure_file()
    
    while True:
        print(f"\nChoose: [a]dd, [l]ist, [s]earch, [stats], [q]uit")
        cmd = input("> ").strip().lower()
        
        if cmd in ('a', 'add'):
            add_entry()
        elif cmd in ('l', 'list'):
            entries = get_entries()
            display_entries(entries)
        elif cmd in ('s', 'search'):
            query = input("Search query: ").strip()
            if query:
                search_entries(query)
        elif cmd in ('stats', 'statistics'):
            show_statistics()
        elif cmd in ('q', 'quit', 'exit'):
            print("👋 Goodbye!")
            break
        else:
            print("❌ Unknown command. Try again.")

if __name__ == "__main__":
    main()
    #End of Program
