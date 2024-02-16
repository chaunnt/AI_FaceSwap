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
-v $(pwd):/Deep-Live-Cam/data_demo \
-e NVIDIA_VISIBLE_DEVICES=0 \
-e DISPLAY=:2 \
nexle/faceswap/deepfacelive/app:latest \
--execution-provider cuda \
--execution-threads 12 \
--max-memory 16 \
--frame-processor {face_swapper,face_enhancer} \
--keep-fps \
--keep-audio
# wine python run.py --execution-provider dml --execution-threads 12  --max-memory 16 --keep-fps --keep-audio