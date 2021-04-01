Intro
----

Build local image:

```bash 
# At root level
docker build -t soils-analysis .
docker run -p8000:8000 soil-analysis start
```

Testing local server:

```
./test-server.sh
```
