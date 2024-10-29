import numpy as np
import cv2 as cv
import os
import argparse
import pickle


def load_images_from_path(img_path):
    """
    Load images from the specified directory.
    
    Parameters:
        img_path (str): Path to the directory containing images.
        
    Returns:
        list: List of loaded images.
    """
    images = []
    for filename in sorted(os.listdir(img_path)):
        file_path = os.path.join(img_path, filename)
        img = cv.imread(file_path)
        if img is not None:
            images.append(img)
    return images

def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    """
    Calibrate the camera using chessboard pattern images.
    
    Parameters:
        images (list): List of images for calibration.
        board_pattern (tuple): Chessboard pattern as (columns, rows).
        board_cellsize (float): Size of each chessboard cell in meters.
        K (np.array): Initial camera matrix (optional).
        dist_coeff (np.array): Initial distortion coefficients (optional).
        calib_flags (int): Calibration flags (optional).
        
    Returns:
        rms (float): Root mean square error of the calibration.
        K (np.array): Camera matrix.
        dist_coeff (np.array): Distortion coefficients.
        rvecs (list): Rotation vectors.
        tvecs (list): Translation vectors.
    """
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0, "No corners found in any images!"

    # Prepare 3D points of the chessboard
    obj_pts = [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points)

    # Calibrate the camera
    return cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)
\
def save_calibration_data(calibration_data, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(calibration_data, f)
    print(f"Calibration data saved to {file_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Camera calibration using chessboard images.')
    parser.add_argument('img_path', type=str, help='Path to the directory containing images.')
    parser.add_argument('board_pattern', type=int, nargs=2, help='Chessboard pattern as two integers: columns rows.')
    parser.add_argument('--board_cellsize', type=float, default=0.0025, help='Size of each chessboard cell in meters (default: 0.0025).')
    parser.add_argument('save_path', type=str, help='Path to save calibration results.')
    args = parser.parse_args()

    # Load images from the specified path
    images = load_images_from_path(args.img_path)
    assert len(images) > 0, "No images found in the specified directory!"

    # Perform camera calibration
    board_pattern = tuple(args.board_pattern)
    rms, K, dist_coeff, rvecs, tvecs,  = calib_camera_from_chessboard(images, board_pattern, args.board_cellsize)
    calibration_data = {
        'rvecs': rvecs,
        'tvecs': tvecs,
        'rms': rms,
        'K': K,
        'dist_coeff': dist_coeff
    }

    save_calibration_data(calibration_data, args.save_path)
    
    # Print calibration results
    print('## Camera Calibration Results')
    print(f'* The number of selected images = {len(images)}')
    print(f'* RMS error = {rms}')
    print(f'* Camera matrix (K) = \n{K}')
    print(f'* Distortion coefficient (k1, k2, p1, p2, k3, ...) = {dist_coeff.flatten()}')
    # print("Rotation vectors (rvecs):", rvecs)
    # print("Translation vectors (tvecs):", tvecs)
