import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pytube import YouTube, Playlist
from moviepy.editor import *
import os

def download_video(url, folder, progress_callback):
    try:
        video = YouTube(url)
        stream = video.streams.filter(only_audio=True).first()
        out_file = stream.download(output_path=folder)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        clip = AudioFileClip(out_file)
        clip.write_audiofile(new_file)
        clip.close()
        os.remove(out_file)  # Remove the original download
        progress_callback()
        print(f"Downloaded and converted {new_file}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def download_playlist(url, folder, progress):
    try:
        pl = Playlist(url)
        total_videos = len(pl.video_urls)
        print(f"Total videos found: {total_videos}")  # Check how many videos are found
        progress['maximum'] = total_videos
        for video_url in pl.video_urls:
            print(f"Processing {video_url}")  # Output each video URL being processed
            download_video(video_url, folder, lambda: progress.step(1))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download playlist: {str(e)}")

def start_download():
    url = url_entry.get()
    folder = folder_path.get()
    if not url or not folder:
        messagebox.showerror("Error", "Please fill in all fields")
        return
    progress_bar['value'] = 0
    if "list=" in url:
        threading.Thread(target=download_playlist, args=(url, folder, progress_bar)).start()
    else:
        threading.Thread(target=download_video, args=(url, folder, lambda: progress_bar.step(100))).start()

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

app = tk.Tk()
app.title("YouTube Downloader and Converter")

main_frame = ttk.Frame(app, padding="30")
main_frame.grid()

url_label = ttk.Label(main_frame, text="YouTube URL or Playlist:")
url_label.grid(column=0, row=0, sticky=tk.W)
url_entry = ttk.Entry(main_frame, width=50)
url_entry.grid(column=1, row=0, padx=5, pady=5)

folder_label = ttk.Label(main_frame, text="Save to Folder:")
folder_label.grid(column=0, row=1, sticky=tk.W)
folder_path = tk.StringVar()
folder_entry = ttk.Entry(main_frame, textvariable=folder_path, width=47)
folder_entry.grid(column=1, row=1, padx=5)
folder_button = ttk.Button(main_frame, text="Browse", command=select_folder)
folder_button.grid(column=2, row=1, padx=5)

progress_bar = ttk.Progressbar(main_frame, length=400)
progress_bar.grid(column=0, row=2, columnspan=3, pady=20)

download_button = ttk.Button(main_frame, text="Download", command=start_download)
download_button.grid(column=1, row=3, pady=20)

app.mainloop()
