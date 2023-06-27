---
layout: post
title: "Flask view serve file"
date: 2023-06-27
categories: Python
tags:
  - Flask
---

we can use flask view to serve files in a directory:

```python
from .config import FILE_DIRECTORY

@app.route('/api/file/<path:filename>')
def serve_static(filename):
    return send_from_directory(FILE_DIRECTORY, filename)
```

filename is the relative path of the file to the `FILE_DIRECTORY`.  
for example, the tree is:

```text
FILE_DIRECTORY
├── a
│   └── b
│── c
```

we can get file `b` use url `/api/file/a/b` and file `c` use url `/api/file/c`.
