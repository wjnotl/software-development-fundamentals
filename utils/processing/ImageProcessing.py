import io
import os
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps, UnidentifiedImageError


def circular_crop(path, width=100, height=100):
    img = Image.open(path).convert("RGBA").resize((width, height), Image.LANCZOS)

    # Create a same size mask with a white circle
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)

    # Apply mask to image
    result = ImageOps.fit(img, (width, height), centering=(0.5, 0.5))
    result.putalpha(mask)

    # Convert to CTkImage
    return ctk.CTkImage(result, size=(width, height))


def prepare_post_image(path, width=324, height=243):
    img = Image.open(path).convert("RGBA")
    img_width, img_height = img.size

    # Calculate image aspect ratio
    aspect_ratio = img_width / img_height

    # Target aspect ratio: 4:3
    if aspect_ratio >= (4 / 3):
        # Wider than 4:3 => fix width to 324
        new_width = width
        new_height = int(width / aspect_ratio)
    else:
        # Taller than 4:3 => fix height to 243
        new_height = height
        new_width = int(height * aspect_ratio)

    # Resize the image
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)

    if aspect_ratio >= (4 / 3):
        # Wider than 4:3 => return resized image
        return ctk.CTkImage(resized_img, size=(new_width, new_height))
    else:
        # Taller than 4:3 => create a gray canvas and paste the resized image at the center
        canvas = Image.new("RGBA", (width, height), "#666666")
        paste_x = (width - new_width) // 2
        paste_y = (height - new_height) // 2
        canvas.paste(resized_img, (paste_x, paste_y), resized_img)
        return ctk.CTkImage(canvas, size=(width, height))


def get_image_size_in_bytes(pil_image):
    try:
        with io.BytesIO() as buffer:
            pil_image.save(buffer, format="PNG")
            return buffer.tell()
    except (OSError, ValueError, UnidentifiedImageError) as e:
        return f"Error while saving image to memory: {e}"


def limit_image_size(ctk_image, max_mb):
    try:
        if ctk_image is not None:
            if not isinstance(ctk_image, ctk.CTkImage):
                raise ValueError("Image must be a CTkImage object")

            pil_image = ctk_image._light_image
            size = get_image_size_in_bytes(pil_image)
            if isinstance(size, str):
                raise ValueError(size)
            if size > max_mb * 1024 * 1024:
                raise ValueError(f"Image cannot be larger than {max_mb}MB")
    except ValueError as e:
        return str(e)
    return None


def remove_image_from_storage(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        return None
    except PermissionError:
        return "Permission denied while removing the file"
    except Exception as e:
        return "Unexpected error while removing the file: " + str(e)
    return None


def save_image_to_storage(ctk_image, path):
    try:
        pil_image = ctk_image._light_image
        pil_image.convert("RGBA").save(path, format="PNG")
    except OSError as e:
        return "Error while saving the image: " + str(e)
    except PermissionError:
        return "Permission denied while saving the image"
    except Exception as e:
        return "Unexpected error while saving the image: " + str(e)
    return None
