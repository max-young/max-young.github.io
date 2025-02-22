---
layout: post
title: "Python Docker"
date: 2023-11-20
categories: Backend
tags:
  - Python
  - Docker
---


<https://docker-py.readthedocs.io/en/stable/index.html>

### docker client

```python
import docker

docker_client = docker.from_env()
```

### build image

```python

try:
    image = docker_client.images.get(base_img_name)
    image.reload()
except docker.errors.ImageNotFound:
    image = docker_client.images.build(path=f"{root_dir}/docker",
                               tag=base_img_name)
```

### run a docker container

```python
mounts = [
    docker.types.Mount(target="/apollo",
                        source=apollo_dir,
                        type="bind"),
    docker.types.Mount(target="/apollo/modules/map/data",
                        source=map_dir,
                        type="bind"),
    docker.types.Mount(target="/apollo/modules/calibration/data",
                        source=calibration_dir,
                        type="bind"),
    docker.types.Mount(target="/apollo/third_party/archives/gpu",
                        source=gpu_dir,
                        type="bind",
                        read_only=True),
    docker.types.Mount(target="/apollo/data",
                        source=apollo_data_dir,
                        type="bind"),
]
for bag_dir in BAG_DIRS:
    mounts.append(
        docker.types.Mount(target=bag_dir,
                           source=bag_dir,
                           type="bind",
                           read_only=True))
for other_dir in OTHER_DIRS:
    mounts.append(
        docker.types.Mount(target=other_dir,
                           source=other_dir,
                           type="bind"))
ports = {}
for p in range(DVPORT_RANGE_BEGIN, DVPORT_RANGE_END):
    ports[p] = p
environments = ["USER=apollo"]
container = docker_client.containers.run(image="ubuntu:18.04-dvplayer",
                                         user="apollo",
                                         name=DV_CONTAINER_NAME,
                                         hostname=DV_CONTAINER_NAME,
                                         auto_remove=True,
                                         environment=environments,
                                         detach=True,
                                         tty=True,
                                         stdin_open=True,
                                         mounts=mounts,
                                         ports=ports)
```

### tips

if you run a container with auto remove, then after you stop this container, the container will be removed.  
but this process is async, so you restart this container immediately, you will get a error.  
you can use container.wait to wait the container to be removed.

```python
container = docker_client.containers.get(DV_CONTAINER_NAME)
container.stop()
container.wait(condition="removed")
```