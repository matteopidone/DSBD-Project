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

### Requisiti
Si consiglia di dedicare almeno 3/4 Gb di RAM a Docker Desktop per evitare problemi di terminazione improvvisa dei processi all'interno dell' `Etl Data Pipeline` (`Error 137, Error 0`)

## Data Retrieval
 - Porta 9003: <a href ="http://localhost:9003">Clicca qui</a>

## SLA Manager
- Porta 9004 
- Numero violazioni passate: `localhost:9004/pastViolation` <a href ="http://localhost:9004/pastViolation">Clicca qui</a>
- Indicazione sulle possibili violazioni: `localhost:9004/futureViolation` <a href ="http://localhost:9004/futureViolation">Clicca qui</a>