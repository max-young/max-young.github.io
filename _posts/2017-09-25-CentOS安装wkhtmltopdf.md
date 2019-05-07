---
layout:     post
title:      "HTML文件转换PDF"
subtitle:   "CentOS安装wkhtmltopdf，及Python转换实现"
date:       2017-09-25 13:27:00
author:     "alvy"
header-img: "img/post-bg-unix-linux.jpg"
header-mask: 0.3
catalog:    true
tags:
    - Linux
    - CentOS
    - Python
---

##### 安装wkhtmltopdf

参考地址：

centos安装wkhtmltopdf有一点复杂，参照第一个链接

为了支持中文，需安装对应字体，参照第二个链接

安装如果出现错误，可参照第三个链接

[How To Install wkhtmltopdf In CentOS 7.0](https://jaimegris.wordpress.com/2015/03/04/how-to-install-wkhtmltopdf-in-centos-7-0/)

[python wkhtmltopdf使用与注意事项](http://kaito-kidd.com/2015/03/12/python-html2pdf/) 

[Python pip install fails: invalid command egg_info](http://stackoverflow.com/questions/11425106/python-pip-install-fails-invalid-command-egg-info)

1. 安装wkhtmltopdf

   - Step 1: Preparation

     Login to your CentOS machine. Make sure that you have root access. It is up to you on how you gain a root access by logging in directly as root user or do an su - command.

   - Step 2: Install Dependencies

     Now that I mentioned it, there are two items needed in order to install the wkhtmltopdf:

     xorg-x11-fonts-Type1

     xorg-x11-fonts-75dpi

     Install the two items with the following command

     ```shell
     yum install -y xorg-x11-fonts-75dpi
     yum install -y xorg-x11-fonts-Type1   
     ```

   - Step 3: Install wkhtmltopdf

     Next, download the wkhtmltopdf RPM file.

     ```shell
     $ wget http://download.gna.org/wkhtmltopdf/0.12/0.12.2.1/wkhtmltox-0.12.2.1_linux-centos7-amd64.rpm
     ```

     As of the published date, there is no 32-bit version of the said tool available for download. After the file has been downloaded, run the command:

     ```shell
     $ rpm -Uvh wkhtmltox-0.12.2.1_linux-centos7-amd64.rpm
     ```

   - Step 4: Testing

     And now for the test. Run the command (and make sure that the computer is accessible to internet):

     ```shell
     wkhtmltopdf http://www.google.com.ph google.pdf
     # During the generation, it will show something like this:
     Loading pages (1/6)
     Counting pages (2/6) 
     Resolving links (4/6) 
     Loading headers and footers (5/6) 
     Printing pages (6/6)
     Done
     ```

     If the command generates the from the website to PDF file successfully, again, it is obvious that the wkhtmltopdf is working.

2. 安装中文字体        

   > 中文乱码说明：    
   > 保证网页编码为UTF-8，GBK、GB2312网上说好像支持不太好，我未测试；    
   > 如果导出是乱码，注意不是方框方框，则是网页编码问题；    
   > 如果导出是方框方框，表示服务器未安装中文字体，安装字体即可，安装下面说明；    
   > 安装中文字体：    
   > - 查看目前安装字体：fc-list    
   > - 下载所需字体,例如msyh.ttf    
   > - mkdir /usr/share/fonts/zh_CN    
   > - mv msyh.ttf /usr/share/fonts/zh_CN    
   > - 执行fc-cache -fv    
   >   查看是否安装成功：fc-list，查看是已安装

##### Python实现

```python
url = "http://www.google.com"
pdf = pdfkit.from_url(url, False)
abc = StringIO()
abc.write(pdf)
abc.seek(0)
return send_file(abc, attachment_filename="test.pdf",
                 as_attachment=True, mimetype="application/pdf")
```