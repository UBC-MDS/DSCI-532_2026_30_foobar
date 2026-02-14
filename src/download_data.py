import os
import kagglehub

def download_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '../data/raw/')
    os.makedirs(data_dir, exist_ok=True)

    kagglehub.dataset_download(
        "zahranusratt/student-social-media-addiction-analysis-dataset",
        output_dir = data_dir)
        
if __name__ == "__main__":
    download_data()
