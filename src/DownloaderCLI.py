import sys
from typing import Any, Callable

try:
    import yt_dlp
except ImportError:
    sys.exit("Install requirements first")


class Downloader:
    def __init__(self) -> None:
        self.running = True
        self.path = ""

    def run(self) -> None:
        self.path = self.getDownloadPath() or "."
        while self.running:
            self.menu()

    def getSelection(self, allowed: list[int]) -> int:
        while True:
            try:
                selection = int(input("\nSelect: "))
                if selection in allowed:
                    return selection

                options = f"{allowed[0]}-{allowed[-1]}"
                print(f"\nIncorrect selection, please select {options}")
            except ValueError:
                print("\nInvalid input, please enter a number")

    def menu(self) -> None:
        print("\n===Menu===")
        print(f"Current path: {self.path}")
        print("1. Change download path")
        print("2. Download")
        print("3. Exit")

        selection = self.getSelection([1, 2, 3])

        if selection == 1:
            self.path = self.getDownloadPath() or "."
        elif selection == 2:
            self.download(self.getLink(), self.path, self.getDownloadType())
        else:
            print("\nGoodbye!")
            self.running = False

    def getDownloadType(self) -> Callable[[str], dict[str, Any]]:
        print("\nSelect download type: \n1. Video \n2. Audio")
        selection = self.getSelection([1, 2])

        if selection == 1:
            return self.getVideoOptions

        return self.getAudioOptions

    def getDownloadPath(self) -> str:
        return input("\nEnter download path: ")

    def getLink(self) -> str:
        return input("\nEnter YouTube link: ")


    def getVideoOptions(self, path: str, link: str) -> dict[str, Any]:
        chosen_format = self.selectResolution(link)

        return {
            "format": chosen_format,
            "outtmpl": f"{path}/%(title)s.%(ext)s",
        }
