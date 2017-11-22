# dockercourse

## 1 - Docker run and docker exec

Every linux distribution contains the file ```/etc/issue``` with a message or system identification
(see https://linux.die.net/man/5/issue)

The command ```cat``` prints the contents of a file

In this assignment we will print the content of this file in different ways.

1. Use ```docker run``` to directly run ```cat /etc/issue``` of the ```nginx``` image (```-ti``` should not be needed)
1. Use ```docker run``` to start an interactive shell (```/bin/bash```) and print the content of ```/etc/issue``` from there
1. Start an ```nginx``` container in the background (using ```-d```). Use ```docker ps``` to identify its name and then
   use ```docker exec``` to directly execute ```cat /etc/issue``` (```-ti``` should not be needed)
1. While the container is still running, use ```docker exec``` to start an interactive shell print the content of
   ```/etc/issue``` from that shell
1. stop and remove the container with ```docker rm```

### Bonus:

1. Use ```docker run``` to run the command ```ps -ef``` of the ```nginx``` image.
1. Now start an ```nginx``` container in the background again and this time run the ```ps -ef``` command with
   ```docker exec```. Can you explain the difference?


## 2 - Install Portainer

Portainer is a web ui on top of docker, making most of the commands available via a graphical user interface. 
It is available as a docker container, making it a nice first example of running a service as container.

1. Go to Docker Hub (https://hub.docker.com/), search for Portainer and go to the top result (with most pulls
   and stars)
1. Follow the 'Deploy Portainer' link and install portainer according the instructions under 'Quick start'.
  
   Try to explain for yourself the options passed to the 'docker run' command.
  
   Note that because portainer runs as a docker container it obviously doesn't have permission to access the
   docker deamon unless this is explicitly granted. This is done by mounting a socket from the host to the
   container as if it is a normal file.

1. Go to the portainer web interface (http://<your_ip>:9000), come up with a new password and choose to manage
   the Local Docker Enviroment
  
1. Take your time to look around. You should see that at least one container is running (portainer itself) and
   can inspect its properties
  
1. Remove the container via the web ui. This is equivalent to command 'docker rm -f <name of container, or container id>'.

1. Start a new container (arrow up in the terminal to select the previous command line).
   Log in again and notice that it rememberd the password. How is this possible?

### Bonus:

1. Remove the container again. This time also remove the mounted volume on the host with

   ```bash
   sudo rm -rf /opt/portainer/
   ```
   
   Be careful with this command, don't type it wrong or we have to create a new VM for you!
   
1. Start a new container again and go to http://<your_ip>:9000. Now it should prompt you for a new password
   again
   
   
   
## 3 - Create your own image

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

1. We base the image on the popular lightweight Alpine image. In this step you should:
   
   * Add the **FROM** instruction for the alpine base image. Look it up on Docker Hub and
     see the example under 'Usage'.
   * Add the app folder to the image using **ADD**
   * Add a **CMD** instruction to start ```python service.py``` by default

   At this stage you should get an error like:
   
   ```starting container process caused "exec: \"python\": executable file not found in $PATH"```

1. Our app needs Python to be installed. 

   * Use ```apk``` to install the package ```python```
   (see the Alpine documentation on Docker hub under Usage for an example)
   
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

### Bonus

1. Replace the **CMD** by an **ENTRYPOINT**. This allows arguments to be passed to our service
   (but it doesn't allow easy access to the shell in the container anymore)
   
1. Expose port 8000 to make it visible for tools that that port is used, allowing auto-binding for
   example.

## 4 - Registries and tags

There is a docker registry installed on the local network of the VM's: ```cursusregistry:5000```
 
1. Tag your greeting image with ```cursusregistry:5000/<your-name>/greeting```. List your local
   images with:

    ```docker images```

   You should see that the image ```greeting``` and ```cursusregistry:5000/<your-name>/greeting```
   point to the same image ID
   
   Notice that because you didn't explicitly tag it with a version it was tagged with ```latest```
   
1. Push the image to the cursusregistry

   The registry doesn't have a user interface, but you should be able to list the tags on your image
   with the following command:

   ```curl -X GET http://cursusregistry:5000/v2/<your-name>/greeting/tags/list```

   This should print something like:
   ```{"name":"<your-name>/greeting","tags":["latest"]}```   

1. Now tag your image again, but this time with the version tag ```1.0```
   (i.e. ```cursusregistry:5000/<your-name>/greeting:1.0```), and push that to the registry too.
   
   Inspect the registry again if you like
    
1. Pull the image by one of its new tags and run it::

   ```docker pull cursusregistry:5000/<your-name>/greeting```
   ```docker run --rm -p8000:8000 cursusregistry:5000/<your-name>/greeting```
   
   You should see that it pulls the image from the repository before starting it
   
   Note: docker run would also pull the image, but only if it doesn't find the tag locally.
   Therefore we pull first.

### Bonus

1. Stop the image and this time run the image from your neighbour

1. Change the greeting format and build the image again like we did in the previous assignment
   Give it the tag ```cursusregistry:5000/<your-name>/greeting:1.1``` and push it
   
   You now have a 1.0, 1.1 and latest in the repository, but to which image is latest pointing?
   
1. Fix this and *pull* and *run* the image by its ```latest``` tag


## 5 - Docker compose

1. Make a docker-compose file to run te service from the previous assignment
