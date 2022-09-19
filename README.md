# Nemo: an acceleration framework for Maya Rigging

将nemo.mod内的路径改为Nemo的位置，然后复制到"~/maya/modules"下即可。  
加载后在maya顶部的菜单栏应该出现一个“Nemo”项。

- <NEMO_ROOT>/extern: 外部依赖
- <NEMO_ROOT>/modules: 解析Maya文件所需的配置文件
- <NEMO_ROOT>/nemo: 主体代码
- <NEMO_ROOT>/lib: 脚本依赖的Nemo库
- <NEMO_ROOT>/plug-ins: Maya插件

## Table of Contents

1. [导出(export)](#导出)
2. [上传(nemofarm)](#服务器处理)
3. [本地组装(assemble)](#组装)
4. [运行时](#运行时)
5. [检查](#检查)

## 导出

在导出工具中，用户可以通过命名或者选择策略的方式筛选控制器和模型。同时也可以开启或关闭插件。

💡 高级用户可以参考interface直接调用nemo.m2n，直接调用下层方法做更强的自定义。

导出成功后的文件：

- **Graph JSON** 描述了Rig的运算逻辑。Graph JSON中的节点命名会脱敏处理。
- Resource 是特殊的nemodata格式，它包含了模型，权重，修型等数据。
- Scene JSON 主要描述了控制器的数据。
- Debug JSON 使用户可以在本地[检查](#检查)效果错误及其具体原因。
- MAT (JSON & ma) 包含了资产使用的材质信息。

**只有 Graph JSON 需要发送到服务器处理**， 其它的文件会在后续[组装](#组装)文件时用到。

通过将资产中的几何数据隔离到Resource文件中以及重命名脱敏，这些隐私数据将无需对我们分享。

### 已知限制
- 不可以出现循环依赖(Cycle Warning)
- 表达式的部分语法暂不支持 
  * 连续赋值，如`a=b=1`
- 不支持动力学系统(毛发或肌肉)
- IK
  * preferredAngle会导致误差

## 服务器处理

通过 Nemo Farm 上传 Graph JSON 到服务器

服务器回传的内容包括：

- 编译结果(dll/so)
- Config JSON

## 组装

从服务器发送回的数据后，用户可以在本地重新组装成新的Maya文件。

主要用到的数据包括：

- 描述控制器的Scene JSON
- 存储了模型，权重，修型等数据的nemodata
- 描述了材质信息的MAT(ma & JSON)

组装完成后，工具将会把生成的Maya文件和运行时所依赖的文件保存至指定的Runtime文件夹内（注意这个文件夹在保存前会被工具清空）  
如果组装时选择相对路径模式，那么可以把这个文件夹整体打包到别处使用。  
如果选择绝对路径模式，那么移动时需要改变maya文件和config json的路径。

## 运行时

动画师使用Rig时除了需要在组装阶段生成的maya文件之外，还包括：

- `CONFIG.json` 描述了角色相关的信息，包括其它各项资源的位置。
- `<name>.so(dll)` 与角色匹配的二进制动态库。
- `<name>__RESOURCE.nemodata` 资源文件。
- `<name>__MAT.json` 材质和mesh的对应关系，在生成后不可编辑mesh部分，但可以编辑指定的材质。

> 💡 Linux系统可以考虑在env中设置`__GL_SYNC_TO_VBLANK=0`, 会节省帧刷新时间

### 代理显示模式

Nemo的代理显示模式直接将运算所得数据传输到Maya VP2的GPU管线，提高了帧速率的同时也带来一些限制。

1. 鼠标点选角色时会选中整个角色，而不能分开选择某一部分。
2. 仅支持线框显示和贴图显示，不支持"灰模"显示。
3. 模型上无法再附加变形器或控制器，也不能直接出缓存。
4. 部分高级材质或自定义材质可能不支持，譬如用到Tangent或Binormal的材质。这类角色开启代理显示时Nemo会有报错警告。

选中角色根节点后点击顶部Nemo菜单的Switch，可以在代理显示模式和实体模式间切换。实体模式没有上述问题，但速度会有所降低。

> 💡 仅支持Nvidia GPU，并且需要安装最新显卡驱动

## 检查

如果用生成的Nemo Rig去替换动画文件中的原始Rig，可能会发生效果不匹配的情况，甚至直接崩溃。此时可以使用`NemoMayaNodes`插件中的NemoCheck命令检查错误。

💡 使用NemoCheck命令需首先打开原始Rig（而非Nemo Rig），或者包含原始Rig的动画文件（此时需要设置ns命令空间）。

此命令会检查Maya中当前帧所有节点的计算结果与Nemo是否匹配，并生成日志文件。  
NemoCheck命令有两个参数，分别是[导出](#导出)的 Debug JSON 和 nemodata。运行前请确认是用相同版本的工具导出的Debug JSON。  
除此之外的Flag包括：

- `id(ignoreDeformer)`        默认为开。因为变形器检查的时间很长，所以可以用此选项跳过所有的变形器
- `ns(namespace)`             默认为空。Rig的命名空间，不需要时可以留空
- `od(outputDirectory)`       默认为空。日志输出目录，为空时输出到 Script Editor
- `s(skip)`                   默认为空。可以跳过某个节点的检查，需要跳过多个节点时用`;`分隔
- `v(verbose)`                默认为0。日志的详细程度
- `x(stopOnFirstError)`       默认为开。在第一个错误时即停止而不是检查完所有节点才停止
- `ft(focusType)`             默认为空。可以只检查某种类型的节点

### 使用方法

```python
print cmds.NemoCheck(path_debug, path_resource, ns='<your-namespace>', od='<your-log-directory>')
```

如果有错误，生成的日志文件中会包含一些 closure JSON（闭包），这些 closure 记录了节点的输入和输出，用于开发者复现 Bug 进行调试。  
由于变形器的输入可能包含资产数据，所以NemoCheck会选择最不匹配的一个点记录 closure，因此用户可以放心地将闭包与开发者共享。

### 命令崩溃时

如果 Nemo 替换后即崩溃，那么 NemoCheck 同样也可能运行即崩溃。这其实是一件好事，说明复现并捕捉到了错误。  
此时可以选择将 verbose 设置为 1，并打开日志记录。日志中可以看到在哪个节点发生了崩溃。  
将 verbose 设置为 2 时，NemoCheck 还会在检查前就为所有节点记录 closure，但这样会导致执行过程相当漫长，因此仅在必要时如此做。

### 已知限制

- closestPointOnSurface在端点处可能出现U或V的坐标与Maya发生很大漂移，这是因为在极点处U或V不影响取点的位置。
- closestPointOnMesh的最近点如果落在模型边上可能导致面ID与Maya不一致。
- transferAttriutes在投影和模型边缘非常接近时结果会不稳定。
- 欧拉角与四元数转化时结果可能会变化，这是因为同一个旋转对应有两个符号相反的四元数，而对应的欧拉角则更多。
