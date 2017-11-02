# -*- coding: utf-8 -*-
""" Heart Rate Calculations utilities module
This module is in charge of providing utilities for calculating heart beat rates.
"""
import logging
from inspect import getargspec

import numpy as np

import fft
import video_utils

_logger = logging.getLogger(__name__)

_HERTZ_PER_MINUTE = 60


def measure(video, roi, min_freq, max_freq, channel='G'):
    """ Measures the heart beat rate in the given video, customizing the process according to the given params.

    Params:
        video (Video): The video to analyze.
        roi (tuple): A 4-dimensional tuple holding each of the vertexes of a rectangular ROI.
                     Note: The first two elements define the height, and the second two, the width.
                     This means that roi[0] is the upper left corner, roi[1] is the lower left corner,
                     roi[2] is the upper right corner, and roi[3] is the lower right corner.
        upper_left_vertex (tuple): A tuple of two elements (in which both are integers),
                                    representing a point in the frame to be considered as the upper left vertex of the
                                    rectangular ROI.
                                    Note: The orientation is (row, column).
        roi_height (int): The height of the ROI
        roi_width (int): The width of the ROI.
        min_freq (float): The min. frequency to use in the bandpass filtering applied to the video signal.
        max_freq (float): The max. frequency to use in the bandpass filtering applied to the video signal.
        channel (str): The channel to process.
    Returns:
        float: The average heart beat rate that could be measured from the given video.
    """
    # Verify params...
    if video is None or not isinstance(video, video_utils.Video):
        _logger.debug("Could not measure heart beat rate. Video is null or not a Video instance")
        raise ValueError("The video not be null and must be a Video instance")
    if video.length == 0:
        _logger.debug("Video length is 0")
        raise ValueError("The video is empty")
    if channel is None or not isinstance(channel, str):
        _logger.debug("Could not measure heart beat rate. Channel is null or not a string instance")
        raise ValueError("The channel must not be null and must be a string")

    # Prepare stuff...
    _logger.info("Preparing stuff to measure heart beat rate from video...")
    length = 2 ** int(np.log2(video.length))  # Get the previous power of 2 from the given video
    half_length = length / 2
    frequencies = np.linspace(-half_length, half_length - 1, length) * video.fps / length

    # Signal processing...
    frames = _get_channel_signal(video, channel)[:length]  # Get just the first elements
    signal = _create_signal(frames, roi, video.height, video.width)  # Will validate the ROI
    processed_signal = _process_signal(signal)
    # noinspection PyTypeChecker
    filtered_signal = _filter_signal(processed_signal, [_create_bandpass_filter(frequencies, min_freq, max_freq)])

    _logger.info("Calculating average heart beat rate...")
    # noinspection PyTypeChecker
    return abs(frequencies[np.argmax(filtered_signal)]) * _HERTZ_PER_MINUTE


def _get_channel_signal(video, channel):
    """ Gets the specified channel from the given video.
    This method assumes that type validations over the arguments was already done.

    Params:
        video (Video): The video from which the signal is extracted.
        channel (str): The channel to be extracted.
    Returns:
        ndarray: The signal extracted from the channel video.
    """
    if channel == 'R':
        _logger.info("Getting frames from the R channel...")
        return video.r
    if channel == 'G':
        _logger.info("Getting frames from the G channel...")
        return video.g
    if channel == 'B':
        _logger.info("Getting frames from the B channel...")
        return video.b

    _logger.debug("A wrong channel was passed. Must be 'R', 'G' or 'B', but was {}".format(channel))
    raise ValueError("The channel was wrong. Must be 'R', 'G' or 'B")


def _create_signal(frames, roi, video_height, video_width):
    """ Creates the signal to be processed from the given list of frames.

    Params:
        frames (list): The list of frames from where the signal will be created. We assume all frames has same shape.
        roi (tuple): A 4-dimensional tuple holding each of the vertexes of a rectangular ROI.
                     Note: The first two elements define the height, and the second two, the width.
                     This means that roi[0] is the upper left corner, roi[1] is the lower left corner,
                     roi[2] is the upper right corner, and roi[3] is the lower right corner.
        video_height (int): The video height
        video_width (int): The video width
    Returns:
        array: The created signal.
    """
    # Validate param...
    if frames is None or not isinstance(frames, list) or not frames:
        _logger.debug("The frames was null, was not a list or was an empty list")
        raise ValueError("The frames must be a non empty list")
    if roi is None or not isinstance(roi, tuple) or len(roi) != 4 or not all(isinstance(vertex, int) for vertex in roi):
        _logger.debug("Wrong ROI definition. Must be a 4-Dimensional tuple of ints")
        raise ValueError("Invalid ROI definition. Must be a 4-Dimensional tuple of ints")

    if roi[0] < 0 or roi[1] >= video_height or roi[2] < 0 or roi[3] >= video_width:
        _logger.debug("The ROI is out of range")
        raise ValueError("Wrong ROI. Is out of range")

    _logger.info("Getting ROI from frames...")
    roi_frames = map(lambda frame: _get_roi(frame, roi), frames)
    _logger.info("Mapping ROI frames to mean value...")
    raw_signal = map(lambda roi_frame: np.mean(roi_frame), roi_frames)  # Calculate the mean of the ROI
    _logger.info("Calculating mean of the raw signal...")
    raw_signal_mean = np.mean(raw_signal)  # Calculate the mean of the signal to be substracted to it

    _logger.info("Creating signal to process...")
    return np.array(map(lambda point: point - raw_signal_mean, raw_signal))  # Creates the final signal to be processed


