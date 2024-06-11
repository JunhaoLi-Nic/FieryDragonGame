# Packages
import pygame
from classes.utils.image_packager import resource_path

def render_square_image(image: str, size: int):
    """
    Renders an image in square aspect ratio.

    :param image: Path for the image to be rendered
    :param size: The dimensions (px) for the image
    :return: The resized image
    """
    # Loads the provided image file and stores it
    loaded_image = pygame.image.load(resource_path(image))

    # Defines the maximum size of the rendering (to prevent blurring the image)
    max_resolution = max(loaded_image.get_size())

    # Create a float scale to adjust the image size to the desired px (from size parameter)
    scale = size / max_resolution

    # Resize the image to the desired size (in px)
    adjusted_resolution = (int(loaded_image.get_width() * scale), int(loaded_image.get_width() * scale))

    # Create a scaled version of the image using the previous calculation
    transformed_image = pygame.transform.scale(loaded_image, adjusted_resolution)

    # Returns the scaled image to be rendered
    return transformed_image


def render_image(image: str, width: int, height: int):
    """
    Renders an image at the specific size

    :param image: Path for the image to be rendered
    :param width: The dimensions (px) for the width of the image
    :param height: The dimensions (px) for the height of the image
    :return: The resized image
    """

    # Loads the provided image file and stores it
    loaded_image = pygame.image.load(resource_path(image))

    # Resize the image to the desired size (in px)
    adjusted_resolution = (width, height)

    # Create a scaled version of the image
    transformed_image = pygame.transform.scale(loaded_image, adjusted_resolution)

    # Returns the scaled image to be rendered
    return transformed_image
