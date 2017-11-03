# -*- coding: utf-8 -*-
import argparse
import logging
import sys

import heart_rate_utils
import video_utils
from heart_rate import __version__

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    # Basic arguments
    parser = argparse.ArgumentParser(description="Heart Rate")
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version='heart_rate {ver}.'.format(ver=__version__))
    parser.add_argument(
        '-v',
        '--verbose',
        dest="log_level",
        help="Set log level to INFO.",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="log_level",
        help="Set log level to DEBUG.",
        action='store_const',
        const=logging.DEBUG)

    # Video Arguments
    parser.add_argument(
        '-vp',
        '--video-path',
        dest="video_path",
        help="Set that path to the video to analyze.",
        action='store',
        type=str)

    # Heart Beat measure arguments
    parser.add_argument(
        '-rUL',
        '--roi-upper-limit',
        dest="roi_upper_limit",
        help="Set upper left corner of the rectangular ROI.",
        action='store',
        type=int)
    parser.add_argument(
        '-rLL',
        '--roi-lower-limit',
        dest="roi_lower_limit",
        help="Set lower left corner of the rectangular ROI.",
        action='store',
        type=int)
    parser.add_argument(
        '-rlL',
        '--roi-left-limit',
        dest="roi_left_limit",
        help="Set upper right corner of the rectangular ROI.",
        action='store',
        type=int)
    parser.add_argument(
        '-rrL',
        '--roi-right-limit',
        dest="roi_right_limit",
        help="Set lower right corner of the rectangular ROI.",
        action='store',
        type=int)
    parser.add_argument(
        '-mF',
        '--min-freq',
        dest="min_freq",
        help="Set the minimum frequency for the bandpass filter.",
        action='store',
        type=float)
    parser.add_argument(
        '-MF',
        '--max-freq',
        dest="max_freq",
        help="Set the maximum frequency for the bandpass filter.",
        action='store',
        type=float)
    parser.add_argument(
        '-R',
        '--red',
        dest="channel",
        help="Set the channel to be processed to RED.",
        action='store_const',
        const="R")
    parser.add_argument(
        '-G',
        '--green',
        dest="channel",
        help="Set the channel to be processed to GREEN.",
        action='store_const',
        const="G")
    parser.add_argument(
        '-B',
        '--blue',
        dest="channel",
        help="Set the channel to be processed to BLUE.",
        action='store_const',
        const="R")

    # Set default values
    parser.set_defaults(log_level=logging.WARN)
    parser.set_defaults(video_path="./video")
    parser.set_defaults(min_freq=0.4)
    parser.set_defaults(max_freq=7.0)
    parser.set_defaults(channel="G")

    return parser.parse_args(args)


def setup_logging(log_level):
    """Setup basic logging

    Args:
      log_level (int): minimum log level for emitting messages
    """
    logging.basicConfig(level=log_level,
                        stream=sys.stdout,
                        format="[%(asctime)s] %(levelname)s:%(name)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.log_level)
    _logger.info("Starting application...")

    try:
        video = video_utils.Video(args.video_path)
    except Exception as e:
        _logger.error("Could not create video instance. Error message is: \"{}\"".format(e.message))
        exit(1)

    roi = (args.roi_upper_limit, args.roi_lower_limit, args.roi_left_limit, args.roi_right_limit)
    min_freq = args.min_freq
    max_freq = args.max_freq
    channel = args.channel
    try:
        # noinspection PyUnboundLocalVariable
        result = heart_rate_utils.measure(video, roi, min_freq, max_freq, channel)
        print("Average heart beat rate is {}".format(result))
    except Exception as e:
        _logger.error("Could not measure heart beat rate. Exception message was {}".format(e.message))
        exit(1)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
