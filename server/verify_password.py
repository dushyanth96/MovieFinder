import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("DB_PASSWORD", "")
print(f"Password length: {len(password)}")
print(f"First 5 chars: {password[:5]}")
print(f"Last 5 chars:  {password[-5:]}")
print(f"Full password: {password}")
print()
print("Character breakdown:")
for i, c in enumerate(password):
    print(f"  [{i:2d}] '{c}' = ord({ord(c)})")
