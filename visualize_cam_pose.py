import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import json
import argparse

def load_calibration_data(file_path):
    """Load calibration data from a specified JSON file."""
    with open(file_path, 'r') as f:
        calibration_data = json.load(f)
    # Convert lists to numpy arrays for further processing
    calibration_data['rvecs'] = [np.array(rvec) for rvec in calibration_data['rvecs']]
    calibration_data['tvecs'] = [np.array(tvec) for tvec in calibration_data['tvecs']]
    calibration_data['K'] = np.array(calibration_data['K'])
    calibration_data['dist_coeff'] = np.array(calibration_data['dist_coeff'])
    return calibration_data

def visualize_cam_pose(obj_pt, rvecs, tvecs):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Draw chessboard points
    ax.scatter(obj_pt[:, 0], obj_pt[:, 1], obj_pt[:, 2], s=50, c='r', marker='+')

    # Draw the camera positions
    for rvec, tvec in zip(rvecs, tvecs):
        # Convert rotation vector to rotation matrix
        R, _ = cv.Rodrigues(rvec)
        
        # Camera position in world coordinates
        camera_position = -R.T @ tvec    

        # Draw a line from the camera center pointing along the z-axis of the camera
        # ax.scatter(camera_position[0], camera_position[1], camera_position[2], s=100, c='b', marker='^')
        # z_axis = R.T @ np.array([[0, 0, 1]]).T
        # ax.quiver(camera_position[0], camera_position[1], camera_position[2],
        #         z_axis[0], z_axis[1], z_axis[2], length=1, color='b')

        # Draw the camera's orientation (X, Y, Z axes)
        x_axis = R.T @ np.array([[1, 0, 0]]).T
        y_axis = R.T @ np.array([[0, 1, 0]]).T
        z_axis = R.T @ np.array([[0, 0, 1]]).T   

        ax.quiver(camera_position[0], camera_position[1], camera_position[2],
                x_axis[0], x_axis[1], x_axis[2], color='r', length=1, label='X axis')
        
        ax.quiver(camera_position[0], camera_position[1], camera_position[2],
                y_axis[0], y_axis[1], y_axis[2], color='g', length=1, label='Y axis')
        
        ax.quiver(camera_position[0], camera_position[1], camera_position[2],
                z_axis[0], z_axis[1], z_axis[2], color='b', length=1, label='Z axis')
    
    # # Add coordinate frame at world origin
    # origin = np.array([0, 0, 0])
    # ax.quiver(origin[0], origin[1], origin[2], 1, 0, 0, color='black', length=1.5)
    # ax.quiver(origin[0], origin[1], origin[2], 0, 1, 0, color='black', length=1.5)
    # ax.quiver(origin[0], origin[1], origin[2], 0, 0, 1, color='black', length=1.5)
    # ax.text(0, 0, 0, 'Origin', color='black')

    # Label the axes
    ax.set_xlabel('X world')
    ax.set_ylabel('Y world')
    ax.set_zlabel('Z world')

    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Visualize camera pose from calibration data.')
    parser.add_argument('calibration_file', type=str, help='Path to the calibration data file.')
    parser.add_argument('board_pattern', type=int, nargs=2, help='Chessboard pattern as two integers: columns rows.')
    args = parser.parse_args()

    # Load the calibration data
    calibration_data = load_calibration_data(args.calibration_file)

    # Generate object points for the chessboard
    rvecs = tuple(np.array(rv) for rv in calibration_data["rvecs"])
    tvecs = tuple(np.array(rv) for rv in calibration_data["tvecs"])
    obj_pt = np.zeros((args.board_pattern[0] * args.board_pattern[1], 3), np.float32)
    obj_pt[:, :2] = np.mgrid[0:args.board_pattern[0], 0:args.board_pattern[1]].T.reshape(-1, 2)
    visualize_cam_pose(obj_pt, rvecs, tvecs)

if __name__ == '__main__':
    main()
