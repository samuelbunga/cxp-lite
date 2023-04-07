# Setup instructions to run CXP-Lite on MacOS

## Step 1: (ONLY FOLLOW STEP 1 IF YOU ARE TRYING TO SETUP DOCKER IMAGE FOR THE VERY FIRST TIME)

1.) Make sure you have docker desktop installed on your Mac. If not, you can download it here: https://www.docker.com/products/docker-desktop/

2.) Open Docker: You press Command + spacebar to open spotlight search and type Docker. Select docker and open.

3.) Now, install Xquartz with brew:
	`brew install xquartz`

4.) Once Xquartz is installed. Open terminal and type open -a xquartz. This will open xquartz App. Now, in the xquartz, select settings - > security -> Uncheck Authenticate connections and Check Allow connections from other clients. DONT close this App.

5.) `docker build https://raw.githubusercontent.com/samuelbunga/cxp-lite/master/Dockerfile -t cxp:latest`

This above step will take several minutes . . .


## Step 2: (RUN THESE BELOW COMMANDS EVERYTIME YOU WANT TO LAUNCH CXP-LITE)

1.) `open -a xquartz`

2.) `IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')`

3.) `export DISPLAY=$IP:0`

4.) `docker run --rm -e DISPLAY=$IP:0 -v /tmp/.X11-unix:/tmp/.X11-unix --mount type=bind,source="$HOME",target=/user_home cxp`


