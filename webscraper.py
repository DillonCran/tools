import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

# How to validate url
# urlparse() function parses a URL into six components, we just need to see if the netloc (domain name) and scheme (protocol) are there.
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Function to get all images from a url
urls = []
def get_all_images(url):
    soup = bs(requests.get(url).content, "html.parser")
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    return urls

        
# Function to download images
def download_images(url, pathname):
    #If no path, make one
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # get all images in chunks
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))  
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

# Main function
def main(url, path):
    imgs = get_all_images(url)
    for img in imgs:
        # for each img, download it
        download_images(img, path)

# Run the main function
main('https://www.limitlesstcg.com/cards/SSP', 
     '/media/dillon/TOSHIBA EXT/Projects/pokedilly/card-images/sw-sh/ssp')









