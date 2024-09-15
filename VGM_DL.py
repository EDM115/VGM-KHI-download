import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urljoin

def init(path):
    save_folder = path
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    session = requests.Session()

    return save_folder, session

def download_file(url, folder, session):
    local_filename = unquote(url).split('/')[-1]
    path = os.path.join(folder, local_filename)
    with session.get(url, stream=True) as r:
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1048576):
                f.write(chunk)
    return local_filename

def extract_download_links(start_url, session):
    response = session.get(start_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    table = soup.find("table", id="songlist")
    download_links = []
    formats = []

    if table:
        header = table.find("tr", id="songlist_header")
        if header:
            ths = header.find_all("th", align="right")
            formats = [th.find("b").text for th in ths]

        rows = table.find_all("tr")
        for row in rows:
            if row.get("id") not in ["songlist_header", "songlist_footer"]:
                download_td = row.find("td", class_="playlistDownloadSong")
                if download_td:
                    a_tag = download_td.find('a')
                    if a_tag and a_tag.has_attr("href"):
                        song_page_url = urljoin(start_url, a_tag["href"])
                        song_page_response = session.get(song_page_url)
                        song_page_soup = BeautifulSoup(song_page_response.content, "html.parser")
                        song_download_spans = song_page_soup.find_all("span", class_="songDownloadLink")
                        for span in song_download_spans:
                            if span.parent.name == 'a':
                                download_url = urljoin(song_page_url, span.parent["href"])
                                size_info = span.parent.parent.text.strip()
                                size_match = re.search(r"\d+(\.\d+)?\s*(KB|MB|GB)", size_info)
                                if size_match:
                                    size_info = size_match.group(0)
                                else:
                                    size_info = "0 KB"
                                download_links.append((download_url, size_info))
    
    return download_links, formats

def calculate_total_size(download_links):
    total_size = 0
    size_pattern = re.compile(r"([\d.]+)\s*(KB|MB|GB)")
    for _, size_info in download_links:
        match = size_pattern.search(size_info)
        if match:
            size_value = float(match.group(1))
            size_unit = match.group(2)
            if size_unit == "KB":
                size_value /= 1024
            elif size_unit == "GB":
                size_value *= 1024
            total_size += size_value
    return total_size

def main():
    print("\tWelcome to VGM DL")
    print("This script will download all the songs from a khinsider album")
    folder_input = input("\nEnter the full folder path to save the files\n(ex C:\\Users\\EDM115\\Desktop) :\n")
    folder = folder_input.replace("\\", "/")
    save_folder, session = init(folder)
    url_input = ""
    while url_input == "":
        url_input = input("\nEnter the full URL of the page to download from\n(ex : https://downloads.khinsider.com/game-soundtracks/album/watch-dogs-2-original-game-soundtrack-2016) :\n")
        if not re.match(r"https://downloads.khinsider.com/game-soundtracks/album/.*", url_input):
            print("Invalid URL, please enter a valid one")
            url_input = ""
    start_url = url_input
    
    print(f"\nListing all files to download... (this will take a while, the more files there are in the album, the longer it will take)")
    download_links, formats = extract_download_links(start_url, session)
    
    if not download_links:
        print("No download links found")
        print("\t(c) 2024 EDM115")
        return
    
    format_sizes = {}
    for fmt in formats:
        chosen_links = [link for link in download_links if fmt.lower() in link[0].split(".")[-1].lower()]
        format_sizes[fmt] = calculate_total_size(chosen_links)

    print("\nAvailable formats :")
    for i, fmt in enumerate(formats):
        print(f"\t{i + 1} : {fmt} ({format_sizes[fmt]:.2f} MB)")
    
    choice = -1
    while choice == -1:
        choice = input("Enter the number of the format you want to download : ")
        if not choice.isdigit():
            print("Invalid choice, please enter a number")
            choice = -1
        else:
            choice = int(choice) - 1
            if choice < 0 or choice >= len(formats):
                print("Invalid choice, please enter a valid number")
                choice = -1
    chosen_format = formats[choice]
    
    chosen_links = [link for link in download_links if chosen_format.lower() in link[0].split(".")[-1].lower()]
    print(f"\nChosen format : {chosen_format}")
    total_size = format_sizes[chosen_format]
    print(f"Total size to download : {total_size:.2f} MB\n")
    
    for url, _ in chosen_links:
        print(f"Downloading : {unquote(url)}")
        download_file(url, save_folder, session)
    
    print("\nAll files downloaded successfully !")
    print("\t(c) 2024 EDM115")

if __name__ == "__main__":
    main()
