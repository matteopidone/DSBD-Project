# DSBD-Project

## Configurazione
Dopo aver clonato il repository, eseguire il comando

```bash
docker compose up
```

All'avvio di ogni container, verranno eseguite operazioni di routine necessarie per l'utilizzo del sistema: creazione ed inizializzazione di tabelle, setup comunicazioni, avvio processi ecc.

Si stima un tempo di start (per i motivi citati sopra) pari a circa 3-4 minuti.

Si rimanda alla sezione `Configurazione` (<a href ="https://google.com">Documentazione Progetto</a>) per tutti i dettagli relativi a questa fase.

In caso di fallimento del processo di building (healthcheck failed ecc) è necessario eseguire 
```bash
docker compose down && docker compose up
```

## Requisiti
Si consiglia di dedicare almeno 3/4 Gb di RAM a Docker Desktop per evitare problemi di terminazione improvvisa dei processi all'interno dell' `Etl Data Pipeline` (`Error 137, Error 0`)
