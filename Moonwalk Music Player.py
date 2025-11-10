import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame
import os
import random
from mutagen.mp3 import MP3

# Initialize Pygame mixer
pygame.mixer.init()

# Global variables
playlist_songs = []
current_index = 0
is_paused = False
shuffle_mode = False
repeat_mode = False
song_length = 0

# Functions
def add_songs():
    global playlist_songs
    songs = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
    for song in songs:
        playlist.insert(tk.END, os.path.basename(song))
        playlist_songs.append(song)

def play_song(event=None):
    global is_paused, current_index, song_length
    if not playlist_songs:
        return
    try:
        selected_indices = playlist.curselection()
        if selected_indices:
            current_index = selected_indices[0]
        song = playlist_songs[current_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        is_paused = False
        song_label.config(text=f"Playing: {os.path.basename(song)}")
        # Get song length
        try:
            audio = MP3(song)
            song_length = audio.info.length
        except:
            song_length = 0
        progress_bar.config(to=song_length)
        update_progress()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def stop_song(event=None):
    global is_paused
    pygame.mixer.music.stop()
    song_label.config(text="Stopped")
    progress_bar.set(0)
    is_paused = False

def pause_song(event=None):
    global is_paused
    pygame.mixer.music.pause()
    is_paused = True

def unpause_song(event=None):
    global is_paused
    pygame.mixer.music.unpause()
    is_paused = False

def next_song(event=None):
    global current_index
    if shuffle_mode:
        current_index = random.randint(0, len(playlist_songs) - 1)
    else:
        current_index += 1
        if current_index >= len(playlist_songs):
            current_index = 0 if repeat_mode else len(playlist_songs) - 1
    playlist.selection_clear(0, tk.END)
    playlist.selection_set(current_index)
    play_song()

def previous_song(event=None):
    global current_index
    if shuffle_mode:
        current_index = random.randint(0, len(playlist_songs) - 1)
    else:
        current_index -= 1
        if current_index < 0:
            current_index = len(playlist_songs) - 1 if repeat_mode else 0
    playlist.selection_clear(0, tk.END)
    playlist.selection_set(current_index)
    play_song()

def set_volume(val):
    pygame.mixer.music.set_volume(float(val)/100)

def toggle_shuffle():
    global shuffle_mode
    shuffle_mode = not shuffle_mode
    shuffle_button.config(relief=tk.SUNKEN if shuffle_mode else tk.RAISED)

def toggle_repeat():
    global repeat_mode
    repeat_mode = not repeat_mode
    repeat_button.config(relief=tk.SUNKEN if repeat_mode else tk.RAISED)

def update_progress():
    if pygame.mixer.music.get_busy() and not is_paused:
        try:
            current_pos = pygame.mixer.music.get_pos() / 1000
            progress_bar.set(current_pos)
        except:
            pass
        root.after(500, update_progress)
    elif not is_paused:
        next_song()

def seek_song(event):
    if song_length > 0:
        click_pos = event.x / progress_bar.winfo_width()
        seek_time = click_pos * song_length
        pygame.mixer.music.play(start=seek_time)
        progress_bar.set(seek_time)

def select_song(event):
    try:
        index = playlist.nearest(event.y)
        playlist.selection_clear(0, tk.END)
        playlist.selection_set(index)
        global current_index
        current_index = index
        play_song()
    except IndexError:
        pass

# GUI Setup
root = tk.Tk()
root.title("Moonwalk Music")
root.geometry("700x500")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

# Left Frame for playlist
left_frame = tk.Frame(root, bg="#1e1e1e")
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

playlist_label = tk.Label(left_frame, text="Playlist", bg="#1e1e1e", fg="white", font=("Arial", 14))
playlist_label.pack(pady=5)

playlist = tk.Listbox(left_frame, selectmode=tk.SINGLE, width=30, bg="#2e2e2e", fg="white", font=("Arial", 12))
playlist.pack(pady=5, fill=tk.Y)
playlist.bind("<Double-1>", select_song)

# Right Frame for controls
right_frame = tk.Frame(root, bg="#1e1e1e")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

song_label = tk.Label(right_frame, text="No song playing", bg="#1e1e1e", fg="white", font=("Arial", 12))
song_label.pack(pady=10)

progress_bar = ttk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=400)
progress_bar.pack(pady=10)
progress_bar.bind("<Button-1>", seek_song)

controls_frame = tk.Frame(right_frame, bg="#1e1e1e")
controls_frame.pack(pady=20)

# Buttons
load_button = tk.Button(controls_frame, text="Add Songs", width=10, command=add_songs)
load_button.grid(row=0, column=0, padx=5)

prev_button = tk.Button(controls_frame, text="Prev", width=8, command=previous_song)
prev_button.grid(row=0, column=1, padx=5)

play_button = tk.Button(controls_frame, text="Play", width=8, command=play_song)
play_button.grid(row=0, column=2, padx=5)

pause_button = tk.Button(controls_frame, text="Pause", width=8, command=pause_song)
pause_button.grid(row=0, column=3, padx=5)

resume_button = tk.Button(controls_frame, text="Resume", width=8, command=unpause_song)
resume_button.grid(row=0, column=4, padx=5)

stop_button = tk.Button(controls_frame, text="Stop", width=8, command=stop_song)
stop_button.grid(row=0, column=5, padx=5)

shuffle_button = tk.Button(controls_frame, text="Shuffle", width=8, command=toggle_shuffle)
shuffle_button.grid(row=1, column=1, pady=10)

repeat_button = tk.Button(controls_frame, text="Repeat", width=8, command=toggle_repeat)
repeat_button.grid(row=1, column=3, pady=10)

volume_label = tk.Label(right_frame, text="Volume", bg="#1e1e1e", fg="white")
volume_label.pack(pady=5)
volume_slider = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume, bg="#1e1e1e", fg="white", troughcolor="#3e3e3e")
volume_slider.set(70)
volume_slider.pack(pady=5)

# Key Bindings
root.bind("<space>", lambda e: pause_song() if pygame.mixer.music.get_busy() else play_song())
root.bind("<s>", stop_song)
root.bind("<p>", play_song)
root.bind("<r>", unpause_song)
root.bind("<n>", next_song)
root.bind("<b>", previous_song)
root.bind("<Shift-s>", toggle_shuffle)
root.bind("<Shift-r>", toggle_repeat)

root.mainloop()
