# YouTube downloader
import os

try:
    from pytube import YouTube
except ImportError:
    os.system("pip install pytube")

if __name__ == "__main__":
    download_path = input("Enter download path: ")
    allowed = [1, 2]

    while True:
        link = input("\nEnter YouTube link: ")
        print("\nLooking for your video...\n")

        yt = YouTube(link)
        print(yt.title)

        pick = int(input("\n1. Video\n2. Audio\nOption: "))

        while pick not in allowed:
            pick = int(input("\n1. Video\n2. Audio\nOption: "))

        print("\nDownloading...\n")

        if pick == 1:
            yd = yt.streams.get_highest_resolution()
            yd.download(download_path)
        elif pick == 2:
            yd = yt.streams.get_audio_only()
            yd.download(download_path)

        print("\nDownload Complete\n")
        print("To download again press Y, anything else is considered as program exit.\n")
        choice = input("Enter your choice: ")
        if type(choice) is str and choice.lower() != "y":
            break
