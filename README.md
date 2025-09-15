# Python训练：文件读写操作



### 代码详情：

单个文件比较小，所以整个读到内存里再进行处理，处理完后覆盖回去

用多进程来并发

加了个计时器和单进程开关，可以拿来比较二者性能开销



### 作业要求：

下载网址https://datadryad.org/stash/dataset/doi:10.5061/dryad.bzkh1899q中的数据资源文件：

Nov 11, 2021 version files

- [DRIAMS_A.tar.gz](https://datadryad.org/stash/downloads/file_stream/1158722 "DRIAMS_A.tar.gz")86.16 GB
- [DRIAMS_B.tar.gz](https://datadryad.org/stash/downloads/file_stream/1144870 "DRIAMS_B.tar.gz")3.69 GB
- [DRIAMS_C.tar.gz](https://datadryad.org/stash/downloads/file_stream/1144871 "DRIAMS_C.tar.gz")12.43 GB
- [DRIAMS_D.tar.gz](https://datadryad.org/stash/downloads/file_stream/1158723 "DRIAMS_D.tar.gz")42.56 GB
- [README.md](https://datadryad.org/stash/downloads/file_stream/1144872 "README.md")5.26 KB

可以先下载最小的DRIAMS_B.tar.gz，解压缩后里面的binned_6000、preprocessed和raw 3个目录里都有几千个txt文件，每个文件的内容是：1到3行的标题及注释说明，紧跟其后的是几千到几万行的列数值。可以发现，这些数值的精度都相当高，达到小数点后十几位，导致txt文件大小过大。

现在需要编程对这些txt进行改写，以缩减这些文件的磁盘空间占用。

要求：

1、文件解压缩后原地改写，保留所有txt文件里的标题和注释说明行；

2、对binned_6000目录里的txt文件里的数据列，第1列保持不变（即保留整数）；第2列归一化到9999，保留整数位；

3、对preprocessed目录里的txt文件里的数据列，第1列缩减精度到2位小数；第2列归一化到9999，保留整数位；

4、对raw目录里的txt文件里的数据列，第1列缩减精度到2位小数；第2列归一化到9999，保留整数位；

5、数据列的分隔符——空格——保持不变；

6、编程语言不限，思考如何提升处理速度，比较不同处理方式的用时差异。

优化出处理速度最快的方法后，就可以再去处理更大的DRIAMS_A.tar.gz、DRIAMS_C.tar.gz和DRIAMS_D.tar.gz压缩文件了。
