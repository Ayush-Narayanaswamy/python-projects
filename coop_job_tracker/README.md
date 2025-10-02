# Co-op Job Tracker

A Python program to track co-op job applications using a CSV file with advanced features.

## Features
- Add job applications with validation (date + status)
- List all applications in a clean, sorted format  
- Search through applications
- View application statistics
- Automatic duplicate file detection and merging
- Persistent storage in `coop_applications.csv`

## Usage
```bash
python csvtracker.py
```

## Commands
- `a` or `add` - Add new application
- `l` or `list` - List all applications
- `s` or `search` - Search applications
- `stats` - View statistics
- `q` or `quit` - Exit program

## File Location
The CSV file is always stored in the same directory as the script to prevent duplicate files.
