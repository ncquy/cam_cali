# Camera Calibration

This project performs camera calibration using images with chessboard patterns to determine intrinsic and extrinsic parameters. The results are essential for applications requiring accurate camera models, such as 3D reconstruction and augmented reality.

## Table of Contents
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Results and Report](#results-and-report)
- [Acknowledgments](#acknowledgments)

## Requirements
- Python 3.x
- OpenCV
- NumPy
- Matplotlib

1. Clone the repository:

   ```bash
   git clone https://github.com/ncquy/camera_calibration
   cd camera_calibration

2. Install the required packages:
   ```bash
   pip install -r requirements.txt

## Project Structure
- `data/`: Contains the raw chessboard images used for calibration.
- `results/`: Stores the output images and calibration results.
- `image_selection.py`: Script for selecting and processing images for calibration.
- `camera_calibration.py`: Script to perform camera calibration, calculate intrinsic parameters, and compute RMS error.
- `visualize.py`: Script for visualizing undistorted images and camera poses.

## Usage
1. Select and Process Images:
   Use `image_selection.py` to filter and preprocess chessboard images for calibration.
   ```bash
   python image_selection.py -video_file 'data/video/logitech.mp4' -board_pattern 9 6 -save_path 'data/img'


2. Run Camera Calibration:
   Execute `camera_calibration.py` to perform camera calibration. This script will calculate the intrinsic parameters and save them in `results/`.
   ```bash
   python camera_calibration.py 'data/img' 9 6 1 'results/cali_result.json'
  

3. Visualize Results:
   Run visualize.py to display undistorted images and visualize the camera poses in 3D.
   ```bash
   python visualize_camera_pose.py 'results/cali.json'


## Results and Report
1. The chessboard image example with corners.
<p align='center'>
  <img width="400px" src="https://github.com/ncquy/camera_calibration/blob/main/data/img_coner.png" />
  <br/>
  <i> The example shows a chessboard image with corners.</i>
</p>

2.  The number of utilized images, RMS error, and the camera intrinsic parameters:
The results after testing different models are summarized in the table below.
<p align='center'>
  <img width="600px" src="https://github.com/ncquy/camera_calibration/blob/main/data/cali_results.png" />
  <br/>
  <i> The number of utilized images, RMS error, and K.</i>
</p>

3.  The undistorted image:
<p align='center'>
  <img width="600px" src="https://github.com/ncquy/camera_calibration/blob/main/data/undistort.png" />
  <br/>
  <i> The undistorted image.</i>
</p>

4.  Camera position visualization:
<p align='center'>
  <img width="200px" src="https://github.com/ncquy/camera_calibration/blob/main/data/cam_pos.png" />
  <br/>
  <i> The visualization of the camera position in 3D space.</i>
</p>

### Authors
* [Nguyen Cong Quy](https://github.com/ncquy)

