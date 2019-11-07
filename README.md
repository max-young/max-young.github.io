### 关于

个人播客, 参(chao)照(xi)了[Sébastien Saunier](https://raw.github.com/ssaunier/ssaunier.github.io/)和[YongYuan's Homepage](http://yongyuan.name/)两位的博客, 非常感谢

### 博客地址

[max young's homepage'](http://www.maxyoung.online)


### 安装步骤

1. 把模板下载过去，如果你没有用单独的域名的话，把`CNAME`文件删掉，然后顺便把`_posts`里的文章删掉； 
2. 配置`_config.yml`，比如把title修改成你自己； 

```js
function DoubanApi() {
	this.defaults = {
		place:"douban",
		user:"57528320",
		api:"08242004429e34bb186c600cc7da9e31",
		book:[{status:"reading",maxnum:20},{status:"read",maxnum:100},{status:"wish",maxnum:100}],
		bookreadingtitle:"在读...",
		bookreadtitle:"读过...",
		bookwishtitle:"想读..."
	};
}
```

### 开发

```shell
bundle exec jekyll build
bundle exec jekyll serve
```

