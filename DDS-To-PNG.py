import os
import time
from PIL import Image
import numpy as np
import cv2  # OpenCV contrib library
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

def process_image_with_pillow_and_opencv(dds_path, output_directory):
    try:
        # Load the .dds image using Pillow
        img = Image.open(dds_path)

        # Convert the image to RGB (OpenCV supports this format)
        img_rgb = img.convert("RGB")
        
        # Convert the image to a numpy array (required for OpenCV)
        img_array = np.array(img_rgb)

        # Flip the image vertically using OpenCV
        flipped_vertically = cv2.flip(img_array, 0)

        # Construct the output path
        output_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(dds_path))[0]}.png")

        # Save the flipped image as PNG using OpenCV
        cv2.imwrite(output_path, flipped_vertically)
        return True  # Return success
    except Exception as e:
        print(f"Failed to process {dds_path}: {e}")
        return False  # Return failure

def convert_dds_to_png_with_pillow_and_opencv(directory):
    # Ensure the output directory exists
    output_directory = os.path.join(directory, "converted_png")
    os.makedirs(output_directory, exist_ok=True)

    # List all .dds files in the directory
    dds_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.dds')]

    # Get the number of CPU cores (for parallel processing)
    max_threads = multiprocessing.cpu_count()

    start_time = time.time()  # Record start time
    print(f"Found {len(dds_files)} .dds images to process.")
    print(f"Using {max_threads} threads.")

    # Parallel processing with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit tasks to the executor
        results = list(executor.map(lambda dds_file: process_image_with_pillow_and_opencv(dds_file, output_directory), dds_files))

    # Calculate statistics
    converted_count = sum(results)
    end_time = time.time()  # Record end time

    # Print summary
    print(f"Conversion completed.")
    print(f"Total images processed: {len(dds_files)}")
    print(f"Successfully converted: {converted_count}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    directory = input("Enter the directory containing .dds images: ")
    convert_dds_to_png_with_pillow_and_opencv(directory)
