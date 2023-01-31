# DSBD-Project

## Configurazione
Dopo aver clonato il repository, eseguire il comando:

```bash
docker compose up
```

All'avvio di ogni container, verranno eseguite operazioni di routine necessarie per l'utilizzo del sistema: creazione di tabelle, inserimento di valori iniziali, setup comunicazioni, avvio processi ecc.

<strong>Si stima un tempo di start (per i motivi citati sopra) pari a circa 3-4 minuti.</strong>

Si rimanda alla sezione `Configurazione` (<a href ="https://github.com/matteopidone/DSBD-Project/blob/main/Relazione%20Progetto%20DSBD.pdf" target="_blank">Documentazione Progetto</a>) per tutti i dettagli relativi a questa fase.

In caso di fallimento del processo di building (kafka errors, healthcheck failed ecc..) è necessario eseguire:
```bash
docker compose down && docker compose up
```

### Requisiti
Si consiglia di dedicare almeno 3/4 GB di RAM a Docker Desktop per evitare problemi di terminazione improvvisa dei processi all'interno dell' `ETL Data Pipeline` (`Error 137, Error 0`)

## Data Retrieval
Porta 9003
 - Metriche: `localhost:9003/` <a href ="http://localhost:9003" target="_blank">Clicca qui</a>

## SLA Manager
Porta 9004 
- Numero violazioni passate: `localhost:9004/pastViolation` <a href ="http://localhost:9004/pastViolation" target="_blank">Clicca qui</a>
- Indicazione sulle possibili violazioni: `localhost:9004/futureViolation` <a href ="http://localhost:9004/futureViolation" target="_blank">Clicca qui</a>
