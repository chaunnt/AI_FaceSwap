docker rm -f faceswap_app
xhost +
docker run -it \
--gpus all \
--privileged \
--ipc=host \
--ulimit memlock=-1 \
--ulimit stack=67108864 \
--name faceswap_app \
--network host \
--device=/dev/video1:/dev/video1 \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v /dev/video0:/dev/video0 \
-v /dev/video1:/dev/video1 \
-v /dev/video2:/dev/video2 \
-v /dev/video3:/dev/video3 \
-v $(pwd)/data_test:/Deep-Live-Cam/data_test \
-e NVIDIA_VISIBLE_DEVICES=0 \
-e DISPLAY=:2 \
philong/deepfacelive:latest \
--execution-provider cuda \
--execution-threads 12 \
--max-memory 16 \
--frame-processor {face_swapper,face_enhancer} \
--keep-fps \
--keep-audio
