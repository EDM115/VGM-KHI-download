# VGM-KHI-download
Automatically download all songs from an album from KH Insider's Video Game Music site with format chooser

## Motivation
The [Video Game Music](https://downloads.khinsider.com/) site has a lot of video game music, but it's a pain to download them one by one. This script will download all songs from an album with a format chooser.

> [!IMPORTANT]  
> This script is for educational purposes only. I do not condone piracy. Please support the original artists by purchasing their music.  
> Also, the website have the ability to download all songs from an album in a zip file. If you're interested AND can afford it, donate to them (more info on their [FAQ](https://downloads.khinsider.com/faq)).

## Requirements
Python 3+ (download [here](https://www.python.org/downloads/)) and git to download the repo (or just download the .py file, in such case skip the second command)  
```bash
pip install BeautifulSoup requests
git clone https://github.com/EDM115/VGM-KHI-download.git && cd VGM-KHI-download
```

## Usage
1. Run the script  
```bash
python VGM_DL.py
```
2. Enter the path where you want to save the songs (ex `C:\Users\EDM115\Music\vgm` or `/home/EDM115/Music/vgm`)
3. Enter the URL of the album you want to download (ex `https://downloads.khinsider.com/game-soundtracks/album/watch-dogs-2-original-game-soundtrack-2016`)
4. Let the script fetch all songs links (this takes a while)
5. Choose the format of the songs you want to download (MP3, FLAC, ...) by typing the corresponding number
6. Let the script download all songs

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
