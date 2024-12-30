from PIL import Image, ImageDraw

# Create a new image with a white background
image_size = (132, 132)
image = Image.new("RGB", image_size, "white")

def create_finder_pattern():
    # Create a 14x14 finder pattern
    pattern_size = 14
    finder_pattern = Image.new("RGB", (pattern_size, pattern_size), "black")
    draw = ImageDraw.Draw(finder_pattern)

    draw.line([2, 2, 11, 2], fill="white", width=2) # Top-left horizontal 1
    draw.line([2, 2, 2, 11], fill="white", width=2) # Top-left vertical 1

    draw.line([2, 10, 11, 10], fill="white", width=2) # Bottom-left horizontal 1
    draw.line([10, 2, 10, 11], fill="white", width=2) # Top-right vertical 1

    return finder_pattern

def create_alignment_pattern():
    # Create a 14x14 alignment pattern
    pattern_size = 14
    alignment_pattern = Image.new("RGB", (pattern_size, pattern_size), "black")
    draw = ImageDraw.Draw(alignment_pattern)

    # Draw the alignment pattern (similar to the finder pattern)
    draw.line([2, 2, 11, 2], fill="white", width=2)  # Top-left horizontal
    draw.line([2, 2, 2, 11], fill="white", width=2)  # Top-left vertical
    draw.line([2, 10, 11, 10], fill="white", width=2)  # Bottom-left horizontal
    draw.line([10, 2, 10, 11], fill="white", width=2)  # Top-right vertical

    return alignment_pattern

def paste_finder_patterns(image):
    finder_pattern = create_finder_pattern()
    alignment_pattern = create_alignment_pattern()
    pattern_size = 14  # Size of the finder pattern

    # Paste the finder pattern in the corners
    image.paste(finder_pattern, (0, 0))  # Top-left
    image.paste(finder_pattern, (image.width - pattern_size, 0))  # Top-right
    image.paste(finder_pattern, (0, image.height - pattern_size))  # Bottom-left

    # Paste the alignment pattern at (6, 26)
    image.paste(alignment_pattern, (21*4, 21*4))  # Adjusting for the top-left corner of the alignment pattern

# Paste finder patterns and alignment pattern into the image
paste_finder_patterns(image)

# Display the image with finder patterns
image.show()

