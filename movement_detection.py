import cv2
import numpy as np

bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

def detect_movement(frame):
    fg_mask = bg_subtractor.apply(frame)

    kernel = np.ones((5,5), np.uint8)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

    movement_pixels = cv2.countNonZero(fg_mask)

    return movement_pixels > 1500
