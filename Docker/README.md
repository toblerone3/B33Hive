# Docker Image for B33Hive

___

![Screenshot](DockHiveCover.png)

## Requirements:
- Docker (Engine or Desktop)
- (Windows Only) Some Form of XServer for Windows (This guide will use XMing, please carefully consider your requirements to decide which you should use)

## Installation:
Download the docker release from the releases section, and at the same time, download and install Xming Server and Xming Fonts (Or your XServer of choice)

Navigate to the Xming Installation Folder and open a CMD Prompt in that location

### WARNING ###
The following should not be done on sensitive networks, please ensure you make an exception for Xming instead of doing the following on any form of production machine as we are about to launch XMing without access control
This is simply for demonstration and testing purposes

Launch XMing using:
```Xming.exe -ac```

## Building Docker:
To build using the docker image provided, open a terminal in the location of the Dockerfile and type:
``` docker build -t dockhive . ```

This will add the image to Docker Desktop, however we need to set a few parameters first in order for us to get a visual output:

In CMD Prompt again, type ```set DISPLAY=<YOUR_IPV4>:0.0```

Finally run the container using:

```docker run -it --rm -e DISPLAY=%DISPLAY% --network="host" --name <NAME> dockhive```

Replace <NAME> with a name of your choosing (Non-Critical)
