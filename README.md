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

1. Verwijder de directory (met `rm -rf portainerdata`)
   
   Mocht je een `Permission denied` melding krijgen, dan kan het alsnog met `sudo rm -rf portainerdata`).

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
   
   Test door een aantal keren kleine wijzigingen in de sourcecode te maken en de image telkens
   weer te herbouwen. Hoe lang duurt het bouwen van de image na een code wijziging?

## 4 - Registries en tags

Referenties:

* https://docs.docker.com/engine/reference/commandline/cli/
* https://docs.docker.com/registry/#requirements
* https://docs.docker.com/engine/reference/commandline/tag/#tag-an-image-referenced-by-name

Er is al een docker registry geinstalleerd op het lokale netwerk: ```cursusregistry:5000```
 
1. Tag je greeting image met ```cursusregistry:5000/<your-name>/greeting```. Bekijk je lokale
   images met:

    ```docker images```

   Je zou moeten zien dat het image ```greeting``` en ```cursusregistry:5000/<your-name>/greeting```
   naar hetzelfde image ID verwijzen

   Merk op dat, omdat je niet expliciet een tag hebt opgegeven de tag ```latest``` is gebruikt.   
   
1. Push de image naar de cursusregistry

   Onze registry heeft geen user interface, maar je kunt de rest interface aanroepen met een webbrowser
   of met curl:
    
   * Een overzicht van de images:

     http://cursusregistry:5000/v2/_catalog

     ```curl -X GET http://cursusregistry:5000/v2/_catalog```

   * De tags van een specifieke image:

     http://cursusregistry:5000/v2/<your-name>/greeting/tags/list

     ```curl -X GET http://cursusregistry:5000/v2/<your-name>/greeting/tags/list```

   Dit zou iets moeten printen als:   
   ```{"name":"<your-name>/greeting","tags":["latest"]}```   

1. Tag je image met versie tag ```1.0```
   (i.e. ```cursusregistry:5000/<your-name>/greeting:1.0```), en push die ook.
   
   Inspecteer de registry nog een keer.
    
1. Pull de image met 1 van de tags en run hem:

   ```docker pull cursusregistry:5000/<your-name>/greeting```
   
   ```docker run --rm -p8000:8000 cursusregistry:5000/<your-name>/greeting```
   
   Opmerking: docker run zal de image ook pullen, maar alleen wanneer die niet lokaal aanwezig is. Daarom pullen
   we eerst zelf expliciet.

### Bonus

1. Stop de container en run deze keer de image van je buurman

1. Wijzig het greeting format en bouw de image nog een keer.
   Geef het de tag ```cursusregistry:5000/<your-name>/greeting:1.1``` en push de image
   
   Je zult nu een 1.0, 1.1 en latest in the repository moeten kunnen zien, maar naar welke image verwijst ```latest```?
   
1. Repareer dit en *pull* and *run* the image met de ```latest``` tag


## 5 - Docker compose

Redis is een snelle key-value store die uitermate geschikt is voor gedeelde cache.

In deze opgave gaan we onze service samen met een redis container opstarten zodat we het aantal request naar onze site
kunnen bijhouden.

1. Maak een docker-compose bestand om de service uit de vorige opgave te runnen
 
   Run de image met

   ```docker-compose build && docker-compose up```

   Stop met ctrl+c

1. In ```service.py```, enable de regels

   ```python
   import redis
   cache = redis.Redis(host='redis', port=6379)
   ```

   en in ```Dockerfile```, voeg module ```redis``` to aan de ```pip install``` regel

1. Build en run met ```docker-compose```. Op de website zal nu een request counter moeten
   verschijnen.

### Bonus

1. Zie:

   ```docker-compose -h```
   ```docker-compose up -h```
   
    * Start de containers in de achtergrond (```docker-compose up -d```)
    
    * Herstart de containers met ```down``` en ```up -d```
    
    * Herstart de containers met ```restart```
    
    Wat is het verschil?
    
    Experimenteer eventueel met andere docker-compose commando's. Gebruik
    
    ```docker ps``` en ```docker ps -a``` om te zien welke containers er zijn en runnen

1. Wanneer en redis container word gestopt en weer gestart dan bewaart deze blijkbaar de state,
   maar bij het opnieuw maken van een container is die state natuurlijk weg
   
   Maak de directory ```redisdata```. Pas ```docker-compose.yml``` de configuratie voor de redis
   service aan met voorbeeld hieronder:

   ```yml
       command: ["--appendonly", "yes"]
       volumes:
         - ./redisdata:/data
   ```
   
   Met het command worden de argumenten ```--apendonly yes``` meegegeven aan redis om persistence
   aan te zetten (zie https://hub.docker.com/_/redis/ onder 'start with persistent storage')
   
   Met volumes word de lokale directory als volume gemount 
   (zie https://docs.docker.com/compose/compose-file/#volumes) 
   
    Wanneer de service nu word downgebracht en daarna weer up, dan zou de teller moeten doorlopen
    
1. Doe hetzelfde, maar maak nu een named volume (zie https://docs.docker.com/compose/compose-file/#volumes)

## 6 - Docker swarm

