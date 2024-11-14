import cv2
import numpy as np

def calculate_distance_in_kilometers(image_path):
    pixels_per_meter = 1
    # Step 1: Load the image
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: Image not found.")
        return
    
    # Step 2: Convert the image to grayscale for edge detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Step 3: Apply Gaussian blur to smooth the image (helps with edge detection)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    # Step 4: Apply Canny Edge Detection to detect the road edges
    edges = cv2.Canny(blurred_image, 50, 150)
    
    # Step 5: Detect the contours (boundaries) of the road
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        print("Error: No contours found.")
        return
    
    # Find the largest contour which likely corresponds to the road
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Step 6: Get the bounding rectangle around the road contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Step 7: Measure the width of the road in pixels
    road_length_in_pixels = h  # For vertical roads, you can take height (h)
    
    # Optional: Draw the detected contour and bounding box for visual confirmation
    cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    
    
    # Step 8: Convert pixel length to meters using the scale (pixels per meter)
    road_length_in_meters = road_length_in_pixels / pixels_per_meter

    return road_length_in_meters/100

# Example usage:
image_path = './uploads/th.jpg'

road_length_in_kilometers = calculate_distance_in_kilometers(image_path)
