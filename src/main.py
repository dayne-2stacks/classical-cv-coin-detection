
import cv2
import numpy as np
import sys

def get_average_color(image, circle):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.circle(mask, (circle[0], circle[1]), circle[2], 255, -1) # Mark a filled circle where coin is 
    mean = cv2.mean(image, mask=mask)  # Get the average color inside the circle
    return mean[:3]  # Return the RGB average

def hough_circle_transform(image, min_radius, max_radius, threshold):
    # Apply gaussian blur to smooth image
    image =cv2.GaussianBlur(image, (5, 5), 0)
    # Compute sin and cos values for samples of theta
    theta_values = np.arange(0, 360, 1)
    cos_theta = np.cos(np.deg2rad(theta_values))
    sin_theta = np.sin(np.deg2rad(theta_values))

    # Perform Canny edge detection 
    edges = cv2.Canny(image, 100, 200)
    y_indexes, x_indexes = np.nonzero(edges)  # Get coordinates of all edges

    height, width = edges.shape
    
    votes = np.zeros((height, width, max_radius), dtype=np.uint64)

    # Apply Hough transform only on edge regions 
    for r in range(min_radius, max_radius):
        # create an array of possible lengths of x and y for each degree theta sampled for each radius 
        x_vals = (np.expand_dims(x_indexes, axis=1) - r * cos_theta).astype(np.int32)  
        y_vals = (np.expand_dims(y_indexes, axis=1) - r * sin_theta).astype(np.int32)  

        # ensure that x and y values from a pixel would be a valid point
        valid_indexes = (x_vals >= 0) & (x_vals < width) & (y_vals >= 0) & (y_vals < height)

        # Update votes for valid coordinates
        for rad in range(len(theta_values)): 
            # 0th Dim - edge location, 1st Dim - length of x and y per given theta 
            valid_x = x_vals[:, rad][valid_indexes[:, rad]] # Filter out invalid x vand y values
            valid_y = y_vals[:, rad][valid_indexes[:, rad]] 
            votes[valid_y, valid_x, r] += 1 # vote for a ray in the directions x, y and magnitude of r 

    detected_circles = [] # array to store circles
    region_mask = np.zeros((height, width), dtype=np.uint8)

    # normalize votes to a value between 0 and 1
    if np.amax(votes) != 0:
        votes = votes/np.amax(votes)

    # Search for circles, but only keep the largest circle in each region
    for r in range(max_radius - 1, min_radius - 1, -1):
        for y in range(height):
            for x in range(width):
                # If circle is voted enough times and the area doesnt have an existing circle, add circle
                if votes[y, x, r] >= threshold and region_mask[y, x] == 0:
                    # Mark the region as visited
                    cv2.circle(region_mask, (x, y), int(r * 1.5), 1, thickness=-1)
                    # Add circle to detected
                    detected_circles.append((x, y, r))

    return detected_circles


# Function to classify coins based on radius and color
def classify_coin(image, circle, color_threshold=15):
    radius = circle[2]
    # Get the average color inside the circle
    avg_color = get_average_color(image, circle)
    # If color is more red than green and blue by a certain threshold it is a penny
    if avg_color[2] > avg_color[1] + color_threshold and avg_color[2] > avg_color[0] + color_threshold: 
        return 1
    elif radius in [20, 21, 22]: # range for nickels
        return 5
    elif radius in [19, 18]: # range for dimes
        return 10
    elif radius in [26, 25, 24, 23]: # range for quarters
        return 25
    else:
        return "Unknown"

def main():
# Read the image file name from standard input
    image_file = input().strip()

    # Read the image
    image = cv2.imread(image_file)
    if image is None:
        print(f"Error: Could not read image {image_file}")
        sys.exit(1)


    # Downsample by a factor of 5 
    height, width = image.shape[:2]
    new_width = width // 5  
    new_height = height // 5

    # Resize the image
    downsampled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    # Define minimum and maximum radius for downsampled photos for coins and a voting threshold
    min_radius = 18  
    max_radius = 27 
    threshold = 0.65  

    # Find the minimum and maximum pixel values
    min_value = np.min(downsampled_image)
    max_value = np.max(downsampled_image)

    # Apply the normalization to increase contrast
    normalized_image = (((downsampled_image - min_value) / (max_value - min_value)) * 255).astype(np.uint8)

    # Detect circles
    circles = hough_circle_transform(normalized_image, min_radius, max_radius, threshold)

    # Output the results with classification
    print(f"{len(circles)}")
    for circle in circles:
        coin_type = classify_coin(downsampled_image, circle)
        print(f"{circle[0]*5} {circle[1]*5} {coin_type}") 

if __name__ == "__main__":
    main()
