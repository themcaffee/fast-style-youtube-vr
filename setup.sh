#!/bin/bash
# Simple script that __should__ install all of the necessary dependencies to run
# STILL EXPERIMENTAL
# USE AT YOUR OWN RISK


# Verify the user actually wants to run this script
function ask_yes_or_no() {
    read -p "$1 ([y]es or [N]o): "
    case $(echo $REPLY | tr '[A-Z]' '[a-z]') in
        y|yes) echo "yes" ;;
        *)     echo "no" ;;
    esac
}
echo "Neural Styles Youtube VR Ubuntu 16.04 w/ GPU acceleration install script"
echo "This is script is going to take a really long time so get a cup of coffee (or four)."
echo "If running in an ec2 instance, it is maybe possible (untested) to run this in a "
echo "smaller and cheaper instance before the expensive compute instances."
echo "It is also very untested so USE AT YOUR OWN RISK"
if [[ "no" == $(ask_yes_or_no "Are you sure?") || \
      "no" == $(ask_yes_or_no "Are you *really* sure?") ]]
then
    echo "Skipped."
    exit 0
fi


echo "Creating work directory"
mkdir ~/.fast_style_youtube_vr
cd ~/.fast_style_youtube_vr
mkdir unprocessed_videos
mkdir cut_videos
mkdir processed_videos
mkdir metadata_videos
mkdir small_files
mkdir models

echo "Getting fast-style-transfer"
wget https://github.com/lengstrom/fast-style-transfer/archive/master.zip
unzip master.zip
rm master.zip

echo "Install fast style transfer dependencies"
sudo apt-get install -y python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
sudo pip install scipy
sudo pip install Pillow

echo "Getting spatial-media"
wget https://github.com/google/spatial-media/archive/master.zip
unzip master.zip
rm master.zip

echo "Installing youtube-upload"
sudo apt-get install -y google-api-python-client progressbar2
wget https://github.com/tokland/youtube-upload/archive/master.zip
unzip master.zip
rm master.zip
cd youtube-upload-master
sudo python setup.py install

echo "Installing youtube-dl"
sudo apt-get install -y youtube-dl


echo "Finished."
echo "You will need to follow the rest of the steps in setup to complete the install"
