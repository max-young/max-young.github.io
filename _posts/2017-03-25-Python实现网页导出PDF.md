---
layout:     post
title:      "Python实现网页导出PDF"
subtitle:   ""
date:       2017-03-25 11:27:00
author:     "alvy"
header-img: "img/post-bg-database.jpg"
header-mask: 0.3
catalog:    true
tags:
    - Python
    - Web
---

1. 安装pdfkit、wkhtmltopdf    
   参考地址：

   [https://jaimegris.wordpress.com/2015/03/04/how-to-install-wkhtmltopdf-in-centos-7-0/](https://jaimegris.wordpress.com/2015/03/04/how-to-install-wkhtmltopdf-in-centos-7-0/)    
   [http://kaito-kidd.com/2015/03/12/python-html2pdf/](http://kaito-kidd.com/2015/03/12/python-html2pdf/)    
   centos安装wkhtmltopdf有一点复杂，参照第一个链接    
   为了支持中文，需安装对应字体，参照第二个链接    
   安装如果出现错误，可参照这里：    [http://stackoverflow.com/questions/11425106/python-pip-install-fails-invalid-command-egg-info](http://stackoverflow.com/questions/11425106/python-pip-install-fails-invalid-command-egg-info)    

2. 代码

   ```python
   import pdfkit
   ......
   # html文件里的引用css和js等文件需要用到绝对路径
   render_html = render_template("exam_check_preview.html", **locals())
   options = {
       'disable-smart-shrinking': '',
       'image-dpi': 100,
       'zoom': 0.52,
       'quiet': ''
   }
   # 指定wkhtmltopdf路径，用whereis wkhtmltopdf即可获得，不指定会错误IOError: No wkhtmltopdf executable found
   config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
   pdf = pdfkit.from_string(render_html, False, options=options,
                            configuration=config)
   one_file = StringIO()
   one_file.write(pdf)
   one_file.seek(0)

   # 下载pdf
   file_name = "example.pdf"
   return send_file(one_file, attachment_filename=file_name,
                    as_attachment=True, mimetype="application/pdf")

   ```