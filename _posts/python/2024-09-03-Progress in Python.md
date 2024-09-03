---
layout:     post
title:      "Progress in Python"
date:       2024-09-03
categories: Python
tags:
    - Python
---


### Progress Bar

采用[Progress Bar](https://progressbar-2.readthedocs.io/en/latest/#context-wrapper)

示例代码:
```Python
import progressbar

progress_bar = progressbar.ProgressBar(max_value=len(data))
bar_count = 0
for i in data:
    progress_bar.update(bar_count)
    bar_count += 1
    
    # do something with i
```

### Spinner

```python
import itertools
import sys
import threading
import time


def spinner_decorator(func):
    def spinning_cursor():
        while True:
            for cursor in '|/-\\':
                yield cursor

    def spinner_task(spinner):
        while not done:
            sys.stdout.write(next(spinner))  # Write the next character
            sys.stdout.flush()               # Flush the output buffer
            sys.stdout.write('\b')           # Erase the last character
            time.sleep(0.1)                  # Delay

    def wrapper(*args, **kwargs):
        global done
        done = False
        spinner = spinning_cursor()
        spinner_thread = threading.Thread(target=spinner_task, args=(spinner,))
        spinner_thread.start()

        # Execute the original function
        result = func(*args, **kwargs)

        # Stop the spinner
        done = True
        spinner_thread.join()
        print(" 完成 !")  # Indicate task completion

        return result

    return wrapper
```