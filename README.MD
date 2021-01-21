## <center>中国区基于CloudEndure的一键大规模在线迁移解决方案</center>
### 项目说明
在实际项目中，用户需要将不同场景的服务器（比如本地数据中心的硬件或虚拟化环境、不同的云厂商的虚机环境等）在线迁移到AWS环境中。用户往往会考虑两个非常重要的因素：
- 迁移不影响现有的业务系统
- 迁移要求简单、高效、兼容性好

针对不同的用户场景，AWS有不同的迁移方案和工具。CloudEndure迁移工具能够很好地满足在线迁移和简单易用的特点。CloudEndure是一个PAAS级别的基于Block复制的迁移方案，通常用户通过CloudEndure平台提供的Console控制台，简单的点击几下，在源服务器端安装好相关agent和环境检查即可完成相关迁移操作。但这种方式存在几个明显的不足：
- 需要用户有一定的AWS基础，事先配置好AWS VPC及网络环境
- 需要事先登录每台源服务器进行agent安装并执行环境检查
- 需要用户了解AWS EC2相关机型，以便选择与源服务器匹配的机型
- 在待迁移服务器或虚机数量比较多的情况下，重复性工作量太大
- 人为操作的地方较多，容易出错

为了解决以上问题，并继承CloudEndure强大的功能和优势。基于中国区用户的特点，开发了一键式大规模迁移的整体解决方案。
### 方案特点
- 操作简单：只需要在任何客户端（Windows或linux）安装好python环境，即可完成一键批量迁移，不需要有AWS的相关基础知识
- 功能强大：能够自动根据源端机型匹配AWS对应的最新机型。解决了Cloudendure自身默认根据源端只能匹配上一代机型的问题。同时，针对不同环境（如Amazon Linux，CentOS，Ubuntu）做了适配
- 大规模迁移：适用于大规模迁移，一次可以达到CloudEndure单项目上限（350台虚机同时迁移）
- 可定制化：根据用户特定的诉求，可以随时修改脚本，满足特定的迁移需求（如用户源环境中没装python，不用每台机器去安装，可以直接在脚本中修改，会自动帮助安装相关环境。同样也可以进行内核开发包升级或驱动安装等）
----
### 如何使用
在任何可以运行python脚本的环境中，准备好相关环境，输入Cloudendure帐号和源服务器信息后，执行"one-click-massive-migration.py"脚本即可开始所有源服务器迁移（每台源服务器启用独立thread进行迁移，非迁移完成一台再迁移另外一台），本文介绍以Windows为例。

 **迁移流程**

<table>
    <tr>
        <td rowspan="4"><center>基础环境准备</td>
        <td><center>关键事项</td>
        <td><center>具体Action</td>
   </tr>
   <tr>
        <td><font color=gray size=2>注册AWS帐号</td>   
        <td><font color=gray size=2>创建用户，授予操作EC2、VPC等相关Role，并获取AKSK</td>  
   </tr>
   <tr>
        <td><font color=gray size=2>注册Cloudendure帐号</td>
        <td><font color=gray size=2>在AWS Console提support case申请License（中国），创建迁移项目，并输入第一步的AKSK</td>
   </tr>
   <tr>
        <td><font color=gray size=2>准备Windows环境</td>
        <td><font color=gray size=2>安装python，并通过pip安装fabric库</td>
   </tr>
   <tr>
       <td rowspan="4"><center>批量迁移</td>
       <td><center><font color=gray size=2>下载源码</td>
       <td><center><font color=gray size=2>直接通过git clone或从GitHub网站下载所有源码到本地任意目录，建议放在英文目录下。https://github.com/wanggaoxiong/one-click-massive-migration/</td>
  </tr>
  <tr>
       <td><font color=gray size=2>输入Cloudendure帐号信息</td>
       <td><font color=gray size=2>直接修改“Cloudendure_Account_Info.csv”文件，在其中输入前面注册的CloudEndure帐号信息，以及项目名称</td>
  </tr>
  <tr>
       <td><font color=gray size=2>输入源服务器信息</td>
       <td><font color=gray size=2>直接修改“Source_Servers_Info.csv”文件，输入需要迁移的机器的ip、用户名、密码或key相关信息</td>
  </tr>
  <tr>
       <td><font color=gray size=2>执行迁移脚本</td>
       <td><font color=gray size=2>直接在客户端中执行“one-click-massive-migration.py” python脚本，即可自动开启大规模迁移</td>
  </tr>
