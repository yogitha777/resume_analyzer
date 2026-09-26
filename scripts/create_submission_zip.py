import os
import zipfile

def create_submission_zip():
    source_dir = os.path.abspath("C:/Users/anand/OneDrive/Desktop/yogitha_resume_analyzer")
    output_zip = os.path.abspath("C:/Users/anand/OneDrive/Desktop/yogitha_resume_analyzer_SUBMISSION.zip")
    
    exclude_dirs = {"venv", ".venv", ".git", "__pycache__", "pycache", ".pytest_cache", ".idea", ".vscode"}
    exclude_files = {".env", ".DS_Store"}
    
    if os.path.exists(output_zip):
        os.remove(output_zip)
        
    print(f"Creating ZIP archive: {output_zip}")
    count = 0
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith(".egg-info")]
            
            for file in files:
                if file in exclude_files or file.endswith(".pyc") or file.endswith(".zip"):
                    continue
                
                abs_file = os.path.join(root, file)
                rel_file = os.path.relpath(abs_file, source_dir)
                
                # Double check no .env or venv gets included
                if ".env" in rel_file.split(os.sep) or "venv" in rel_file.split(os.sep):
                    continue
                
                zipf.write(abs_file, rel_file)
                count += 1

    size_mb = os.path.getsize(output_zip) / (1024 * 1024)
    print(f"[OK] ZIP successfully created: {output_zip} ({count} files included, size: {size_mb:.2f} MB)")

if __name__ == "__main__":
    create_submission_zip()
