from __future__ import print_function
import subprocess
from subprocess import CalledProcessError
import os
import glob

# Base folder for processing videos
HOME_PATH = os.path.expanduser("~")
WORK_FOLDER = HOME_PATH + "/.fast_style_youtube_vr"

# Subfolders for each step
UNPROCESSED_FOLDER = WORK_FOLDER + "/unprocessed_videos/"
UNPROCESSED_INPUT = UNPROCESSED_FOLDER + "%(id)s"
CUT_FOLDER = WORK_FOLDER + "/cut_videos/"
PROCESSED_FOLDER = WORK_FOLDER + "/processed_videos/"
METADATA_FOLDER = WORK_FOLDER + "/metadata_videos/"
SMALLFILE_FOLDER = WORK_FOLDER + "/small_files/"
MODEL_FOLDER = WORK_FOLDER + "/models/"

# Location of fast style project
FAST_STYLE_LOCATION = WORK_FOLDER + '/fast-style-transfer-master/'
TRANSFORM_LOCATION = FAST_STYLE_LOCATION + "transform_video.py"

# Script location to add 360 video headers
METADATA_SCRIPT = WORK_FOLDER + "/spatial-media-master/spatialmedia"

# Location of youtube json secrets file for user to upload as
YOUTUBE_SECRETS = WORK_FOLDER + "/youtube.json"


def style_video(url, model, start_time, duration, video_title=None, video_description=None, dry_run=False, skip_cleanup=False):
    """
    Downloads a youtube VR video, cuts it, styles it, and reuploads it

    :param url: The full youtube URL to the video
    :param model: The name of the .ckpt model
    :param start_time: The time in the video to start the cut
    :param duration: How long the video cut should be
    :param video_title: The Youtube title of the uploaded result (optional)
    :param video_description: The Youtube description of the uploaded result (optional)
    :param dry_run: If true, styling is skipped. For testing all other steps before lengthy style step. (optional)
    :param skip_cleanup: Skip removing the created video files at the end. (optional)
    """
    # Get the video from youtube
    _download_youtube_video(url)
    video_file = url.split("?v=")[-1] + ".mp4"

    # Cut it to desired length
    in_path = UNPROCESSED_FOLDER + video_file
    out_path = CUT_FOLDER + video_file
    _cut_video(in_path, out_path, start_time, duration)

    # Style it using model
    in_path = CUT_FOLDER + video_file
    out_path = PROCESSED_FOLDER + video_file
    model_location = MODEL_FOLDER + model + ".ckpt"
    if dry_run:
        _move_video(in_path, out_path)
    else:
        _style_video(in_path, out_path, model_location)

    # Add youtube 360 metadata
    in_path = SMALLFILE_FOLDER + video_file
    out_path = METADATA_FOLDER + video_file
    _add_metadata_to_video(in_path, out_path)

    # Upload to youtube
    in_path = METADATA_FOLDER + video_file
    if not video_title:
        video_title = video_file + " styled for " + model
    if not video_description:
        video_description = "Created with Fast Style for Youtube VR Videos (https://github.com/themcaffee/fast-style-youtube-vr)."
    _upload_video(in_path, video_title, video_description)

    # Cleanup work directories
    if not skip_cleanup:
        _cleanup_folders([UNPROCESSED_FOLDER, CUT_FOLDER, PROCESSED_FOLDER, SMALLFILE_FOLDER])


def _download_youtube_video(url):
    """
    Download the given youtube video in mp4 format. If there is no available mp4 format, there will be an error.

    :param url: The full youtube url of the video
    """
    youtube_dl_cmd = ["youtube-dl",
                      "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
                      "--restrict-filenames",
                      "--output=" + UNPROCESSED_INPUT + "",
                      url]
    _run_process_helper("Downloading from youtube", youtube_dl_cmd)


def _cut_video(in_path, out_path, start_time, duration):
    """
    Cut a video using ffmpeg

    :param video_name: The video name to cut
    :param start_time: When to start the cut. Format '00:00:00'
    :param duration: Number of seconds after start to cut
    """
    cut_cmd = ["ffmpeg",
               "-y",
               "-v", "error",
               "-i", str(in_path),
               "-ss", str(start_time),
               "-strict", "-2",
               "-t", str(duration),
               "-async", "1",
               out_path]

    _run_process_helper("Cutting to desired length", cut_cmd)


def _style_video(in_path, out_path, model_location, fast_style_location=FAST_STYLE_LOCATION):
    """
    Uses fast style transfer to style a video using a given model.

    :param in_path: The current path of the video to style
    :param out_path: The destination of the styled video
    :param model_location: The location of the .ckpt model file
    :param fast_style_location: The location of the fast style project folder. (Optional)
    """
    # TODO Check for model file existence
    transform_cmd = ["python transform_video.py",
                     "--checkpoint " + model_location,
                     "--in-path " + in_path,
                     "--out-path " + out_path]

    # Run transform
    os.chdir(fast_style_location)
    concat_cmd = " ".join(transform_cmd)
    _run_process_helper("Styling video", concat_cmd, shell=True)


def _add_metadata_to_video(in_path, out_path, metadata_script=METADATA_SCRIPT):
    """
    Adds the VR video metadata necessary for youtube to recognize that this video is a VR video

    :param in_path: The current path of the video to add the metadata to
    :param out_path: The destination of the video with metadata headers
    :param metadata_script: The path of the script to add the youtube metadata headers
    """
    metadata_cmd = ["python", metadata_script,
                    "-i", in_path,
                    out_path]
    _run_process_helper("Adding metadata to video", metadata_cmd)


def _upload_video(in_path, video_title, video_description, youtube_secrets=YOUTUBE_SECRETS):
    """
    Upload the video to youtube

    :param in_path: The current path of the video to upload
    :param video_title: The title of the video on Youtube
    :param video_description: The description of the video on Youtube. (Optional)
    :param youtube_secrets: The path of the user's youtube json secrets file (Optional)
    """
    # Upload to youtube
    youtube_cmd = ["youtube-upload",
                   "--client-secrets", youtube_secrets,
                   "--title", video_title,
                   "--description", video_description,
                   in_path]
    _run_process_helper("Uploading to youtube", youtube_cmd)


def _cleanup_folders(folders):
    """
    Remove all of the mp4s in the given folders

    :param folders: List of folders to look in
    """
    for folder in folders:
        for fl in glob.glob(folder + "*.mp4"):
            print ("Removing file: " + fl)
            os.remove(fl)


def _move_video(in_path, out_path):
    """
    Move a video file to a new location

    :param in_path: The current path of the video file
    :param out_path: The desired location of the video file
    """
    subprocess.check_call(["mv", in_path, out_path])


def _run_process_helper(name, command, shell=False):
    """
    Helper to run shell commands and give useful output about the command state

    :param name: Name of the current step
    :param command: The command to execute
    :param shell: Execute as shell
    :return: The result of the command
    """
    try:
        print ("Running step: " + name)
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=shell)

        print ("Finished step: " + name)
        if output:
            print ("Command output: " + str(output))

        return output
    except CalledProcessError as err:
        # Print out useful information
        print ("Failure on step: " + name)
        print ("Output: " + err.output)
        print ("cmd: " + ' '.join(map(str, err.cmd)))
        print ("returncode: " + str(err.returncode))
        raise err
