# classical-cv-coin-detection

## Overview
This project contains a Python program that detects and identifies coins in an input image and calculates their total monetary value in US cents. The program processes images and outputs the number, positions, and values of the detected coins. This program provides an automated method for detecting and counting coins in images. The task involves locating coins and determining their value (in cents) from a given image.

### Coin Types Supported:
- **Quarters:** 25 cents
- **Dimes:** 10 cents
- **Nickels:** 5 cents
- **Pennies:** 1 cent

### Input Format
- The program reads the file path of an input image from standard input.
- Images must be in `.png` format and processed within 10 seconds.

### Output Format
- The program outputs the following:
  1. **N**: Total number of coins detected.
  2. For each detected coin: `X Y V`, where:
     - `X` and `Y`: Center coordinates of the coin in the image (in pixels).
     - `V`: Coin value (1, 5, 10, or 25).

## Input Constraints
1. All coins are fully visible and placed on a monochromatic US letter-size sheet of paper (2159 × 2794 pixels).
2. Images are cropped to the paper region with a 20-pixel margin guaranteed to not contain any coin.
3. No other objects are present in the image.

## Output Example
For an image `1.png`, the program might output:

```
17
390 349 25
986 420 25
1429 611 25
... (additional lines for other coins)
```

## Project Components

### `main.py`
This is the main Python script that implements the coin detection and value calculation logic.

### Key Features:
1. **Image Preprocessing:**
   - Downscales images by a factor of 5 to optimize processing speed.
   - Normalizes image pixel values to enhance contrast.
   - Applies Gaussian blur to smooth the image and reduce noise.

2. **Coin Detection:**
   - Uses a custom implementation of the Hough Circle Transform:
     - Applies edge detection using the Canny algorithm.
     - Votes on potential circle centers and radii.
     - Filters out overlapping circles by keeping the most prominent ones.

3. **Coin Classification:**
   - Determines coin type based on radius and average color:
     - Quarters, dimes, nickels, and pennies have specific radius ranges.
     - Average color within each circle is analyzed to identify pennies.

4. **Output Generation:**
   - Outputs the number of detected coins and their coordinates scaled back to original image dimensions.
   - Outputs the classification of each coin in cents.

### Helper Functions
- **`hough_circle_transform()`**:
  - Implements a custom Hough Circle Transform for detecting circular shapes in the image.
  - Outputs a list of detected circles with their centers and radii.

- **`get_average_color()`**:
  - Computes the average RGB color within a detected circle.
  - Helps classify pennies based on their distinct reddish hue.

- **`classify_coin()`**:
  - Maps radius and color data to specific coin types.
  - Supports error handling for unrecognized coin sizes.

## Benchmarks
### Test Output
----------------------------------------
- **Detection rate:** 94.89% 
- **False alarm rate:** 0.00% 
- **Classification rate:** 97.67% 

## Notes
- Adhere to the 10-second processing time limit for each image.


An improved version was later developed that uses a support vector machine to help with classifying pennies.


