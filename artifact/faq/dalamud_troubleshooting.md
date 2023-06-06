# Dalamud 常见问题解答

## 目录

### 信息

- [如何安装/启用插件？](#q-如何安装/启用插件)
- [如何启用插件测试版本？](#q-如何启用插件测试版本)
- [插件的命令是什么？](#q-插件的命令是什么)
- [如何开启或关闭 Dalamud Staging？](#q-如何开启或关闭-dalamud-staging)
- [如何重置 dalamud/插件窗口位置？](#q-如何重置-dalamud插件窗口位置)
- [如何手动删除插件？](#q-如何手动删除插件)
- [为什么找不到插件？](#q-为什么找不到插件)

### 故障排除

- [尝试安装/更新/禁用插件时出现错误消息](#q-尝试安装更新禁用插件时出现错误消息)
- [Reshade 及其变体无法工作，或 Dalamud UI 失败](#q-reshade-及其变体无法工作或-dalamud-ui-失败)
- [如何修复依赖 Dalamud 提供的 opcodes 的插件？](#q-如何修复依赖-dalamud-提供的-opcodes-的插件)
- [所有插件基本上都停止工作了](#q-所有插件基本上都停止工作了)

### 杂项

- [不要期望在补丁发布日获得 XL/Dalamud/插件的更新](#q-不要期望在补丁发布日获得-xldalamud插件的更新)
- [记住，无论补丁多小，都可能破坏插件](#q-记住无论补丁多小都可能破坏插件)

<hr>

<hr />

### Q: 如何安装/启用插件？

不知道如何安装插件？ 只需在你看到游戏中的已加载信息后后键入 `/xlplugins`。

<hr />

### Q: 如何启用插件测试版本？

1. 在游戏中输入 `/xlsetting`。
2. 转到 `实验性` 标签
3. 点击 `获取插件测试版本`
4. 点击 `保存` / `保存并关闭`

**请注意，测试插件可能会有bug，并且在最终发布之前可能会发生巨大的变化。 尤其是在较新的插件上，它们可能会导致游戏崩溃。 **

如需疑难解答，请将问题/评论/问题保留在我们[QQ频道](https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&inviteCode=CZtWN&from=181074&biz=ka&shareSource=5)的`#？插件问答帮助`频道中。

<hr />

### Q: 插件的命令是什么？

插件会在插件安装窗口（`/xlplugins`）中列出它们的命令。命令 `/xlhelp` 将在你的聊天中打印所有命令。

您也可以查看 [插件库](https://xlweb.ffxiv.wang/plugin_status) 来查看是否有一些快速文档，或者查看插件的repo 以获取阅读信息。
<hr />

### Q: 如何开启或关闭 Dalamud Staging ？

#### 在游戏中（如果你还能启动）

1. 在游戏中输入 `/xldev`。
2. 点击屏幕顶部的 Dalamud 菜单。
3. 按需选择/取消选择设置。
4. 重新启动游戏。

#### 游戏外（当你遇到崩溃时）

1. 关闭游戏。
2. 转到 `.\Roaming\` 并在你选择的文本编辑器中打开 `dalamudConfig.json`。
3. 转到 `"DalamudBetaKey":` 这一行。更改值为 `"BETAKEYHERE"` 以启用 Dalamud Staging，将其更改为 **`null`**（无引号）以禁用 Dalamud Staging。
4. 保存文件。
5. 启动游戏。

- 这是为开发者准备的，而不是用户。插件测试人员只有在特别声明时才应使用它。你应该预期在 staging 构建中遇到问题和更频繁的崩溃。**谨慎使用。**
- 注意：启用 Dalamud Staging 后，你可能需要等待 Dalamud 被重新下载。
- 注意 2：你应该用真正的 beta 密钥替换 `BETAKEYHERE` 条目。**它需要引号**。
- 注意 3：确保在将 `DalamudBetaKey` 设置为 null 时没有引号。

<hr />

### Q: 如何重置 dalamud/插件窗口位置？

#### XIVLauncher_CN

1. 关闭游戏。
2. 转到 `.\Roaming\`。
3. 删除 `dalamudUI.ini`。
4. 启动游戏。

#### 注入器

1. 关闭游戏
2. 转到 注入器目录下的 `XIVlauncher`文件夹
3. 删除`dalamudUI.ini`
4. 启动游戏

<hr />

### Q: 如何手动删除插件？

#### XIVLauncher_CN

1. 关闭游戏和 XIVLauncher。
2. 转到 `.\Roaming\installedPlugins`。
3. 删除插件的文件夹。
4. 转到 `.\Roaming\devPlugins`。
5. 删除所有手动安装的插件。（检查它们是否有第三方仓库，或稍后重新安装它们。）
6. 启动游戏。

#### 注入器

1. 关闭游戏和注入器。
2. 转到 `.\XIVLauncher\\installedPlugins`。
3. 删除插件的文件夹。
4. 转到 `.\XIVLauncher\\devPlugins`。
5. 删除所有手动安装的插件。（检查它们是否有第三方仓库，或稍后重新安装它们。）
6. 启动游戏。

- 注意：你可能没有任何手动安装的插件。这没问题。

<hr />

### Q: 为什么找不到插件？

插件通常需要为新的补丁进行更新。如果只过了几天或几周，请耐心等待 -
插件通常会回来。没有估计时间，也没有服务等级协议，这取决于开发者的时间/兴趣/动力。你可以查看这个[网站](https://xlweb.ffxiv.wang/plugin_status)，看看哪些插件目前可用。
<hr />

### Q: 在尝试安装/更新/禁用插件时收到错误消息

请向我们提供更多的信息，以便我们能够帮助解答为什么会发生这种情况。

1. 哪个插件？
2. 先前的版本是否起作用，您是否知道它是什么版本？
3. 是否删除插件并尝试重新安装能否工作？
4. 您可以提供您的 `dalamud.txt` 文件吗？

<hr />

### Q: Reshade 及其变体不起作用或 Dalamud UI 失败

1. 转到 `<your game installation folder>\最终幻想XIV\game`
2. 确保游戏已关闭
3. 如果有一个名为`d3d11.dll`或`dinput8.dll`的文件**重命名**为`dxgi.dll`
4. 重新启动

如果这不起作用，请在我们的 QQ频道 联系我们。

<hr />

### Q: 如何修复依赖 Dalamud 提供的 opcodes 的插件？

某些插件和功能（Universalis 更新，PennyPincher 等）需要知道 FFXIV 客户端的当前 opcodes。这些在每个补丁中都会改变，有时在新补丁的 Dalamud 更新准备好之前可能需要更多的时间来整理。

如果你需要在更新后刷新你的 opcode 信息，请重新启动游戏。Dalamud 将在启动时检查更新的定义。

<hr />

### Q: 所有我的插件基本上都停止工作了

可能有很多事情导致这种情况，我们需要从你那里获取更多信息！

如果可能，请加入我们的 [QQ频道](https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&inviteCode=CZtWN&from=181074&biz=ka&shareSource=5) 并在我们的支持频道中提问。我们可能需要你的 `output.log`
和/或 `dalamud.log` 文件来调查原因。

如果你有任何额外的插件/注入器/模组，如 ReShade/GShade，RivaTuner/RTSS/MSI Afterburner，任何屏幕显示/覆盖，或通过 TexTools 安装的模组，这些也可能导致崩溃或冲突，知道这些也会有帮助。
<hr />

### Q: 不要指望 Dalamud/Plugin 在游戏更新日发布更新。

请记住，许多开发人员都有学校/工作/两者兼而有之，并且生活在不同的时区。 可能随时会更新 “XL可以随时消失”的概念仍然存在。（删除）
<hr />

### Q:只要游戏更新，无论更新大小都可以导致插件无法正常工作

如果您在 Dalamud 被列入补丁白名单后遇到崩溃，您将需要禁用/删除插件并等待更新。

依赖opcode的插件可能比依赖hook的插件花费稍长一些。 但这最终取决于ffxiv客户端发生了多少变化。
<hr />

想要添加一个新的常见问题解答？ 请使用下面的模板，PR 到主 [常见问题](https://github.com/ottercorp/faq)

```
### Q: Basic Title
FAQ content
<hr>
```

然后使用“[Name/Title here]（#anchor here）将其添加到目录中<br>

[返回到顶部](#table-of-contents)<br> [返回主页](https://ottercorp.github.io/faq)
