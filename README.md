# Opgaven basiscursus docker

## 1 - ```docker run``` en ```docker exec```

Referenties:

* https://docs.docker.com/engine/reference/commandline/cli/
* http://tldp.org/LDP/abs/html/basic.html
* https://dockercheatsheet.painlessdocker.com/

Elke linux distributie bevat het bestand ```/etc/issue``` met een melding of systeem identificatie
(zie https://linux.die.net/man/5/issue)

Het commando ```cat``` print de inhoud van een (text)bestand

In deze opgave zullen we de inhoud van ```/etc/issue``` van een container op verschillende manieren op het scherm printen.

1. Gebruik ```docker run``` om direct ```cat /etc/issue``` van de ```nginx``` image te printen
1. Gebruik ```docker run``` om een interactive shell te starten (```/bin/bash```) en print de inhoud van ```/etc/issue``` van daaruit
1. Start een ```nginx``` container in de achtergrond (met ```-d```). Gebruik ```docker ps``` om de naam te identificeren en dan
   ```docker exec``` om direct ```cat /etc/issue``` uit te voeren
1. Terwijl de container nog steeds draait, gebruik ```docker exec``` om een interactieve shell te starten en print de inhoud van
   ```/etc/issue``` van daaruit
1. Bij welke van de bovenstaande manieren zijn de vlaggen ```-ti``` nodig?
1. stop and verwijder eventuele achtergelaten containers (```docker rm```)

### Bonus:

1. Gebruik ```docker run``` om de proceslijst van de ```httpd:2.4.34``` image te printen (```ps -ef```)
1. Start nu een container op basis van ```httpd:2.4.34``` in de achtergrond en voer ```ps -ef``` uit via ```docker exec```.
   Kun je het verschil verklaren?

## 2 - Installeer Portainer

Referenties:

* https://docs.docker.com/engine/reference/commandline/cli/

Portainer is een web interface boven op docker, waarmee de meeste docker commando's via een grafische user interface
beschikbaar wordt gemaakt. Portainer is zelf ook als docker container te draaien en dus een mooi eerste voorbeeld voor
het draaien van een service in een container.

1. Ga naar Docker Hub (https://hub.docker.com/), zoek op Portainer en ga naar het top resultaat (met de meeste pulls
   en stars)
1. Volg de **Deploy Portainer** link en installeer portainer volgens de instructies onder **Quick start**.
  
   Probeer de opties die aan ```docker run``` worden meegegeven te verklaren
  
   Merk op dat portainer, omdat deze in een container draait, uiteraard geen toegang heeft tot de docker deamon op de host
   tenzij die toegang expliciet wordt gegeven. Dat gebeurt door het mounten van een socket op de host zoals ook een
   gewoon bestand of directory kan worden gemount.

1. Ga naar de portainer webinterface (http://localhost:9000), bedenk een wachtwoord en kies om de 'Local Docker Environment'
   te beheren.
  
1. Neem de tijd om even rond te kijken. Je zou in elk geval moeten zien dat er tenminste een container draait
   (portainer zelf) en je kunt daar de eigenschappen van inspecteren.
  
1. Verwijder de container via the web ui. Dit is equivalent aan het commando ```docker rm -f <name of container, or container id>```.

1. Start een nieuwe container (pijltje omhooog in de terminal om laatste commando te selecteren). Log opnieuw in en merk
   op dat het wachtwoord is onthouden. Hoe kan dat?

### Bonus:

1. Verwijder de container maar verwijder dit keer ook het volume.

1. Start een nieuwe container en open opnieuw de webinterface. Nu zal er opnieuw een wachtwoord worden gevraagd
   again
   
### Bonus 2:

1. Maak een directory 'portainerdata' en start portainer deze keer met de directory gemount

1. Controleer of het wachtwoord tussen verschillende containers wordt bewaard.

1. Onderzoek de directory op de host. Wie is de eigenaar van de bestanden?

   
## 3 - Maak je eigen image

Referenties:

* https://docs.docker.com/engine/reference/commandline/cli/
* https://docs.docker.com/engine/reference/builder/

Het doel is om een image te maken met een eenvoudige python web service.

Tip: je kunt met 1 commando de image bouwen en runnen wanneer het bouwen slaagt:
```bash
docker build -t greeting . && docker run --rm -p8000:8000 greeting
```

Je kunt dit tussen elk van de volgende stappen uitvoeren om te zien hoe je ervoor staat.
  
1. open de ```greeting``` directory in je home en maak daar het bestand ```Dockerfile```

1. We baseren ons image op het populaire lichtgewicht Alpine image. In deze stap moet je:
   
   * De **FROM** instructie voor het alpine base image toevoegen. Je kunt dit vinden op Docker Hub onder 'Usage'.
   * Voeg de ```app``` folder toe aan het image met **ADD**
   * Voegen een **CMD** instructie toe en start daar ```python service.py```

   Wanneer je de container bouwt en draait dan zou je de onderstaande melding moeten krijgen:
   
   ```starting container process caused "exec: \"python\": executable file not found in $PATH"```

1. Het blijkt dat onze app Python nodig heeft om te draaien: 

   * Voeg het package ```python``` to met de package manager ```apk``` die op alpine wordt gebruikt
   (zie de documentatie van de Alpine image op Docker hub (onder 'Usage') voor een voorbeeld)
   
   Nu zou je bij het draaien de volgende melding moeten zien:

   ```ImportError: No module named cherrypy```

1. Blijkbaar heeft onze app ook de Python modules ```cherrypy``` en ```simplejson``` nodig. Python modules kunnen worden
   geinstalleerd met ```pip```.
   
   * Gebruik ```apk``` om het package ```py-pip``` te installeren op het image
   * Gebruik ```pip install cherrypy simplejson``` om de beide Python modules te installeren
   
   Nu zou de service correct moeten starten. Ga naar http://localhost:8000 om te kijken of de web service werkt.
   Je zou nu de volgende melding moeten krijgen:
   
   ```jquery library is not loaded```

1. Onze webpagina verwacht jquery-3.2.1.min.js in the ```static``` folder.

   * Gebruik **ADD** om ```https://code.jquery.com/jquery-3.2.1.min.js``` aan de image toe te voegen als
     ```static/jquery-3.2.1.min.js```
   
   Dit is een goed moment om de bestanden in de container eens te inspecteren. De eenvoudigste manier is door het
   runnen van ```ls -l``` of ```ls -l /static```. Maar het kan natuurlijk ook met bijvoorbeeld een interactieve shell.
   
   Let op: alpine bevat geen ```/bin/bash``` maar wel ```/bin/sh```.
   
   Herlaad de web pagina wanneer de container weer draait. Deze keer zou de pagina moeten werken!
   
1. Simuleer wat development werk door het greeting format in ```app/service.conf``` te wijzigen naar iets ludieks en
   herbouw en run nog een keer. Je zou nu moeten worden begroet met je eigen melding.!

### Bonus

1. Vervang **CMD** door een **ENTRYPOINT**. Dit maakt het bijvoorbeeld mogelijk om command line argumenten achter het run
   commando direct door te geven aan de service (maar daardoor wordt het iets lastiger om toegang tot de shell te krijgen)
   
1. **EXPOSE** poort 8000 zodat het zichtbaar is dat die poort in de image wordt gebruikt.
   
1. Staan de commando's in de dockerfile in een logische volgorde? Bedenk welke onderdelen het meest waarschijnlijk zullen
   wijzigen tijdens development en herschik de commando's wanneer je denkt dat dit de snelheid verhoogd.
   
   Test door een aantal keren kleine wijzigingen in de sourcecode te maken (whitespace is voldoende) en de image telkens
   weer te herbouwen. Hoe snel is het bouwen van de image na een code wijziging?

## 4 - Registries and tags

References:

* https://docs.docker.com/engine/reference/commandline/cli/
* https://docs.docker.com/registry/#requirements
* https://docs.docker.com/engine/reference/commandline/tag/#tag-an-image-referenced-by-name

There is already a docker registry installed on the local network of the VM's: ```cursusregistry:5000```
 
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


## 6 - Docker swarm