import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import random

# Function to generate a random movie index
def get_random_highlight_index(total_movies):
    return random.randint(0, total_movies - 1)

random_highlight_index = None  # Variable to store the random index
# Function to search for movies

# Function to search for movies
def search_movies():
    genre = genre_var.get()
    url = f"https://www.imdb.com/search/title/?genres={genre}&sort=num_votes,desc&title_type=feature&count=50"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Clear the previous results
    for widget in frame.winfo_children():
        widget.destroy()

    # Get all the movies from the search results
    all_movies = soup.select('.lister-item')

    # Randomly select 10 movies from the search results
    random_movies = random.sample(all_movies, 10)

    # Generate a random index
    global random_highlight_index
    random_highlight_index = get_random_highlight_index(len(random_movies))

    for i, movie in enumerate(random_movies):
        title = movie.h3.a.text
        img = movie.find('img')
        if img and 'loadlate' in img.attrs:
            img_url = img['loadlate']
            img = Image.open(requests.get(img_url, stream=True).raw)
            img = img.resize((150, 225))  # Resize image with anti-aliasing
            img = ImageTk.PhotoImage(img)
            movie_images.append(img)

            # Create a frame as a container for image and title
            movie_frame = tk.Frame(frame, padx=5, pady=5)
            movie_frame.grid(row=i // 5, column=i % 5)

            # Add the image to the frame
            img_label = tk.Label(movie_frame, image=img)
            img_label.pack()

            # Add the title label below the image
            title_label = tk.Label(movie_frame, text=title)
            title_label.pack()

            # Apply an outline to the random movie
            if i == random_highlight_index:
                movie_frame.config(borderwidth=3, relief="solid")  # Add an outline

                # Add "Watch This!" label below 
                watch_this_label = tk.Label(movie_frame, text="Watch This!", bg="red", fg="white")
                watch_this_label.pack()

        else:
            movie_images.append(None)

# Create the main window
root = tk.Tk()
root.title("IMDb Movie Search")
# Maximize the window
root.state('zoomed')

# Create a label
label = tk.Label(root, text="Select a Movie Genre:")
label.pack(pady=10)

# Create a genre dropdown
genres = ["Action", "Adventure", "Animation", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi"]
genre_var = tk.StringVar()
genre_dropdown = ttk.Combobox(root, textvariable=genre_var, values=genres)
genre_dropdown.pack(pady=5)
genre_dropdown.set("Action")

# Create a search button
search_button = tk.Button(root, text="Search", command=search_movies)
search_button.pack(pady=5)

# Create a frame to display movie images and titles with 5 columns
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Store movie images
movie_images = []

# Start the Tkinter main loop
root.mainloop()
