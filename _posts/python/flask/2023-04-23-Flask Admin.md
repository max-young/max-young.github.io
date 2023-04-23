---
layout: post
title: "Flask Admin"
date: 2023-04-23
categories: Python
tags:
  - Flask
---

- [basic usage](#basic-usage)
- [custom view](#custom-view)

<https://flask-admin.readthedocs.io/en/latest/>

### basic usage

```python
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)


from .models import CaseAppearance, CaseCategory, TaskCategory, User
from .user import UserAdminView
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='kanban admin', template_mode='bootstrap3')
admin.add_view(ModelView(TaskCategory, db.session))
admin.add_view(ModelView(CaseCategory, db.session, category="case"))
admin.add_view(ModelView(CaseAppearance, db.session, category="case"))
```

### custom view

```python
class UserAdminView(ModelView):
    """user admin view
    """
    column_hide_backrefs = False
    column_list = ('username', "modules")
    can_create = False
    can_delete = False
    form_columns = ('modules', )
```

```python
admin.add_view(UserAdminView(User, db.session))
```
