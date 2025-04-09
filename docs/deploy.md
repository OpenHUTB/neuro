## 网页部署
1. 生成 neuro.pdf 后，运行脚本 `src/split_pdf_with_index.py` 将在 `docs/pdf`目录下生成每个章节的 PDF 文件。
2. 编译并本地部署网页：
```shell
mkdocs serve 
```
使用浏览器打开 [http://127.0.0.1:8000](http://127.0.0.1:8000)，查看文档页面能否正常显示。

3. 部署到`github`（可选）：
```shell
mkdocs gh-deploy
```
该命令会自动将相应内容推送到项目的`gh-pages`分支上，然后在 `Github` 项目设置中选择好对应 `GitPage` 的分支，目录选择`/(root)`（注意不要是`/(docs)`，然后通过 [`https://openhutb.github.io/neuro/`](https://openhutb.github.io/neuro/) 访问即可。



### pdf转html（可选）
可以使页面打开每一章节的html文件，而不需要浏览器支持阅读PDF，但有些图片为黑色背景。
```text
1.[**大脑**与行为](html/01.html)（结构） <span id="brain_behavior"></span>
```
步骤：打开 `Microsoft Store`，搜索 Ubuntu，安装Ubuntu 20.04 子系统，然后配置环境：
```shell
wsl --set-default-version 2
# 安装ssh服务，便于本地和 Ubuntu 子系统之间交互
sudo apt-get install openssh-server
sudo systemctl enalbe ssh.service
# 解决：Failed to start OpenBSD Secure Shell server.
sudo /etc/init.d/ssh start
service sshd status
# 解决不支持明码登陆：Disconnected: No supported authentication methods available (server sent: publickey)
sudo vi /etc/ssh/sshd_config
# 将PasswordAuthentication no 修改为 PasswordAuthentication yes
sudo systemctl restart sshd.service
```


编译安装pdf2htmlEX：
```shell
git clone https://github.com/pdf2htmlEX/pdf2htmlEX.git
# 将 pdf2htmlEX 安装到 /usr/local/bin
cd pdf2htmlEX
./buildScripts/buildInstallLocallyApt

# 下载测试文件
# https://sbel.wiscweb.wisc.edu/wp-content/uploads/sites/569/2018/06/TR-2017-08.pdf
wget https://github.com/OpenHUTB/neuro/releases/download/v5.0/neuro.pdf
# 生成pdf所对应的html文件
# --zoom 页面显示时缩放的倍数
pdf2htmlEX --zoom 1.3 neuro.pdf
# 每个页面存在一个单独的文件中（内容不显示）
# pdf2htmlEX --embed cfijo --split-pages 1 --dest-dir out --page-filename test-%d.page neuro.pdf
```

将生成的html文件更新到gh-deploy分支：
```shell
# 新建孤儿分支
git checkout --orphan gp-deploy
# 清楚创建分支时拷贝过来的内容
git rm -rf .
git add .
git commit -m 'init'
git push
```