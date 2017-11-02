# -*- coding: utf-8 -*-
""" Video utilities module
This module is in charge of providing utilities for loading videos into memory.
"""
import logging
import os

import cv2

_logger = logging.getLogger(__name__)


class Video:
    """ Class representing a video loaded using OpenCV
    """

    def __init__(self, path_to_video):
        """ Creates a new Video instance. This will load into memory the video.

        Args:
            path_to_video (str): The path to the video to analyze.
        Returns:
            A new video instance.
        Raises:
            ValueError: If the given path_to_video is None, is not a string, or is an empty string.
            IOError: If the given path_to_video is not a file.
        """
        # Check type and validate the given path_to_video
        if path_to_video is None or not isinstance(path_to_video, str) or not path_to_video:
            _logger.debug("The given path to the video is not valid")
            raise ValueError("None, non string or empty string path to video")

        # Check a file exists with the given path_to_file name
        if not os.path.isfile(path_to_video):
            _logger.debug("The given path to the video is not a file")
            raise IOError("'{}' is not a file".format(path_to_video))

        video_capture = cv2.VideoCapture(path_to_video)
        if not video_capture.isOpened():
            _logger.debug("Could not open video")
            raise IOError("Could not open '{}' file".format(path_to_video))

        _logger.debug("Reading video properties...")
        self._length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self._width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._fps = video_capture.get(cv2.CAP_PROP_FPS)
        _logger.debug("Video properties read successfully")

        _logger.debug("Reading video frames...")
        self._b = []
        self._g = []
        self._r = []
        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if ret:
                self._b += [frame[:, :, 0]]
                self._g += [frame[:, :, 1]]
                self._r += [frame[:, :, 2]]
            else:
                break
        _logger.debug("Video frames read successfully")

        _logger.debug("Closing CV2...")
        video_capture.release()
        cv2.destroyAllWindows()
        _logger.debug("CV2 closes successfully...")

        _logger.info("Video instance created successfully")

    @property
    def length(self):
        """
        Returns:
            The length of the video (i.e the amount of frames).
        """
        return self._length

    @property
    def width(self):
        """
        Returns:
            The video width.
        """
        return self._width

    @property
    def height(self):
        """
        Returns:
            The video height.
        """
        return self._height

    @property
    def fps(self):
        """
        Returns:
            The amount of frames per second
        """
        return self._fps

    @property
    def b(self):
        """
        Returns:
            The 'B' video frames.
        """
        return self._b

    @property
    def g(self):
        """
        Returns:
            The 'G' video frames.
        """
        return self._g

    @property
    def r(self):
        """
        Returns:
            The 'R' video frames.
        """
        return self._r
