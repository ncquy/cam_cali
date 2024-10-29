import cv2 as cv
import argparse

def select_img_from_video(video_file, board_pattern, select_all=False, wait_msec=10, wnd_name='Camera Calibration'):
    """
    Select images from video based on board pattern.
    
    Parameters:
        video_file (str): Path to the input video file.
        board_pattern (tuple): Chessboard pattern as a tuple (columns, rows).
        select_all (bool): If True, select all frames. If False, allows manual selection.
        wait_msec (int): Delay in milliseconds between frames.
        wnd_name (str): Name of the display window.
        
    Returns:
        list: Selected images from the video.
    """
    # Open a video
    video = cv.VideoCapture(video_file)
    assert video.isOpened(), f"Cannot open video file: {video_file}"

    # Select images
    img_select = []
    while True:
        # Grab an image from the video
        valid, img = video.read()
        if not valid:
            break

        if select_all:
            img_select.append(img)
        else:
            # Show the image
            display = img.copy()
            cv.putText(display, f'NSelect: {len(img_select)}', (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
            cv.imshow(wnd_name, display)

            # Process the key event
            key = cv.waitKey(wait_msec)
            if key == ord(' '):  # Space: Pause and show corners
                complete, pts = cv.findChessboardCorners(img, board_pattern)
                cv.drawChessboardCorners(display, board_pattern, pts, complete)
                cv.imshow(wnd_name, display)
                key = cv.waitKey()
                if key == ord('\r'):
                    img_select.append(img)  # Enter: Select the image
            if key == 27:  # ESC: Exit (Complete image selection)
                break

    cv.destroyAllWindows()
    return img_select

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select images from a video file for camera calibration.')
    parser.add_argument('video_file', type=str, help='Path to the input video file')
    parser.add_argument('cols', type=int, help='Number of inner corners per a chessboard row')
    parser.add_argument('rows', type=int, help='Number of inner corners per a chessboard column')
    parser.add_argument('--select_all', action='store_true', help='Select all frames without manual input')
    parser.add_argument('--wait_msec', type=int, default=10, help='Delay in milliseconds between frames')
    args = parser.parse_args()

    board_pattern = (args.cols, args.rows)
    selected_images = select_img_from_video(args.video_file, board_pattern, select_all=args.select_all, wait_msec=args.wait_msec)

    print(f'Total selected images: {len(selected_images)}')
