# XIVLauncherCN Steam Deck 安装指南

## 安装

<!-- ### 在您的 Steam Deck 上安装 Steam 版本的 FFXIV

要使用 XIVLauncherCN，FFXIV 免费试用版或完整版 FFXIV 必须安装在您的 Steam Deck 的 **内部存储器** 中。 您无需启动它，也无需创建 Steam 版本的 SE 帐户，只需安装即可。 如果您在 Steam 上没有 FFXIV，请安装免费试用版。

要安装试用版，您需要在 Steam 商店中查找。 根据您之前是否在此帐户上安装了试用版，它可能会从搜索结果中隐藏。 在这种情况下，在桌面模式下寻找最终幻想系列中的 demo，或 [使用此链接进入试用版](https://store.steampowered.com/app/312060/FINAL_FANTASY_XIV_Online_Free_Trial/)。

这是在游戏模式下查看游戏窗口所必需的。 -->

### 切换到桌面模式

按住电源按钮。 选择“切换到桌面模式”

### 安装 XIVLauncherCN

打开 “Discover Store”，搜索 “XIVLauncherCN” ，然后安装。

**可选：**如果您想将 Final Fantasy XIV 安装到您的 Deck 的 MicroSD 卡或默认以外的任何文件夹 (`~/.xlcore_cn/ffxiv`)，您还需要 Discover Store 中的 `Flatseal`。

### 拷贝国服游戏文件

由于盛趣删除了早期补丁，启动器无法从头下载游戏，请通过各种方式下载国服游戏文件并转移到 Steam Deck 中。

### 添加非 Steam 游戏

在 Steam 的桌面模式中，选择“添加游戏”，向下滚动到 XIVLauncherCN，单击复选框，然后单击“添加所选程序”

在 Steam 中右键单击 XIVLauncher，选择“属性”，然后
  - 将“启动目录”替换为： `/home/deck` 或其他的非只读目录，国服的启动器需要运行在有写入权限的目录来进行登陆二维码的下载。
  - 将“启动选项”替换为： `XL_SECRET_PROVIDER=FILE %command% run --parent-expose-pids --parent-share-pids --parent-pid=1 --branch=stable --arch=x86_64 --command=xivlauncher cn.ottercorp.xivlaunchercn` 请注意，在此配置下，XIVLauncher 会将您的密码保存到您的 Steam Deck 中的文件中，因为 Valve 默认没有提供更安全的密码存储方式。 如果这对您来说是个问题，请从上面的行中省略 `XL_SECRET_PROVIDER=FILE` - 在这种情况下，XIVLauncher 将无法保存您的密码。

**不要为 XIVLauncher 设置兼容模式。** XIVLauncher 是本机 Linux 应用程序。 为它设置兼容性会破坏它。

### 允许外部文件夹访问 XIVLauncher

运行 Flatseal。 在左侧，向下滚动到 XIVLauncherCN。 在窗口的主要部分，向下滚动到“文件系统”。 单击其他文件旁边的文件夹图标。 输入您所安装最终幻想 XIV 的位置。 默认情况下，您的 MicroSD 安装到 `/run/media/mmcblk0p1`。同样的，也需要添加上一步骤的启动目录为可访问目录。

### 切换到游戏模式

在桌面上，点击“返回游戏模式”。

### 第一次设置/运行游戏

在 Steam 中运行 XIVLauncherCN。 打开 XIVLauncherCN 后，点击左下角的齿轮图标设置游戏数据路径、Dalamud 注入设置等。更改设置后，点击对号。 输入您的用户名，单击登录，扫码，然后让 XIVLauncher 更新游戏。

出现提示时，按“Steam”按钮，选择“FINAL FANTASY XIV Online Free Trial”。 片刻之后，最终幻想 XIV 将出现在屏幕上。

## 常见问题

### Q: 我是 WeGame 端，如何登陆？

暂时不支持 WeGame 端账号登陆。

### Q: 我的配置文件保存在哪里？

配置文件保存在`~/.xlcore_cn`。

### Q: 游戏随机消失，休眠后无法恢复

请确保 Steam 商店的 [FINAL FANTASY XIV Online](https://store.steampowered.com/app/39210/FINAL_FANTASY_XIV_Online/) 或 [FINAL FANTASY XIV Online Free Trial](https://store.steampowered.com/app/312060/FINAL_FANTASY_XIV_Online_Free_Trial/) 已安装在您的 Steam Deck 的 **内部存储器** 中。

### Q: 我的音频有爆裂声/失真

尝试将 “PULSE_LATENCY_MSEC=60” 添加到 Steam 启动选项的开头。

### Q: 我无法控制我的游戏

请在 Steam 中更改 “FINAL FANTASY XIV Online Free Trial” 的控制器布局，**而不是**更改 XIVLauncher 的控制器布局。

### Q: Final Fantasy XIV 无法正常关闭 / Steam 一直认为 Final Fantasy XIV 正在运行

确保在“添加非 Steam 游戏”步骤中设置了启动选项。 特别是 `--parent-expose-pids --parent-share-pids --parent-pid=1` 参数允许 XIVLauncherCN 与 Steam 通信以报告游戏结束。

### Q: XIVLauncher 在尝试通过 Steam 运行时立即关闭

不要在 Steam 中为 XIVLauncher 设置兼容模式。 XIVLauncher 是一个不需要 Proton 运行的原生 Steam 应用程序。

### Q: 我无法输入我的用户名/密码

由于 Steam 文本输入 API 的限制，请使用 Steam Deck 的游戏模式完成输入。

### Q: 我在设置界面的文本框只能够输入，无法删除已有的内容

由于 Steam 文本输入 API 的 BUG，请选中内容高亮后进行输入替换。

### Q: 我无法在游戏内聊天框中输入中文（中文字符变成问号）

游戏对于输入法的检测无法识别 Steam Deck 虚拟键盘的语言切换。

建议启用插件框架后安装 ChatTwo 插件替代游戏原本的聊天系统。

[返回顶部](#安装)\
<a href="{{ site.github.baseurl }}/">返回 FAQ 主页</a>