def _get_roi(frame, roi):
    """ Extracts the ROI from the given frame.
    Note: The ROI is rectangular.
    Note: We assume validations were already performed when execution of this method is reached.

    Params:
        frame (array): A 2-dimensional numpy array representing a frame.
        roi (tuple): A 4-dimensional tuple holding each of the vertexes of a rectangular ROI.
                     Note: The first two elements define the height, and the second two, the width.
                     This means that roi[0] is the upper left corner, roi[1] is the lower left corner,
                     roi[2] is the upper right corner, and roi[3] is the lower right corner.
    Returns:
        array: A new frame, representing the ROI of the given frame.
    """
    return frame[roi[0]:roi[1], roi[2]:roi[3]]


def _process_signal(signal):
    """ Process the given signal, transforming it into the frequency domain.
    Params:
        signal (array): The signal to be processed:
    Returns:
        array: The processed signal
    """
    # Validate param...
    if signal is None or not isinstance(signal, np.ndarray):
        _logger.error("Could not process signal. Must not be null, and must be instance of numpy's array")
        raise ValueError("The signal must not be null and must be a numpy array")

    _logger.info("Processing signal...")
    return np.abs(fft.fftshift(fft.fft(signal))) ** 2  # Calculate spectral density


def _filter_signal(signal, filters=None):
    """ Applies the given filters to the given signal.
    Params:
        signal (array): The signal to be filtered.
        filters (list): A List of functions that receive only one argument (the signal)
                        that represent the filtering function
    Returns:
        array: The filtered signal.
    """
    # Validate params...
    if signal is None or not isinstance(signal, np.ndarray):
        _logger.error("The signal must not be null, and must be represented as a numpy array.")
        raise ValueError("Wrong type for signal")
    if filters is None:
        filters = []
    invalid_filters = filter(lambda filter_function: len(getargspec(filter_function).args) != 1, filters)
    if invalid_filters:
        _logger.debug("A filter which does not receive only one argument was tried to be used.")
        raise ValueError("All filters should receive one argument (the signal to be filtered)")

    _logger.info("Filtering processed signal...")
    # Apply all filters
    for f in filters:
        new_signal = f(signal)
        if new_signal is None or not isinstance(new_signal, np.ndarray) or signal.shape != new_signal.shape:
            _logger.error("One of the filters did not returned a numpy array or was not the same shape")
            raise ValueError("Tried to apply a wrong filter")
        signal = new_signal

    return signal


def _create_bandpass_filter(freqs, min_freq, max_freq):
    """ Creates a bandpass filter (a filter that passes frequencies between a min. and a max. value).
    Params:
        freqs (ndarray): An array containing the frequencies.
        min_freq (float): The minimum frequency the filter will pass.
        max_freq (float): The maximum frequency the filter will pass.
    Returns:
        function: A function that takes a signal and returns the filtered signal, applying bandpass filtering.
    """
    if freqs is None or not isinstance(freqs, np.ndarray) or not len(freqs.shape) == 1:
        _logger.debug("Wrong frequencies value. Must be a one dimensional numpy array")
        raise ValueError("The given frequencies are invalid")
    if min_freq is None or not isinstance(min_freq, float):
        _logger.debug("Wrong min frequency value. Must be a float")
        raise ValueError("The given min. frequency is invalid. Must be a float")
    if max_freq is None or not isinstance(max_freq, float):
        _logger.debug("Wrong max frequency value. Must be a float")
        raise ValueError("The given max. frequency is invalid. Must be a float")
    if max_freq < min_freq:
        _logger.debug("Wrong min/max frequencies value. The max. frequency must not be smaller than the max. frequency")
        raise ValueError("The given min and max. frequencies pair is invalid. "
                         "The max. frequency must not be smaller than the max. frequency")

    # Create anonymous function that takes a signal as argument and applies the filtering to it
    length = freqs.shape[0]
    return lambda signal: np.array([signal[i] if min_freq <= freqs[i] <= max_freq else 0.0 for i in range(length)])
