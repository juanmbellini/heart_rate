# -*- coding: utf-8 -*-
import argparse
import logging
import sys

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

    parser.add_argument(
        '-vp',
        '--video-path',
        dest="video_path",
        help="Set that path to the video to analyze.",
        action='store',
        default="./video",
        type=str)

    return parser.parse_args(args)


def setup_logging(log_level):
    """Setup basic logging

    Args:
      log_level (int): minimum loglevel for emitting messages
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


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
