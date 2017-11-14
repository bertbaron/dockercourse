# dockercourse

## Inspect the filesystem and interactive shell



## Install Portainer

Portainer is a webui on top of docker, making most of the commands available via a graphical user interface. 
It is available as a docker container making it a nice first example of running a service as container.

1. Go to Docker Hub (https://hub.docker.com/), search for Portainer and go to the top result (with most pulls
   and stars)
1. Follow the 'Deploy Portainer' link and install portainer according the instructions under 'Quick start'
  
   Try to explain for yourself the options passed to the 'docker run' command.
  
   Note that because portainer runs as a docker container it obviously doesn't have permission to access the
   docker deamon unless this is explicitly granted. This is done by mounting a socket from the host to the
   container as if it is a normal file.

1. Go to the portainer web interface (http://<your_ip>:9000), come up with a new password and chose to manage
   the Local Docker Enviroment
  
1. Take your time to look around. You should see that at least one container is running (portainer itself) and
   can inspect its properties
  
1. Remove the container via the web ui. This is equivalent to 'docker rm -f <container>'.

1. Start a new container using the command line from 2. Log in again and notice that it rememberd the password.
   How is this possible?

Bonus:

1. Remove the container again. This time also remove the mounted volume on the host with

   ```bash
   sudo rm -rf /opt/portainer/
   ```
   
   Be careful with this command, don't type it wrong or we have to create a new VM for you!
   
1. Start a new container again and go to http://<your_ip>:9000. Now it should prompt you for a new password
   again
   
   
   
## Create your own image

The task is to create an image for a simple python web service.

Tip: you can build the image and run it if the build is successful with a single command:
```bash
docker build -t greeting . && docker run --rm -p8000:8000 greeting
```

Use the arrow up to recall the command from history. You can do this at any time between
the steps to see where you are.
  
1. cd into the greeting directory and create a Dockerfile there with the command
   ```bash
   nano Dockerfile
   ```

1. We base the image on the popular lightweight Alpine image. Look it up on Docker Hub and
   see the example under 'Usage'. In this step you should:
   
   * Add the **FROM** instruction
   * Add the app folder to the image using **ADD**
   * Set the entry point to ```python service.py``` using **CMD**
     (We will change it to Entrypoint later)

   At this stage you should get an error like:
   
   ```starting container process caused "exec: \"python\": executable file not found in $PATH"```

1. Our app needs Python to be installed. 

   * Use ```apk``` to install the package ```python```
   (see the Alpine documentation on Docker hub for an example)
   
   At this stage you should get an error like:

   ```ImportError: No module named cherrypy```

1. Our app needs the Python modules ```cherrypy``` and ```simplejson```. Python modules can be
   installed using pip.
   
   * Use ```apk``` to install the package ```py-pip```
   * Run the command ```pip install cherrypy simplejson``` to install both Python modules
   
   Now the service should start correctly. Go to http://<your-ip>:8000 to see if it is
   accessible. You should get the message:
   
   ```jquery library is not loaded```

1. Our page requires jquery-3.2.1.min.js in the ```static``` folder.

   * Use **ADD** to add ```https://code.jquery.com/jquery-3.2.1.min.js``` as
     ```static/jquery-3.2.1.min.js```
     
   This may be a good time to inspect the files in the container. The easiest way is to
   run the container with for example ```ls -l``` or ```ls -l /static``` as argument. Since we
   didn't specify an Entrypoint it will use ```/bin/sh``` as entrypoint
   
   Reload the web page, this time it should work!
   
1. Simulate some development effort by changing the greeting format in ```app/service.conf```
   to something unique and rebuild and run again. You should now be greeted with your own
   unique message!
   
   
## Registries and tags