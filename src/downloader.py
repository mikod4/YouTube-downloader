import yt_dlp
from typing import Any

def download(link, opts):
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([link])
        return "Download completed successfully."
    except Exception as e:
        return f"Download failed: {e}"

def getResolutions(link: str) -> list[str]:
    """Fetches available heights and returns them as strings for CTkOptionMenu."""
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(link, download=False)
            formats = info.get('formats', [])
            
            # Extract heights, remove None, and sort descending
            heights = sorted(list(set(
                f['height'] for f in formats if f.get('height') is not None
            )), reverse=True)
            
            # Convert to strings with 'p' (e.g., "1080p") to avoid CTk ljust errors
            return [f"{h}p" for h in heights]
    except Exception:
        return ["Error fetching resolutions"]

def getAudioOptions(path: str, hook: Any) -> dict[str, Any]:
    return {
        "format": "bestaudio/best",
        "outtmpl": f"{path}/%(title)s.%(ext)s",
        "progress_hooks": [hook],
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

def getVideoOptions(path: str, resolution: str, hook: Any) -> dict[str, Any]:
    # Strip the 'p' from "1080p" to get the integer height for the filter
    res_num = resolution.replace("p", "")
    chosen_format = f"bestvideo[height<={res_num}]+bestaudio/best"

    return {
        "format": chosen_format,
        "outtmpl": f"{path}/%(title)s.%(ext)s",
        "progress_hooks": [hook],
        # merge_output_format ensures you get an .mp4 or .mkv
        "merge_output_format": "mp4", 
    }