</table>

**批量迁移操作步骤**

1. 准备客户端环境（以Windows为例）
- 安装python

  建议安装最新的版本，如3.9.0，默认自带pip3，以及很多模块。下载地址：https://www.python.org/downloads/windows/。 完成安装后，默认python和pip都安装成功了。
    ```
    C:\Users\Administrator>python -V
    Python 3.9.0
    C:\Users\Administrator>pip -V
    pip 20.2.3 from c:\users\administrator\appdata\local\programs\python\python39\lib\site-packages\pip (python 3.9)
    ```
- 安装fabric

  通过pip安装fabric模块，用于远程连接各个源端服务器并将相关脚本推送到源端，并在源端执行相关脚本。
  <details>
    <pre><code>
    C:\Users\Administrator>pip install fabric
    Collecting fabric
      Downloading fabric-2.5.0-py2.py3-none-any.whl (51 kB)
         |████████████████████████████████| 51 kB 145 kB/s
    Collecting paramiko>=2.4
      Downloading paramiko-2.7.2-py2.py3-none-any.whl (206 kB)
         |████████████████████████████████| 206 kB 547 kB/s
    Collecting invoke<2.0,>=1.3
      Downloading invoke-1.4.1-py3-none-any.whl (210 kB)
         |████████████████████████████████| 210 kB 2.2 MB/s
    Collecting pynacl>=1.0.1
      Downloading PyNaCl-1.4.0-cp35-abi3-win_amd64.whl (206 kB)
         |████████████████████████████████| 206 kB 3.3 MB/s
    Collecting bcrypt>=3.1.3
      Downloading bcrypt-3.2.0-cp36-abi3-win_amd64.whl (28 kB)
    Collecting cryptography>=2.5
      Downloading cryptography-3.3.1-cp36-abi3-win_amd64.whl (1.5 MB)
         |████████████████████████████████| 1.5 MB 3.3 MB/s
    Collecting cffi>=1.4.1
      Downloading cffi-1.14.4-cp39-cp39-win_amd64.whl (179 kB)
         |████████████████████████████████| 179 kB 6.4 MB/s
    Collecting six
      Downloading six-1.15.0-py2.py3-none-any.whl (10 kB)
    Collecting pycparser
      Downloading pycparser-2.20-py2.py3-none-any.whl (112 kB)
         |████████████████████████████████| 112 kB 3.3 MB/s
    Installing collected packages: pycparser, cffi, six, pynacl, bcrypt, cryptography, paramiko, invoke, fabric
    Successfully installed bcrypt-3.2.0 cffi-1.14.4 cryptography-3.3.1 fabric-2.5.0 invoke-1.4.1 paramiko-2.7.2 pycparser-2.20 pynacl-1.4.0 six-1.15.0
    WARNING: You are using pip version 20.2.3; however, version 20.3.1 is available.
    You should consider upgrading via the 'c:\users\administrator\appdata\local\programs\python\python39\python.exe -m pip install --upgrade pip' command.
    </code></pre>
      <summary>安装fabric模块:</summary>
  </details>

    默认安装了如下包：
    ```
    C:\Users\Administrator>pip freeze >requirements.txt
    C:\Users\Administrator>type requirements.txt
    bcrypt==3.2.0
    cffi==1.14.4
    cryptography==3.3.1
    fabric==2.5.0
    invoke==1.4.1
    paramiko==2.7.2
    pycparser==2.20
    PyNaCl==1.4.0
    six==1.15.0
    ```
2. 下载源码  
  直接通过git clone或从GitHub网站下载所有源码到本地任意目录，建议放在英文目录下。  
  下载地址：https://github.com/wanggaoxiong/nwcd/


3. 完善CloudEndure帐号信息  
  在下载下来的源码中找到名为“Cloudendure_Account_Info.csv”的csv文件，输入前面注册的CloudEndure帐号信息，以及建立的（迁移）项目名称，保持退出。注意，不要修改csv文件名。
    <table>
        <tr>
            <td><center>CE_User_Name</td>
            <td><center>CE_Password</td>
            <td><center>CE_Project_Name</td>
       </tr>
       <tr>
           <td><center><font color=gray size=2>输入Cloudendure帐号用户名</td>
           <td><center><font color=gray size=2>输入Cloudendure帐号密码</td>
           <td><center><font color=gray size=2>输入创建的Cloudendure迁移项目名称</td>
      </tr>
    </table>
