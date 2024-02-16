docker rm -f facewine
xhost +
docker run -it \
--gpus all \
--privileged \
--ipc=host \
--name facewine \
--device /dev/snd \
--device=/dev/dri \
-e DISPLAY=$DISPLAY \
-e LC_ALL=en_US.UTF-8 \
-e LANG=en_US.UTF-8 \
-e LANGUAGE=en_US.UTF-8 \
-e NVIDIA_VISIBLE_DEVICES=0 \
-v /tmp/.X11-unix:/tmp/.X11-unix:ro \
-v $(pwd)/../:/mnt \
wine:20.04