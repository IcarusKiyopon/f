import pandas as pd
from sqlalchemy import create_engine
import re
import os

# 1. LOCAL DATABASE CONFIGURATION
# This matches the admin/password123 you set in the docker-compose file
LOCAL_URL = "postgresql://admin:password123@localhost:5432/frammer_analytics"
engine = create_engine(LOCAL_URL)

def clean_column_name(name):
    """Converts 'Uploaded Duration (hh:mm:ss)' -> 'uploaded_duration'"""
    name = str(name)
    name = re.sub(r'\(.*?\)', '', name) # Remove anything in parentheses
    clean_name = name.strip().lower().replace(" ", "_").replace("-", "_")
    return re.sub(r'_+', '_', clean_name).strip('_')

# List of your 11 files
files_to_load = [
    "video_list_data_obfuscated.csv",
    "channel-wise-publishing duration.csv",
    "channel-wise-publishing.csv",
    "CLIENT 1 combined_data(2025-3-1-2026-2-28).csv",
    "combined_data(2025-3-1-2026-2-28) by channel and user.csv",
    "combined_data(2025-3-1-2026-2-28) by input type.csv",
    "combined_data(2025-3-1-2026-2-28) by language.csv",
    "combined_data(2025-3-1-2026-2-28) by output type.csv",
    "combined_data(2025-3-1-2026-2-28) by user.csv",
    "monthly-chart.csv"
]

print("🚀 Starting local ingestion...")

for file in files_to_load:
    if not os.path.exists(file):
        print(f"⏩ Skipping {file} (Not found)")
        continue

    try:
        df = pd.read_csv(file)
        # Apply cleaning to columns
        df.columns = [clean_column_name(col) for col in df.columns]
        
        # Create a clean table name
        table_name = clean_column_name(file.split('.')[0])
        
        # Upload to Docker Postgres
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"✅ Created table: {table_name}")
    except Exception as e:
        print(f"❌ Error with {file}: {e}")

print("\n🎉 ALL DATA IS NOW IN DOCKER!")