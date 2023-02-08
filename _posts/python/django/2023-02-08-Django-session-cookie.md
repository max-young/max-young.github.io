---
layout: post
title: "Django session cookie"
date: 2023-02-08
categories: Backend
tags:
  - Python
  - Django
---

we can save data in the browser use cookie, and we can get it when we visit the website again.

django settings:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.sessions',
    ...
]

MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
```

in the view:

```python
def fool(request):
    """simple homepage for 安全员
    """
      repo_updated_time = request.session.get("repo_updated_time")
      if not repo_updated_time or (datetime.now() - datetime.strptime(repo_updated_time, "%Y-%m-%d %H:%M:%S")).seconds > 8 * 60 * 60:
          request.session["repo_updated_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          check_repo_uptodate = subprocess.call(os.getcwd() + "/utils/check_repo_uptodate.sh", shell=True)
          if check_repo_uptodate != 0:
              subprocess.Popen(os.getcwd() + "/utils/update_gondor.sh", shell=True)
              return render(request, "message.html", {"message": "后台正在更新, 请稍侯"})
```
