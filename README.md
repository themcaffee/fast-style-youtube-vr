# Fast Style Youtube VR :zap: :art: :video_camera: :sunglasses:

Step inside a virtual world painted by your favorite artist. Simple proof of concept script to download Youtube VR videos, transfer
style using fast style, add metadata, and reupload to Youtube for viewing. Requires a good GPU to finish in reasonable amount of time.

_(Click to go to video. Make sure to use a compatible browser.)_

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
4. Get JSON file of youtube credentials by following youtube-upload's [guide](https://github.com/tokland/youtube-upload#authentication). Put the downloaded json file into `~/fast_style_youtube_vr/youtube.json`.

5. Install [Tensorflow, CUDA, and cuDNN](https://www.tensorflow.org/versions/r0.11/get_started/os_setup.html). If you have a Nvidia GPU, you should also make sure to install the drivers from Nvidia themselves.

6. Download the [pre-generated models](https://drive.google.com/drive/folders/0B9jhaT37ydSyRk9UX0wwX3BpMzQ). Move the models
 into `~/.fast_style_youtube/vr/models`.


## Example Usage

Download and style the video with the scream model that's located in ~/.fast_style_youtube_vr/models/scream.ckpt. This will
take a long time and depends heavily on your gpu power.

```
python run.py --video https://www.youtube.com/watch?v=T_KXSWiPL-4 --model scream --start-time 00:00:30 --duration 30
```

Give the final youtube title and description

```
python run.py --video https://www.youtube.com/watch?v=T_KXSWiPL-4 --model scream --start-time 00:00:30 --duration 30
```

## All available options

--video (required): The full Youtube URL of the video to download.

--model (required): The name of the model file to use to style.

--start-time (required): When to start the cut of the file. Expect format: 00:00:00.

--duration (required): The duration of the cut video in seconds.

--video-title (optional): The title of the uploaded video on Youtube.

--video-description (optional): The description of the uploaded video on Youtube.


## Credits

Thanks to Logan Engstrom ([fast-style-transfer](https://github.com/lengstrom/fast-style-transfer)) for the awesome stylization implementation. (And of course all of the other libraries utilized in this project).
