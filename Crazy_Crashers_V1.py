"""Crazy Crashers game V1. Setting up game basis"""

import pygame
import random
import os


def load_images(folder_path):
    """Loads all images from a folder and returns a dictionary.

  Args:
      folder_path: Path to the folder containing the images.

  Returns:
      A dictionary where the key is the filename (without extension)
       and the value is the loaded image surface.
  """
    images = {}
    for filename in os.listdir(folder_path):
        # Check if it's an image file
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # Get filename without extension
            name, _ = os.path.splitext(filename)
            # Load the image and add it to the dictionary
            image = pygame.image.load(os.path.join(folder_path, filename)) \
                .convert_alpha()
            images[name] = image
    return images


# Example usage
assets_path = os.path.join("assets", "cars")  # Replace with your path
car_images = load_images(assets_path)

# Access images by filename (without extension)
bike_1_image = car_images["bike_1"]
car_10_image = car_images["car_10"]  # Assuming car_10.png exists
truck_3_image = car_images["truck_3"]
