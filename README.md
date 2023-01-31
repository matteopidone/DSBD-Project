# DSBD-Project

## Configurazione
Aprire nella directory del progetto un terminale ed eseguire il seguente comando

```bash
docker compose up
```

In questo modo ogni microservizio lancerà operazioni di routine necessarie per l'utilizzo del sistema: creazione ed inizializzazione di tabelle, setup comunicazioni, avvio processi ecc.
Si stima un tempo di start pari a circa 3-4 minuti.
Si rimanda alla sezione `Configurazione` della relazione per tutti i dettagli relativi a questa fase.

In caso di fallimento del processo di building (healthcheck failed ecc) è necessario eseguire 
```bash
docker compose down
```
e poi successivamente
```bash
docker compose up
```

## Requisiti
Si consiglia di dedicare almeno 3/4 Gb di RAM a Docker Desktop per ovviare problemi di terminazione improvvisa dei processi all'interno dell' `Etl Data Pipeline` (`Error 137, Error 0`)

## Microservice_1 - ETL Data Pipeline

## Microservice_2 - Data Storage

## Microservice_3 - Data Retrieval

## Microservice_4 - SLA Manager
