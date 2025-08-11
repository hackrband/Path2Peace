import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os



class ImageAudioApp:
    def __init__(self, root, images, audios):
        self.root = root
        self.root.title("Image Audio Viewer")

        self.images = images
        self.audios = audios
        self.current_index = 0

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Load initial image
        self.image_label = tk.Label(root)
        self.image_label.pack()

        # Buttons for navigation
        self.prev_button = tk.Button(root, text="<< Prev", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(root, text="Next >>", command=self.next_image)
        self.next_button.pack(side=tk.RIGHT)

        # Load the first image and set click event
        self.load_image(self.current_index)
        self.image_label.bind("<Button-1>", self.play_audio)

    def load_image(self, index):
        image_path = self.images[index]
        print(f"Loading image from: {image_path}")  # Debugging line
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference to avoid garbage collection

    def play_audio(self, event):
        audio_path = self.audios[self.current_index]
        print(f"Playing audio from: {audio_path}")  # Debugging line
        if not os.path.exists(audio_path):
            print(f"Error: Audio file not found: {audio_path}")  # Debugging line
            return
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

    def next_image(self):
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.load_image(self.current_index)

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image(self.current_index)


if __name__ == "__main__":
    root = tk.Tk()

    # Get the absolute path of the current directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the actual image files
    images = [
        os.path.join(base_dir, "images", "1.png"),
        os.path.join(base_dir, "images", "105.png"),
        os.path.join(base_dir, "images", "106.png"),
        os.path.join(base_dir, "images", "107.png"),
        os.path.join(base_dir, "images", "108.png"),
        os.path.join(base_dir, "images", "109.png"),
        os.path.join(base_dir, "images", "110.png"),
        os.path.join(base_dir, "images", "111.png"),
        os.path.join(base_dir, "images", "112.png"),
        os.path.join(base_dir, "images", "113.png"),
        os.path.join(base_dir, "images", "114.png")
    ]

    # Specify the corresponding audio files
    audios = [
        os.path.join(base_dir, "mp3", "1.mp3"),
        os.path.join(base_dir, "mp3", "105.mp3"),
        os.path.join(base_dir, "mp3", "106.mp3"),
        os.path.join(base_dir, "mp3", "107.mp3"),
        os.path.join(base_dir, "mp3", "108.mp3"),
        os.path.join(base_dir, "mp3", "109.mp3"),
        os.path.join(base_dir, "mp3", "110.mp3"),
        os.path.join(base_dir, "mp3", "111.mp3"),
        os.path.join(base_dir, "mp3", "112.mp3"),
        os.path.join(base_dir, "mp3", "113.mp3"),
        os.path.join(base_dir, "mp3", "114.mp3")
    ]

    print(f"Image paths: {images}")  # Debugging line
    print(f"Audio paths: {audios}")  # Debugging line

    app = ImageAudioApp(root, images, audios)
    root.mainloop()

# Changes Made:
# Added a check in the play_audio method to see if the audio file exists, and print an error message if it does not.
# Adjusted the paths to match the structure shown in your screenshot (using mp3 instead of audio).
# Ensure the folder names and paths are correctly set as per your project directory structure. This debugging information will help pinpoint if the paths are being constructed correctly or if there are any discrepancies.
__init__.py
