import os
import re

ROOT = "data/acne/JPEGImages"

for fname in os.listdir(ROOT):
    old_path = os.path.join(ROOT, fname)

    # Only rename if file starts with "levle"
    if fname.startswith("levle"):
        # Replace only at beginning
        new_name = fname.replace("levle", "level", 1)
        new_path = os.path.join(ROOT, new_name)

        print(f"Renaming: {fname}  -->  {new_name}")
        os.rename(old_path, new_path)

print("\nDone! All filenames corrected.")

