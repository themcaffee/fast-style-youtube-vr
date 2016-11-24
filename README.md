# Fast Style Youtube VR

Step inside a world painted by your favorite artist. Simple proof of concept script to download Youtube VR videos, transfer
style using fast style, add metadata, and reupload to Youtube for viewing.

[![Venice Scream](https://img.youtube.com/vi/jfiGyaFzHug/0.jpg)](https://www.youtube.com/watch?v=jfiGyaFzHug)

[![Venice Rain Princess](https://img.youtube.com/vi/ZuxioQEKw7I/0.jpg)](https://www.youtube.com/watch?v=ZuxioQEKw7I)

[Playlist of short example videos](https://www.youtube.com/watch?v=EwQmQKw1stw&feature=youtu.be&list=PLu1w_GF5s7kvia2T6sYN2zGqzgEYVo4dG)

[Playlist of longer example videos](https://www.youtube.com/playlist?list=PLQ931W8JAdGuiNUvEqvG4x0O0-Fl1P-wM)


## Getting Setup

1. Get the project

```
echo "Get the project"
wget https://github.com/themcaffee/fast-style-youtube-vr/archive/master.zip
unzip master.zip
rm master.zip
cd fast-style-youtube-vr-master
```

2. Install python 2.7 and pip

```
sudo apt-get install -y python-pip python-dev libcurl4-openssl-dev
```

3. Run setup script

```
cd fast-style-youtube-vr-master
./setup.sh
```

4. Get JSON file of youtube credentials by following [youtube-upload's guide](https://github.com/tokland/youtube-upload#authentication).
Put the downloaded json file into `~/fast_style_youtube_vr/youtube.json`.

5. Install (Tensorflow, CUDA, and cuDNN)[https://www.tensorflow.org/versions/r0.11/get_started/os_setup.html). It would also be a good idea to install your graphic card's appropriate Nvidia drivers.

6. Download [pre-generated models](https://drive.google.com/drive/folders/0B9jhaT37ydSyRk9UX0wwX3BpMzQ). Move the models
 into `~/.fast_style_youtube/vr/models`.


## Example Usage

Download and style the video with the scream model that's located in ~/.fast_style_youtube_vr/models/scream.ckpt. This will
take a long time and depends heavily on your gpu power.

```
python run.py --video https://www.youtube.com/watch?v=T_KXSWiPL-4 --model scream
```

Same as above but cut the video starting at 00:00:30 to 30 seconds long before styling

```
python run.py --video https://www.youtube.com/watch?v=T_KXSWiPL-4 --model scream --start-time 00:00:30 --duration 30
```

Give the final youtube title and description

```
python run.py --video https://www.youtube.com/watch?v=T_KXSWiPL-4 --model scream --start-time 00:00:30 --duration 30
```

## All available options

--video : The full Youtube URL of the video to download.

--model : The name of the model file to use to style.

--start-time : When to start the cut of the file. Format: 00:00:00

--duration : The duration of the cut video in seconds.

--video-title : The title of the uploaded video on Youtube.

--video-description : The description of the uploaded video on Youtube.
