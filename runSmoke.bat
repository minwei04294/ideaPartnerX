::【指令格式】：python 脚本.py 大区库dbid 执行人userid 指令类型 参数1 参数2 ...
::
::【参数说明】
::1、根据fiddler抓包执行数据初始化：
::指令类型: 1
::参数1: saz文件所在绝对路径
::参数2: saz文件解压后所在绝对路径
::【示例】python 脚本.py 257 3680 1 D:/fiddlerdata D:/unzip
::
::2、根据履历构建的测试数据集id执行测试：
::指令类型: 2
::参数1: saz文件名称的列表，英文逗号','分隔
::【示例】python 脚本.py 257 3680 2 saz_filename1,saz_filename2
::
::【使用说明】
::1、执行时先执行指令类型=1再执行指令类型=2。
::2、执行时，仅需根据需要修改对应的大区库dbid、执行人userID、指令类型、参数1、参数2即可。
::3、过程中如有路径，请避免路径带空格。

python %cd%/runSmoke.py 257 3680 2 saz_filename1,saz_filename2

pause