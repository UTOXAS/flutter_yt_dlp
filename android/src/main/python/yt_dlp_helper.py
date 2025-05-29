import yt_dlp
import json
import os
import logging
from io import StringIO

# Configure logging with DEBUG level for detailed output
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LogCapture(StringIO):
    """Captures yt-dlp output for logging."""

    def write(self, message):
        if message.strip():
            logger.debug(f"yt-dlp output: {message.strip()}")


def extract_format_info(format_data):
    """Extracts format info from yt-dlp data."""
    return {
        "formatId": format_data.get("format_id", "unknown"),
        "ext": format_data.get("ext", "unknown"),
        "resolution": (
            format_data.get("resolution", "unknown")
            if format_data.get("vcodec", "none") != "none"
            else "audio only"
        ),
        "bitrate": int(format_data.get("tbr", 0) or 0),
        "size": int(
            format_data.get("filesize", 0) or format_data.get("filesize_approx", 0) or 0
        ),
        "vcodec": format_data.get("vcodec", "none"),
        "acodec": format_data.get("acodec", "none"),
    }


def get_video_info(url):
    """Fetches video metadata and formats."""
    ydl_opts = {
        "quiet": True,
        "format": "bestvideo+bestaudio/best",
        "logger": logger,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_info = {
                "title": info.get("title", "unknown_video"),
                "thumbnail": info.get("thumbnail"),
                "formats": [extract_format_info(f) for f in info.get("formats", [])],
            }
            logger.info(f"Fetched info for {url}: {len(video_info['formats'])} formats")
            return json.dumps(video_info)
    except Exception as e:
        logger.error(f"Error fetching info for {url}: {str(e)}")
        return json.dumps({"title": "unknown_video", "thumbnail": None, "formats": []})


def download_format(url, format_id, output_path, overwrite, progress_callback):
    """Downloads a specific format with progress updates."""
    log_capture = LogCapture()

    def progress_hook(d):
        status = d.get("status")
        if status == "downloading":
            downloaded = int(d.get("downloaded_bytes", 0))  # Convert to int
            total = int(
                d.get("total_bytes", d.get("total_bytes_estimate", 0) or 0)
            )  # Convert to int
            if total > 0:
                logger.info(f"Progress for {url}: {downloaded}/{total} bytes")
                progress_callback.onProgress(downloaded, total)
        elif status == "finished":
            total = int(
                d.get("total_bytes", d.get("total_bytes_estimate", 0) or 0)
            )  # Convert to int
            logger.info(f"Download finished for {url}: {total} bytes")
            progress_callback.onProgress(total, total)
        elif status == "error":
            logger.error(f"Download error for {url}: {d.get('error')}")

    ydl_opts = {
        "format": format_id,
        "outtmpl": output_path,
        "progress_hooks": [progress_hook],
        "force_overwrites": overwrite,
        "noprogress": False,
        "quiet": False,  # Allow yt-dlp output for debugging
        "logger": logger,
        "verbose": True,  # Enable verbose output for debugging
        "logtostderr": True,  # Ensure logs go to stderr
        "errfile": log_capture,  # Capture errors
        "outfile": log_capture,  # Capture output
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Starting download: {url} format {format_id} to {output_path}")
            ydl.download([url])
            logger.info(f"Download completed for {url}")
    except Exception as e:
        logger.error(f"Download failed for {url}: {str(e)}")
        raise
