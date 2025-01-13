import os
import time
import sys
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

def convert_dds_to_png(dds_path, output_directory, format_aspect_ratio=None):
    """
    Converts a single DDS file to PNG, flipping it vertically. Optionally formats it to a specified aspect ratio.
    """
    try:
        # Open the DDS file with Pillow
        with Image.open(dds_path) as img:
            # Flip vertically
            img = img.transpose(method=Image.FLIP_TOP_BOTTOM)

            if format_aspect_ratio:
                # Calculate the new dimensions for the specified aspect ratio
                width, height = img.size
                aspect_width, aspect_height = format_aspect_ratio
                new_width = width
                new_height = int(width * aspect_height / aspect_width)

                if new_height > height:
                    new_height = height
                    new_width = int(height * aspect_width / aspect_height)

                # Center crop or pad to match the aspect ratio
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Construct output path
            output_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(dds_path))[0]}.png")

            # Save as PNG
            img.save(output_path, "PNG")

        return f"Converted: {os.path.basename(dds_path)}"
    except Exception as e:
        return f"Failed to process {dds_path}: {e}"

def process_dds_directory(input_directory, output_directory, format_aspect_ratio=None):
    """
    Converts all DDS files in a directory to PNG using parallel processing.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Find all DDS files in the directory
    dds_files = [os.path.join(input_directory, f) for f in os.listdir(input_directory) if f.lower().endswith(".dds")]

    if not dds_files:
        print("No DDS files found in the directory.")
        return

    print(f"Found {len(dds_files)} .dds files to process.")

    # Get the number of threads equal to the CPU core count
    num_threads = multiprocessing.cpu_count()
    print(f"Using {num_threads} threads.")

    start_time = time.time()

    # Process files in parallel
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {
            executor.submit(convert_dds_to_png, dds_file, output_directory, format_aspect_ratio): dds_file
            for dds_file in dds_files
        }
        for future in as_completed(futures):
            print(future.result())

    end_time = time.time()
    print(f"Processing completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    # Check for command line arguments
    args = sys.argv[1:]
    format_aspect_ratio = None

    if "-background" in args:
        format_aspect_ratio = (16, 9)
        print("Using default aspect ratio: 16:9")

    if "-aspect_ratio" in args:
        try:
            aspect_index = args.index("-aspect_ratio")
            aspect_ratio = args[aspect_index + 1]
            width, height = map(int, aspect_ratio.split(":"))
            format_aspect_ratio = (width, height)
        except (IndexError, ValueError):
            print("Invalid aspect ratio format. Use -aspect_ratio WIDTH:HEIGHT (e.g., 16:9).")
            sys.exit(1)

    input_dir = input("Enter the directory containing .dds images: ").strip()
    output_dir = os.path.join(input_dir, "converted_png")

    process_dds_directory(input_dir, output_dir, format_aspect_ratio)