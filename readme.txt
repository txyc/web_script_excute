工程目标：
1、配置docker环境——掌握linux下docker镜像的制作、发布、使用
2、部署jenkins服务——掌握linux下jenkins的部署使用，以及docker镜像中的jenkins的部署使用
3、通过网页传输参数给python执行程序——搭建前端服务器，暴露input输入接口，接收用户输入，将参数传递给python程序去执行
4、pytest配合argv/argparse/click接收外部参数——掌握pytest测试框架，掌握python参数传输的方法
5、selenium + webdriver读取指定网络路径信息——掌握selenium的使用
6、整合上述所有步骤打包成一套web自动化测试的解决方案
7、在云服务器上完成上述解决方案的部署，并生成docker镜像

业务逻辑控制：
1、获取一些手动填好的excel表格，包含姓名、电话号码、来访目的、接待人等信息的照片
2、找一个提取图片信息的网络服务——>读取图片结果然后展示在网页中
3、调用2中的网页服务读取1中的数据，并将数据提取出来
4、将3中的数据存入数据库、excel表
工程实现：
1、网页上定期读取指定文件夹下面的照片，启动jenkins服务
2、提供给jenkins一个照片路径参数，启动一个docker服务
3、启动docker服务执行业务逻辑