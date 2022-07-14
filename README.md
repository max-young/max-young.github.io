### 关于

个人博客, 参(chao)照(xi)了[Sébastien Saunier](https://raw.github.com/ssaunier/ssaunier.github.io/)和[YongYuan's Homepage](http://yongyuan.name/)两位的博客, 非常感谢

### 博客地址

[max young's homepage](https://max-young.github.io/)


### 配置

1. 把模板下载过去，如果你没有用单独的域名的话，把`CNAME`文件删掉，然后顺便把`_posts`里的文章删掉； 
2. 配置`_config.yml`，比如把title修改成你自己； 

### 开发

安装依赖(Ubuntu系统):
```shell
sudo apt-get install ruby ruby-all-dev
sudo gem install bundler jekyll
```
启动:
```shell
bundle exec jekyll build
bundle exec jekyll serve
```
如果报bundler版本不够, 按如下操作:
```shell
sudo gem update --system
bundle update --bundler
```

### 发布博文

在_post下增加markdown文件即可