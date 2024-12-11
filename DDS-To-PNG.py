import os
import time
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing


def convert_dds_to_png(dds_path, output_directory):
    """
    Converts a single DDS file to PNG, flipping it vertically.
    """
    try:
        # Open the DDS file with Pillow
        with Image.open(dds_path) as img:
            # Flip vertically
            img = img.transpose(method=Image.FLIP_TOP_BOTTOM)

            # Construct output path
            output_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(dds_path))[0]}.png")

            # Save as PNG
            img.save(output_path, "PNG")

        return f"Converted: {os.path.basename(dds_path)}"
    except Exception as e:
        return f"Failed to process {dds_path}: {e}"


def process_dds_directory(input_directory, output_directory):
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
        futures = {executor.submit(convert_dds_to_png, dds_file, output_directory): dds_file for dds_file in dds_files}
        for future in as_completed(futures):
            print(future.result())

    end_time = time.time()
    print(f"Processing completed in {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    input_dir = input("Enter the directory containing .dds images: ").strip()
    output_dir = os.path.join(input_dir, "converted_png")

    process_dds_directory(input_dir, output_dir)
