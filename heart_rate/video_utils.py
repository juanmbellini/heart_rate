# -*- coding: utf-8 -*-
""" Video utilities module
This module is in charge of providing utilities for loading videos into memory.
"""
import logging
import os

import cv2
import numpy as np

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
            raise IOError("{} is not a file".format(path_to_video))

        video_capture = cv2.VideoCapture(path_to_video)

        self._length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self._width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._fps = video_capture.get(cv2.CAP_PROP_FPS)

        self._r = np.zeros((1, self._length))
        self._g = np.zeros((1, self._length))
        self._b = np.zeros((1, self._length))

        k = 0
        while video_capture.isOpened():
            ret, frame = video_capture.read()

            if ret:
                # TODO: define which part of the frame are we taking, or if we are taking the whole frame
                self._r[0, k] = np.mean(frame[330:360, 610:640, 0])
                self._g[0, k] = np.mean(frame[330:360, 610:640, 1])
                self._b[0, k] = np.mean(frame[330:360, 610:640, 2])
            else:
                break
            k = k + 1
        _logger.debug("Video instance created successfully")

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
    def r(self):
        """
        Returns:
            The 'R' video frames.
        """
        return self._r

    @property
    def g(self):
        """
        Returns:
            The 'G' video frames.
        """
        return self._g

    @property
    def b(self):
        """
        Returns:
            The 'B' video frames.
        """
        return self._b
