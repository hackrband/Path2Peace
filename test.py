import threading
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import os
import sys


class Path2Peace:
    def __init__(self, root, images, audios):
        self.root = root
        self.root.title("Image Audio Viewer")
        self.images = images
        self.audios = audios
        self.current_index = 0
        self.is_video_playing = False  # Track if a video is playing

        # Set fixed window size
        self.window_width = 800
        self.window_height = 600
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        # Initialize Pygame mixer
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Error initializing Pygame mixer: {e}")
            sys.exit(1)

        # Ensure resources are cleaned up on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Create a frame for the image and navigation buttons
        self.frame = ttk.Frame(root, padding="10 10 10 10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Image label
        self.image_label = tk.Label(self.frame)
        self.image_label.pack(pady=20, expand=True)

        # Buttons for navigation
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)  # Add padding for visibility

        self.prev_button = ttk.Button(self.button_frame, text="<< Prev", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(self.button_frame, text="Next >>", command=self.next_image)
        self.next_button.pack(side=tk.RIGHT, padx=5)

        # Now load the first image after all widgets are initialized
        self.load_image(self.current_index)
        self.image_label.bind("<Button-1>", self.play_audio)

    def load_image(self, index):
        """Load and display image based on the current index."""
        image_path = self.images[index]
        try:
            image = Image.open(image_path)
            image = self.resize_image(image)
        except FileNotFoundError:
            # Display error message in the UI
            self.image_label.config(text=f"Error: Image not found: {image_path}")
            return
        except Exception as e:
            self.image_label.config(text=f"Error loading image: {e}")
            return

        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep reference to avoid garbage collection

    def resize_image(self, image):
        """Resize the image to fit within the application window."""
        image_ratio = image.width / image.height
        window_ratio = self.window_width / self.window_height
        if image_ratio > window_ratio:
            new_width = self.window_width
            new_height = int(new_width / image_ratio)
        else:
            new_height = self.window_height
            new_width = int(new_height * image_ratio)
        return image.resize((new_width, new_height), Image.LANCZOS)

    def play_audio(self, event):
        """Play audio corresponding to the currently displayed image."""
        if self.is_video_playing:
            return  # Do not play audio if a video is currently playing
        audio_path = self.audios[self.current_index]
        if not os.path.exists(audio_path):
            self.image_label.config(text=f"Error: Audio file not found: {audio_path}")
            return
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error playing audio: {e}")

    def next_image(self):
        """Move to the next image and audio."""
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.load_image(self.current_index)

    def prev_image(self):
        """Move to the previous image and audio."""
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image(self.current_index)

    def play_videos_sequentially(self, video_files):
        """Play videos one after the other in a separate thread."""
        self.video_thread = threading.Thread(target=self._play_videos, args=(video_files,))
        self.video_thread.start()

    def _play_videos(self, video_files):
        """Helper method to play a list of videos."""
        for video_file in video_files:
            self.is_video_playing = True
            self.play_video(video_file)
        # Once videos finish, show the image-audio viewer
        self.is_video_playing = False
        self.start_image_audio_viewer()

    def play_video(self, video_file):
        """Play a single video file."""
        cap = cv2.VideoCapture(video_file)
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                self.show_frame(frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()  # Ensure resources are released

    def show_frame(self, frame):
        """Display each video frame in Tkinter's Label widget safely."""
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = self.resize_image(image)
        photo = ImageTk.PhotoImage(image)
        # Update the image label in the main thread
        self.root.after(0, lambda: self.image_label.config(image=photo))
        self.image_label.image = photo  # Keep a reference to avoid garbage collection

    def start_image_audio_viewer(self):
        """Show the image and audio viewer after videos finish playing."""
        self.load_image(self.current_index)

    def on_exit(self):
        """Cleanup function to close resources on exit."""
        pygame.mixer.quit()  # Quit pygame mixer to release audio resources
        self.root.destroy()  # Destroy the Tkinter root window


if __name__ == "__main__":
    root = tk.Tk()

    # Set up base directory paths for images and audios
    base_dir = os.path.dirname(os.path.abspath(__file__))


    def load_assets(base_dir):
        """Load images and audios dynamically, ensuring pairs."""
        image_dir = os.path.join(base_dir, "images")
        audio_dir = os.path.join(base_dir, "mp3")
        images = sorted([os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.png')])
        audios = sorted([os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.mp3')])
        return images, audios


    images, audios = load_assets(base_dir)
    videos = [os.path.join(base_dir, "mp4", video) for video in ["loading.mp4", "Hello.mp4", "Logo.mp4"]]

    app = Path2Peace(root, images, audios)

    # Play videos sequentially and then start image/audio viewer
    app.play_videos_sequentially(videos)

    root.mainloop()