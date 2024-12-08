
# DDS to PNG Converter for KSP

This script is designed to convert `.dds` image files (used in **Kerbal Space Program** or KSP) to `.png` format. It utilizes **Pillow** for image handling and **OpenCV** for parallel processing, making the conversion fast and efficient.

## Features:
- Converts `.dds` files to `.png` format.
- Flips images vertically as part of the conversion process.
- Utilizes parallel processing based on the number of available CPU cores, significantly speeding up the process for large numbers of images.
- Generates a new directory (`converted_png`) to save the converted `.png` files.

## Requirements:
- Python 3.x
- **Pillow**: for handling `.dds` files.
- **OpenCV** (contrib version): for image flipping and saving.
- **Multiprocessing**: to speed up conversion by using parallel threads based on your CPU cores.

## How It Works:
- The script reads `.dds` image files from the specified directory.
- It uses **Pillow** to open and convert the `.dds` files to RGB format.
- The images are flipped vertically using **OpenCV**.
- The converted images are then saved as `.png` files in a new directory named `converted_png` under the input directory.
- The script dynamically adjusts the number of parallel threads used based on the number of CPU cores available on the system.

## Installation:

1. **Clone this repository** or download the script to your machine.

2. **Install the required Python libraries**:
   You can install the required libraries using `pip`:
   ```bash
   pip install Pillow opencv-contrib-python
   ```

## Usage:

1. **Run the script**:
   Navigate to the directory where the script is located and run it using Python:
   ```bash
   python dds_to_png_converter.py
   ```

2. **Input Directory**:
   The script will prompt you to enter the directory containing the `.dds` files. Enter the full path to the folder containing the `.dds` files you want to convert.

3. **Output Directory**:
   The converted `.png` files will be saved in a folder named `converted_png` within the directory you specify.

4. **Processing**:
   The script will process all `.dds` files in the provided directory, flip them vertically, convert them to `.png`, and save them in the `converted_png` folder.

5. **Processing Speed**:
   The script will automatically use the maximum number of threads available on your CPU to process the images in parallel, speeding up the conversion for large sets of files.

6. **Output**:
   After conversion, the script will display:
   - The number of `.dds` images found.
   - The number of successfully converted images.
   - The total time taken for the conversion process.

## Example:

```bash
Enter the directory containing .dds images: C:\Users\Username\KSP\Textures
```

After running the script, the images in the `C:\Users\Username\KSP\Textures` directory will be converted to `.png` and saved in `C:\Users\Username\KSP\Textures\converted_png`.

## Script Details:

- **Dynamic Threading**: The script automatically determines the number of available CPU cores and uses that number of threads for parallel processing to speed up the conversion process.
- **Vertical Flip**: All images are flipped vertically using OpenCV to maintain the proper orientation for KSP textures.

## Example Output:

```bash
Found 50 .dds images to process.
Using 8 threads.
Conversion completed.
Total images processed: 50
Successfully converted: 50
Time taken: 15.32 seconds
```

## License:

This script is free to use and modify. However, make sure to credit ChatGPT for writing the initial version.

## Thanks to ChatGPT:

A special thanks to **ChatGPT** for writing this script and providing assistance in optimizing the image processing using Python, Pillow, and OpenCV.

