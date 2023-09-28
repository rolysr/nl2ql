# nl2ql

Neurosymbolic model for knowledge discovery in semantic networks

## Start Neo4J DB Docker Container

```bash
 docker run \
--name testneo4j \
-p7474:7474 -p7687:7687 \
-d \
-v $HOME/neo4j/data:/data \
-v $HOME/neo4j/logs:/logs \
-e NEO4J_AUTH=neo4j/testpassword \
docker.uclv.cu/neo4j
```
