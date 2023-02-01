# Dalamud FAQ

### Table of Contents
[How do I install/enable plugins?](#q-how-do-i-installenable-plugins) <br>
[How do I enable plugin test builds?](#q-how-do-i-enable-plugin-test-builds) <br>
[What is the command for \<insert plugin here\>?](#q-what-is-the-command-for-insert-plugin-here) <br>
[How do I turn Dalamud Staging on or off?](#q-how-do-i-turn-dalamud-staging-on-or-off) <br>
[Do not expect XL/Dalamud/Plugin updates on patch day releases](#q-do-not-expect-xldalamudplugin-updates-on-patch-day-releases) <br>
[I get an error message when trying to install/update/disable a plugin](#q-i-get-an-error-message-when-trying-to-installupdatedisable-a-plugin) <br>
[Reshade and its variants don't work or Dalamud UI fails](#q-reshade-and-its-variants-dont-work-or-dalamud-ui-fails) <br>
[How do I fix plugins that rely on Dalamud provided opcodes?](#q-how-do-i-fix-plugins-that-rely-on-dalamud-provided-opcodes) <br>
[Outdated Plugins List](#q-outdated-plugins-list) <br>
[All my plugins basically stopped working](#q-all-my-plugins-basically-stopped-working) <br>
[Remember the patches, no matter how small, can break plugins](#q-remember-the-patches-no-matter-how-small-can-break-plugins) <br>
[How do I reset dalamud/plugin window locations?](#q-how-do-i-reset-dalamudplugin-window-locations) <br>
[How do I manually delete plugins?](#q-how-do-i-manually-delete-plugins) <br>
<hr>

<hr />

### Q：如何安装/启用插件？
不知道如何安装插件？ 只需在你看到游戏中的已加载信息后后键入 `/xlplugins`。

<hr />

### Q：如何启用插件测试版本？
1. 在游戏中输入 `/xlsetting`。
2. 转到 `实验性` 标签
3. 点击 `获取插件测试版本`
4. 点击 `保存` / `保存并关闭`

**请注意，测试插件可能会有bug，并且在最终发布之前可能会发生巨大的变化。 尤其是在较新的插件上，它们可能会导致游戏崩溃。 **

如需疑难解答，请将问题/评论/问题保留在我们 discord 服务器上的 [plugin-testing](https://discord.com/channels/581875019861328007/719513457988337724) 频道中。

<hr />

### Q:  \的命令是什么？
虽然某些插件会从插件安装窗口列出它们的命令，但使用 `/xlhelp` 列出它们的命令和描述。

您也可以查看 [插件库](https://github.com/goatcorp/DalamudPlugins/wiki/Plugin-Gallery) 来查看是否有一些快速文档，或者查看插件的repo 以获取阅读信息。
<hr />

### Q：不要指望 Dalamud/Plugin 在游戏更新日发布更新。

请记住，许多开发人员都有学校/工作/两者兼而有之，并且生活在不同的时区。 可能随时会更新 “XL可以随时消失”的概念仍然存在。（删除）
<hr />

### Q：在尝试安装/更新/禁用插件时收到错误消息
请向我们提供更多的信息，以便我们能够帮助解答为什么会发生这种情况。

1. 哪个插件？
2. 先前的版本是否起作用，您是否知道它是什么版本？
3. 是否删除插件并尝试重新安装能否工作？
4. 您可以提供您的 dalamud.txt 文件吗？ 
<hr />

### Q：Reshade 及其变体不起作用或 Dalamud UI 失败
1. 转到 `<your game installation folder>\FINAL FANTASY XIV\game`
2. 确保游戏已关闭
3. 如果有一个名为`d3d11.dll`或`dinput8.dll`的文件**重命名**为`dxgi.dll`
4. 重新启动

如果这不起作用，请在我们的 Discord 服务器上联系我们。

<hr />

### Q：如何修复依赖 Dalamud 提供的操作码的插件？
某些插件和功能(Universalis 更新、PennyPincher 等) 需要了解 FFXIV 客户端的当前opcode。 这些会更改每个补丁，有时可能需要更多时间才能在新补丁的 Dalamud 更新准备好之前进行整理。

如果您需要在更新后刷新您的opcode 信息，请重新启动游戏。 Dalamud 将在启动时检查更新的定义。

<hr />

### Q：过时的插件列表
在过旧的版本, 时间/或者与兴趣的因素下，这些差价目前没有更新，开发者也知道这些。 如果您想帮助维护插件，我们可以帮助您找到他们的 repo 并联系他们（如果他们仍然活跃）。

**Chat Extender** <br> 停止版本：5.3 <br> 状态：分成多个单独的插件，可以单独维护。 (ChatBubbles 和Chat Translator是其中两个插件) <br>

**VoidList** <br> 停止版本： 5.4 <br> 状态: 由 SheepGoMeh 完全替换为 Visibility。 使用 /xlplugins 命令来安装它。 <br>
<hr />

### Q：我的所有插件基本停止工作
可能有许多事情导致这一点，我们需要从你那里获得更多信息！

如果可能，请加入我们的 [Discord 服务器](https://discord.gg/3NMcUV5) 并在 #xivlauncher_issues 频道中请求支持。

我们可能需要您的 `output.log` 或 `dalamud.log` 文件来调查原因。

了解您是否还有任何附加插件/注入器/模组，如reshade/gshade、rivatuner/rtss/msi afesburner， 任何屏幕显示/叠加层或通过 Texttool安装的模组，因为它们也可能导致崩溃或冲突。
<hr />

### Q:只要游戏更新，无论更新大小都可以导致插件无法正常工作
如果您在 Dalamud 被列入补丁白名单后遇到崩溃，您将需要禁用/删除插件并等待更新。

依赖opcode的插件可能比依赖hook的插件花费稍长一些。 但这最终取决于ffxiv客户端发生了多少变化。
<hr />


### Q：如何重置 dalamud/plugin 窗口位置？
1. 关闭游戏
2. 转到 注入器目录下的 xivlauncher文件夹
3. 删除dalamudUI.ini
4. 启动游戏

<hr />

### Q: How do I manually delete plugins?
1. Close the game and xivlauncher
2. Go to %AppData%\XIVLauncher\installedPlugins
3. Remove the folder[s] for the plugin[s]
4. Go to %AppData%\XIVLauncher\devPlugins
5. Remove all manually installed plugins. (Check if they have a third party repo or reinstall later)
6. Start the game

<hr>
想要添加一个新的常见问题解答？ 请使用下面的模板，PR 到主 [常见问题](https://github.com/goatcorp/faq)

```
### Q: Basic Title
FAQ content
<hr>
```
然后使用“[Name/Title here]（#anchor here）将其添加到目录中<br>

[返回到顶部](#table-of-contents)<br> [返回主页](https://goatcorp.github.io/faq)
