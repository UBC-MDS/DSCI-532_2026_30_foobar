import os
import shutil
import kagglehub

def download_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '../data/raw/')
    os.makedirs(data_dir, exist_ok=True)

    print("Downloading to cache...")
    cached_path = kagglehub.dataset_download("zahranusratt/student-social-media-addiction-analysis-dataset")
    
    print(f"Copying data to {target_dir}...")
    shutil.copytree(cached_path, target_dir, dirs_exist_ok=True)

    print("Done.")
        
if __name__ == "__main__":
    download_data()
