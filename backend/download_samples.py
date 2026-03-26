import requests
import os
import time

def download_images(base_url, folder_path, start_id, count):
    os.makedirs(folder_path, exist_ok=True)
    downloaded = 0
    current_id = start_id
    
    print(f"Starting download into {folder_path}...")
    
    while downloaded < count and current_id < start_id + 2000: # expanded search
        img_name = f"{current_id}.jpg"
        url = f"{base_url}/{img_name}"
        save_path = os.path.join(folder_path, img_name)
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                downloaded += 1
                print(f"  [+] Downloaded {img_name} to {folder_path}")
            else:
                pass
        except Exception as e:
            print(f"  [!] Error downloading {img_name}: {e}")
            
        current_id += 1
        time.sleep(0.2) # Avoid rate limits

    print(f"Finished. Downloaded {downloaded} images to {folder_path}.\n")

if __name__ == "__main__":
    healthy_base = "https://raw.githubusercontent.com/ai-agriculture-circuits-and-systems/paddy_disease_classification/main/data/origin/train_images/normal"
    pest_base = "https://raw.githubusercontent.com/ai-agriculture-circuits-and-systems/paddy_disease_classification/main/data/origin/train_images/brown_spot"

    # Search in sequential blocks
    download_images(healthy_base, "healthy", 100000, 20)
    download_images(pest_base, "pest", 100001, 20) # Brown spot seems to overlap or start higher
