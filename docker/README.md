# 1. Clone the repository to your computer
# 2. Run directly on the source code
**Step 1: Build env to run app**
- Option 1: Build base docker container
  ```
  sudo docker build -f docker/Dockerfile.base -t deepfacelive:latest .
  ```
- Option 2: Pull the pre-built Docker image from Docker Hub
  ```
  sudo docker pull philong/deepfacelive:base
  ```
**Step 2: Run source code**
You need to set up the corresponding DISPLAY ID for your computer in the run_env.sh file. Next start run_env.sh
```
sudo bash run_env.sh
# In the docker container
python3 run.py --execution-provider cuda --execution-threads 12 --max-memory 16 --frame-processor {face_swapper,face_enhancer} --keep-fps --keep-audio
```
# 3. Run the FaceSwap App using the pre-packaged Docker image
**Step 1: Pull the docker image**
```
sudo docker pull philong/deepfacelive:latest
```
**Step 2: Confige the run_app.sh file and start**
Mount any folder containing images you want to convert from your computer into the container
```
-v <your-folder-path>:/Deep-Live-Cam/data_test \
```
If your PC supports GPU, adjust the **max-memory** value corresponding to the VRAM size of your GPU and set the **execution-provider** to **cuda**
```
--execution-provider cuda \
--execution-threads 12 \
--max-memory 16 \
```
If your PC does not support GPU, please set the **execution-provider** mode to **cpu**.
```
--execution-provider cpu \
--execution-threads 12 \
--max-memory 16 \
```

# 4. Running on Windows OS
- Install [Xming](https://sourceforge.net/projects/xming/) software additionally to support screen exporting from the container.
- After installing Xming, please start Xlaunch first. Check the DISPLAY ID and DISPLAY PORT in the Xlaunch software.
- Set them in the run_app.sh file and start the container.