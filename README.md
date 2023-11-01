# nl2ql

Neurosymbolic model for knowledge discovery in semantic networks

## Start Neo4J DB Docker Container

### Basic Neo4J DB

```bash
 docker run \
--name testneo4j \
-p 7474:7474 -p 7687:7687 \
-d \
-v $HOME/neo4j/data:/data \
-v $HOME/neo4j/logs:/logs \
-e NEO4J_AUTH=neo4j/testpassword \
docker.uclv.cu/neo4j
```

### Classic Neo4J DB

```bash
docker run \
--name testneo4j2 \
-p 7475:7474 -p 7688:7687 \
-d \
-v $HOME/neo4j2/data:/data \
-v $HOME/neo4j2/logs:/logs \
-e NEO4J_AUTH=neo4j/testpassword2 \
docker.uclv.cu/neo4j

```
