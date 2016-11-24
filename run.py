import argparse

from fast_style_youtube_vr import style_video


def _str_to_bool(string):
    """
    Converts command line boolean string to python boolean
    :param string: The command line string
    :return: The boolean interpretation of the string
    """
    return string.lower() in ("yes", "true", "t", "1")


if __name__ == "__main__":
    # Get command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Full Youtube URL. (required)")
    parser.add_argument("--model", help="Model name to stylize as. (required)")
    parser.add_argument("--start-time", help="[hh:mm:ss] The time to start at in the video. (required)")
    parser.add_argument("--duration", help="Length of video to process in seconds. (required)", type=int)
    parser.add_argument("--video-description", help="The Youtube description of the uploaded result. (optional)", default=None)
    parser.add_argument("--video-title", help="The Youtube description of the uploaded result. (optional)", default=None)
    parser.add_argument("--dry-run", help="If yes, skip running the styling script for testing the rest of the steps (optional)", default="false")
    cli_args = parser.parse_args()
    dry_run = _str_to_bool(cli_args.dry_run)

    # Run the process
    style_video(url=cli_args.url, model=cli_args.model, start_time=cli_args.start_time, duration=cli_args.duration,
                video_title=cli_args.video_title, video_description=cli_args.video_description, dry_run=dry_run)


