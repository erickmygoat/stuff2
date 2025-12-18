import zipfile
import os

def create_zip():
    zip_filename = "stuff2.zip"
    print(f"Creating {zip_filename}...")

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):
            # Exclude unwanted directories
            if ".git" in root or "__pycache__" in root or "venv" in root or "brain_memory" in root or "tools" in root:
                continue

            for file in files:
                if file == zip_filename or file.endswith(".zip") or file.endswith(".log"):
                    continue

                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, ".")
                print(f"Adding {arcname}")
                zipf.write(file_path, arcname)

    print("Zip created successfully.")

if __name__ == "__main__":
    create_zip()
