import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Function to download an image
def download_image(img_url, filename):
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"[✓] Image saved as {filename}")
        else:
            print(f"[X] Error downloading image from {img_url}")
    except Exception as e:
        print(f"[X] Exception while downloading image: {e}")

# Get the name of the file with the links
links_file = input("Enter the name of the .txt file with the links: ").strip()

# Read the links from the file
try:
    with open(links_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"[X] File '{links_file}' not found.")
    exit()

print(f"Found {len(urls)} URLs in the file.")

# Create folder to save images
os.makedirs('images', exist_ok=True)

# For each URL in the file
for base_url in urls:
    print(f"\n>>> Processing: {base_url}")

    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links within the class 'gt200'
        gt200_links = soup.select('.gt200 a')
        print(f" - Found {len(gt200_links)} links in class 'gt200'.")

        for i, a in enumerate(gt200_links, 1):
            link = urljoin(base_url, a.get('href'))
            print(f"   [{i}] Accessing: {link}")

            try:
                link_response = requests.get(link)
                link_soup = BeautifulSoup(link_response.text, 'html.parser')

                div_i1 = link_soup.find('div', id='i1')
                if not div_i1:
                    print("     [!] Div id='i1' not found.")
                    continue

                div_i3 = div_i1.find('div', id='i3')
                if not div_i3:
                    print("     [!] Div id='i3' not found.")
                    continue

                img_tag = div_i3.find('img', id='img')
                if not img_tag or not img_tag.get('src'):
                    print("     [!] Image with id='img' not found.")
                    continue

                img_url = urljoin(link, img_tag['src'])
                filename = os.path.join('images', f"image_{i}_{os.path.basename(link).split('.')[0]}.jpg")
                download_image(img_url, filename)

            except Exception as e:
                print(f"     [X] Error accessing inner link: {e}")

    except Exception as e:
        print(f"[X] Error processing main URL: {e}")