4. 完善待迁移源服务器信息  
  在下载下来的源码中刚找到名为“Source_Servers_Info.csv”的表格，在其中输入所有待迁移的服务器相关信息。服务器如果是采用密码方式登录，则输入密码。如果是秘钥方式（如pem格式的key文件等），请输入秘钥文件所在的目录（可被访问的路径）。  
    请参考下表格式填写：
    <table>
        <tr>
            <td><center>Login_IP</td>
            <td><center>Login_port</td>
            <td><center>User_Name</td>
            <td><center>Password</td>
            <td><center>Key_Path</td>
       </tr>
       <tr>
           <td><center><font color=gray size=2>源服务器IP信息：输入可被客户端访问的公有或私有IP地址</td>
           <td><center><font color=gray size=2>访问源服务器端口信息：默认22，可不写，如果是自定义的其他端口请输入。需要注意安全组或防火墙</td>
           <td><center><font color=gray size=2>源服务器用户名：输入登录用户名</td>
           <td><center><font color=gray size=2>源服务器密码：输入登录密码，如没有可不写</td>
           <td><center><font color=gray size=2>源服务器登录秘钥：输入登录源服务器秘钥路径，如通过密码可登录，可以不写。注意在Windows环境下路径“\”需要使用转义“\\”或“/”代替</td>
      </tr>
      <tr>
          <td><center><font color=gray size=2>68.79.47.*</td>
          <td><center><font color=gray size=2>22</td>
          <td><center><font color=gray size=2>centos</td>
          <td><center><font color=gray size=2>P@ss0rd</td>
          <td><center><font color=gray size=2>C:/Users/Administrator/migration-test/*.pem</td>
     </tr>
     <tr>
         <td><center><font color=gray size=2>---</td>
         <td><center><font color=gray size=2>---</td>
         <td><center><font color=gray size=2>---</td>
         <td><center><font color=gray size=2>---</td>
         <td><center><font color=gray size=2>---</td>
    </tr>
    </table>
5. 批量迁移

- 环境检查  
  执行批量迁移前，提前检查好相关环境，避免出现agent安装不上，ENA以及Nvme驱动安装，甚至防火墙阻止agent与CloudEndure Manager Service通信等问题。  
  源服务器的操作系统内核与内核开发包版本要求匹配，如果不一致，请提前下载好匹配的内核开发包版本文件，放在同一目录下，通过修改“one-click-massive-migration.py”脚本，增加conn.put（'',''）来实现批量文件推送，通过conn.run('command action')执行自动远程批量安装操作。需要安装其他文件，操作类似。  
- 脚本文件内容如下：  
    <details>
    <pre><code>
    # coding: utf-8
    import csv
    import sys
    import os
    import threading
    import time
    import fabric
    from fabric import Connection, task
    local_script_path = os.path.dirname(__file__)
    port = 22
    def migration(servers_login):
        print ("launthing thread...")
        for i in servers_login.keys():
            if str(i) == 'Password':
                passw= servers_login[i]
            elif str(i) == 'Login_IP':
                host= servers_login[i]
            elif str(i) == 'User_Name':
                user= servers_login[i]
            elif str(i) == 'Key_Path':
                key_filename= servers_login[i]
            elif str(i) == 'Login_Port':
                port = servers_login[i]
            else: print ("load source servers info, failed")
        print ("Import the source servers information, Finished")
        print ("start the multi thread migration service...\n")
        conn = fabric.Connection(host = host, user= user, port=port, connect_kwargs={"key_filename": key_filename, "password":passw})
        conn.run('mkdir -p /tmp/temp_CE')
        conn.put(local_script_path+'/aws_model', '/tmp/temp_CE/aws_model')
        conn.put(local_script_path+'/aws-instances.csv', '/tmp/temp_CE/aws-instances.csv')
        conn.put(local_script_path+'/vlookup.sh', '/tmp/temp_CE/vlookup.sh')
        conn.put(local_script_path+'/get-source-instance-type-2.py', '/tmp/temp_CE/get-source-instance-type.py')
        conn.put(local_script_path+'/get-CPU-MEM.sh', '/tmp/temp_CE/get-CPU-MEM.sh')
        conn.put(local_script_path+'/deletion_duplication.py', '/tmp/temp_CE/deletion_duplication.py')
        conn.put(local_script_path+'/CloudEndure.py', '/tmp/temp_CE/CloudEndure.py')
        conn.put(local_script_path+'/Cloudendure_Account_Info.csv', '/tmp/temp_CE/Cloudendure_Account_Info.csv')
        conn.put(local_script_path+'/CE_Account.py', '/tmp/temp_CE/CE_Account.py')
        conn.run("sudo python /tmp/temp_CE/get-source-instance-type.py $(. /tmp/temp_CE/get-CPU-MEM.sh)")
        conn.run("sudo python /tmp/temp_CE/deletion_duplication.py")
        conn.run("sudo sh /tmp/temp_CE/vlookup.sh /tmp/temp_CE/aws_model /tmp/temp_CE/b /tmp/temp_CE/c")
        conn.run("cat /tmp/temp_CE/c|sed -n 1p |cut -d \"'\" -f 8-8 > /tmp/temp_CE/d")
        conn.run("sudo python /tmp/temp_CE/CloudEndure.py $(sudo python /tmp/temp_CE/CE_Account.py)")
        conn.close()
    with open(local_script_path+"/Source_Servers_Info.csv",'r') as f:
        reader = csv.reader(f)
        fieldnames = next(reader)
        csv_reader = csv.DictReader(f,fieldnames=fieldnames)
        j=0
        for row in csv_reader:
            j=j+1
        print ("\nReady for migration %d Servers from your source environment totally... \n" %j)
        f.close()
    source_servers = []
    with open(local_script_path+"/Source_Servers_Info.csv",'r') as f:
        reader = csv.reader(f)
        fieldnames = next(reader)
        csv_reader = csv.DictReader(f,fieldnames=fieldnames)
        for row in csv_reader:
            server = threading.Thread(target=migration, args=(row,))
            source_servers.append(server)
        f.close()
    for server in source_servers:
        server.start()
    for server in source_servers:
        server.join()
    </code></pre>
    <summary>one-click-massive-migration.py：</summary>
    </details>
- 开始迁移  
  只需要打开CMD命令界面，输入一键迁移python脚本名称或执行“python 脚本文件名”即可。如下展示一次性迁移3台服务器为例，执行one-click-massive-migration.py脚本。
    ```
    C:\Users\Administrator\Desktop\migration>one-click-massive-migration.py
    ```
    <details>
    <pre><code>
    
    C:\Users\Administrator\Desktop\migration>python one-click-massive-migration.py

    Ready for migration 3 Servers from your source environment totally...

    launthing thread...
    Import the source servers information, Finished
    start the multi thread migration service...
    launthing thread...
    launthing thread...
    Import the source servers information, Finished
    start the multi thread migration service...

    Import the source servers information, Finished
    start the multi thread migration service...

    {'vCPU-:-MEM(GB)': '2-:-4', 'Type': 't2.medium'}
    {'vCPU-:-MEM(GB)': '2-:-4', 'Type': 't3.medium'}
    {'vCPU-:-MEM(GB)': '2-:-4', 'Type': 't3a.medium'}
    {'vCPU-:-MEM(GB)': '2-:-4', 'Type': 'c5.large'}
    {'vCPU-:-MEM(GB)': '2-:-4', 'Type': 'c5d.large'}
    {'vCPU-:-MEM(GB)': '2-:-8', 'Type': 't2.large'}
    {'vCPU-:-MEM(GB)': '2-:-8', 'Type': 't3.large'}
    {'vCPU-:-MEM(GB)': '2-:-8', 'Type': 't3a.large'}
    {'vCPU-:-MEM(GB)': '2-:-8', 'Type': 'm4.large'}
    {'vCPU-:-MEM(GB)': '2-:-8', 'Type': 'm5.large'}
    {'vCPU-:-MEM(GB)': '2-:-8', 'Type': 'm5a.large'}
    {'vCPU-:-MEM(GB)': '2-:-8', 'Type': 'm5d.large'}
    r5 /tmp/temp_CE/b >> /tmp/temp_CE/c
    m5 /tmp/temp_CE/b >> /tmp/temp_CE/c
    c5 /tmp/temp_CE/b >> /tmp/temp_CE/c
    r5 /tmp/temp_CE/b >> /tmp/temp_CE/c
    m5 /tmp/temp_CE/b >> /tmp/temp_CE/c
    c5 /tmp/temp_CE/b >> /tmp/temp_CE/c
    {'vCPU-:-MEM(GB)': '1-:-1', 'Type': 't2.micro'}
    r5 /tmp/temp_CE/b >> /tmp/temp_CE/c
    m5 /tmp/temp_CE/b >> /tmp/temp_CE/c
    c5 /tmp/temp_CE/b >> /tmp/temp_CE/c
    Connecting to CloudEndure Console... Finished.
    Identifying disks for replication.
    Disk to replicate identified: /dev/nvme0n1 of size 8.0 GiB
    Connecting to CloudEndure Console... Finished.
    All disks for replication were successfully identified.
    Downloading CloudEndure Agent... Identifying disks for replication.
    Disk to replicate identified: /dev/nvme0n1 of size 8.0 GiB
    All disks for replication were successfully identified.
    Downloading CloudEndure Agent... Connecting to CloudEndure Console... Finished.
    Identifying disks for replication.
    Disk to replicate identified: /dev/xvda of size 8.0 GiB
    All disks for replication were successfully identified.
    Downloading CloudEndure Agent... Finished.
    Installing CloudEndure Agent... Finished.
    Installing CloudEndure Agent... Finished.
    Installing CloudEndure Agent... Finished.
    Adding the Source machine to CloudEndure Console... Finished.
    Finished.
    Adding the Source machine to CloudEndure Console... Finished.
    Instance ID: i-00be5cde391d70b9d.
    Installation finished successfully.
    The installation of the CloudEndure Agent has started.
    Running the Agent Installer for a 64 bit system...
    Instance ID: i-04b9ed09537c87a15.
    Installation finished successfully.
    The installation of the CloudEndure Agent has started.
    Running the Agent Installer for a 64 bit system...
    Finished.
    Adding the Source machine to CloudEndure Console... Finished.
    Instance ID: i-0ab08ea0081a58c12.
    Installation finished successfully.
    The installation of the CloudEndure Agent has started.
    Running the Agent Installer for a 64 bit system...
    t2.micro
    Fetching the installation token...
    Getting machine id...
    Waiting for Replication to complete
    Replication has not started. Waiting...
    Replication has not started. Waiting...
    Replicated 0 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 874 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 1537 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 2238 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 2960 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 3694 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 4494 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 5201 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 5919 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 6571 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 7235 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replication completed. Target machine is launchable!
    Setting blueprint...
    Blueprint was set successfully
    Launching target server
    Waiting for job to finish...
    Job started
    Started waiting for latest snapshot
    Finished waiting for latest snapshot
    Started machine conversions
    Finished machine conversions
    Started creating a replica for instance ip-172-31-43-5.cn-north-1.compute.internal
    Finished creating a replica for instance ip-172-31-43-5.cn-north-1.compute.internal
    Job finished
    Target server creation completed!
    c5.large
    Fetching the installation token...
    Getting machine id...
    Waiting for Replication to complete
    Replication has not started. Waiting...
    Replication has not started. Waiting...
    Replication has not started. Waiting...
    Replicated 0 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 882 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 1527 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 2238 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 2909 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 3600 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 4275 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 4994 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 5682 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 6416 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 7098 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replication completed. Target machine is launchable!
    Setting blueprint...
    Blueprint was set successfully
    Launching target server
    Waiting for job to finish...
    Job started
    Started waiting for latest snapshot
    Finished waiting for latest snapshot
    Started machine conversions
    Finished machine conversions
    Started creating a replica for instance ip-172-31-34-44.cn-north-1.compute.internal
    Finished creating a replica for instance ip-172-31-34-44.cn-north-1.compute.internal
    Job finished
    Target server creation completed!
    m5.large
    Fetching the installation token...
    Getting machine id...
    Waiting for Replication to complete
    Replication has not started. Waiting...
    Replicated 0 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 925 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 1601 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 2281 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 2998 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 3680 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 4359 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 5029 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 5656 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 6292 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 6961 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replicated 7623 MB out of 8192 MB bytes
    Will check again in 1 minutes. Waiting...
    Replication completed. Target machine is launchable!
    Setting blueprint...
    Blueprint was set successfully
    Launching target server
    Waiting for job to finish...
    Job started
    Started waiting for latest snapshot
    Finished waiting for latest snapshot
    Started machine conversions
    Finished machine conversions
    Started creating a replica for instance ip-172-31-36-101.cn-north-1.compute.internal
    Finished creating a replica for instance ip-172-31-36-101.cn-north-1.compute.internal
    Job finished
    Target server creation completed!

    C:\Users\Administrator\Desktop\migration>
    </code></pre>
    <summary>同时迁移3台服务器执行结果如下：</summary>
    </details>
