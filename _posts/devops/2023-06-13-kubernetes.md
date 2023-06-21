---
layout: post
title: "kubernetes"
date: 2023-06-13
categories: Devops
tags:
  - docker
---

- [Concept](#concept)
- [Command](#command)
  - [get into container](#get-into-container)
  - [how to get pod name](#how-to-get-pod-name)
  - [how to get container name](#how-to-get-container-name)
  - [check pod status](#check-pod-status)
  - [continuous deploy](#continuous-deploy)

### Concept

- cluster  
  cluster is a set of physical or virtual machines and other infrastructure resources used by Kubernetes to run your applications.
- node  
  node is a physical or virtual machine, cluster is a group of nodes.
- pod  
  pod is a group of one or more containers, with shared storage/network, and a specification for how to run the containers.  
  It can be understood as docker compose.  
  one node can have multiple pods.

### Command

#### get into container

```bash
kubectl exec -it [pod name] --container [container name] -- bash
```

#### how to get pod name

```bash
kubectl get pods
```

#### how to get container name

container name is defined in your yaml file.  
 this is a example of deployment yaml file.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
name: simu
namespace: default
spec:
replicas: 2
selector:
  matchLabels:
    app: simu
template:
  metadata:
    annotations:
      vke.volcengine.com/burst-to-vci: enforce
    labels:
      app: simu
  spec:
    containers:
      - image: cr-cn-beijing.volces.com/white-rhino/simu-web:latest
        name: simu-web
        ports:
          - containerPort: 3000
            protocol: TCP
      - image: cr-cn-beijing.volces.com/white-rhino/simu-api:latest
        name: simu-api
        ports:
          - containerPort: 8814
            protocol: TCP
    imagePullSecrets:
      - name: volc
```

#### check pod status

when a pod occurs error, not running as expect, for example:

```shell
$ simu kubectl get pods
NAME                    READY   STATUS             RESTARTS      AGE
simu-6ff6cbfd59-c9x8r   1/2     CrashLoopBackOff   4 (49s ago)   3m47s
```

you can get error info using this command:

```bash
kubectl describe pod simu-6ff6cbfd59-c9x8r
```

#### continuous deploy

```bash
kubectl rollout restart -f [yaml file]
```

### job
