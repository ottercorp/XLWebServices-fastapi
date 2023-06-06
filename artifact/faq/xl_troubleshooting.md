# XIVLauncher 常见问题解答

## 目录

### 信息

<!--(- [如何禁用自动登录？](#q-how-do-i-disable-autologin)-->

- [XIVLauncher、Dalamud 和 Dalamud 插件是否安全可靠？](#q-xivlauncherdalamud-和-dalamud-插件是否安全可靠)
- [如何卸载 XIVLauncher？](#q-如何卸载-xivlauncher)
- [插件/ XIVLauncher 是否在更新日可用？](#q-插件-xivlauncher-是否在更新日可用)
- [我能在补丁上线之前使用 XIVLauncher 提前登录吗？](#q-我能在补丁上线之前使用-xivlauncher-提前登录吗)
- [我在哪里可以找到我的 FFXIV 安装路径？](q-我在哪里可以找到我的-ffxiv-安装路径)

<!-- - [如何将旧的 Wine 前缀中的 FFXIV 和/或 XIVLauncher 文件迁移到新的前缀中？ [Linux]](#q-how-do-i-migrate-ffxiv-andor-xivlauncher-files-from-an-old-wine-prefix-to-a-new-one-linux) -->

- [如何将 FFXIV 和/或 XIVLauncher 文件从旧的安装迁移到新的安装？[Windows]](#q-如何将-ffxiv-和或-xivlauncher-文件从旧的安装迁移到新的安装windows)

<!-- - [关于 Steam 支持有什么需要注意的事项？](#q-whats-the-deal-with-steam-support) -->

### 故障排除

- [打开程序时，我收到一条错误消息，提示 XIVLauncher 无法检查更新](#q-打开程序时我收到一条错误消息提示-xivlauncher-无法检查更新)
- [我在 Linux 上不断收到“XIVLauncher 失败，无法更新”的错误](#q-我在-linux-上不断收到xivlauncher-失败无法更新的错误)
- [为什么游戏内插件 (Dalamud) 不起作用或插件不显示？](#q-为什么游戏内插件-dalamud-不起作用或插件不显示)
- [如何将 XIVLauncher 和 Dalamud 加入防病毒白名单，以免受到防病毒软件的干扰？](#q-如何将-xivlauncher-和-dalamud-加入防病毒白名单以免受到防病毒软件的干扰)
- [XIVLauncher 不保存我的新密码 / 如何清除保存的密码？](#q-xivlauncher-不保存我的新密码--如何清除保存的密码)
- [我认为 XIVLauncher 导致了蓝屏死机。哪些信息有助于缩小问题范围？](#q-我认为-xivlauncher-导致了蓝屏死机哪些信息有助于缩小问题范围)
- [如何解决启动时的崩溃问题？](#q-如何解决启动时的崩溃问题)
- [网络连接正常但是无法更新XIVLauncher_CN、Dalamud或者无法加载主库插件列表](#q-网络连接正常但是无法更新xivlauncher_cndalamud或者无法加载主库插件列表)
- [官方启动器无法工作 / XIVLauncher_CN 在检查更新时失败 / 无法验证补丁文件](#qq-官方启动器无法工作--xivlauncher_cn-在检查更新时失败--无法验证补丁文件)
- [如何在 RivaTuner/RTSS 中设置注入延迟](#q-如何在-rivatunerrtss-中设置注入延迟)
- [我可以修复我的FFXIV安装吗？](#q-我可以修复我的ffxiv安装吗)
- [在尝试更新FFXIV时，如何修复版本检查错误？](#q-在尝试更新ffxiv时如何修复版本检查错误)
- [我在安装了 TexTools 的情况下更新了游戏。如何修复崩溃问题？](#q-我在安装了-textools-的情况下更新了游戏如何修复崩溃问题)

### 其他

<!-- [请勿以管理员身份运行 XIVLauncher](#do-not-run-xivlauncher-as-admin)\-->
- [XL 环境变量](#q-xl-环境变量)
- [WTFast 配置](#q-wtfast-配置)

<hr>

<!-- ### Q: 如何禁用自动登录？

打开 XIVLauncher 时，按住 Shift 键直到主窗口出现。
-->
<hr>

### Q: XIVLauncher、Dalamud 和 Dalamud 插件是否安全可靠？

是的！在 Goatcorp（和 Ottercorp），我们非常认真对待安全性。使用我们的软件不会让其他玩家察觉到您正在使用第三方修改。我们目前没有任何理由认为 Square Enix 会以任何形式检测客户端修改。 正如我们所使用的
ReShade/GShade、ACT、Teamcraft 和其他社区项目一样。

#### 一般免责声明

在游戏中，您不应提及使用 XIVLauncher 或插件，就像您不应承认使用*任何*第三方修改一样，因为从技术上讲，这违反了《最终幻想XIV》的服务条款。我们没有收到任何用户因使用 XIVLauncher、Dalamud 或 Dalamud
插件而被封禁的报告，但仍然建议您谨慎使用。所有官方支持的插件都经过代码审查，以确保它们不会利用游戏或以任何方式发送无效数据到游戏服务器。**我们无法为来自第三方插件存储库的非官方插件提供支持。您使用这些插件时需要自行承担风险。
**

此外，XIVLauncher 完全是一个__用爱发电项目__
。我们之所以这样做是因为我们觉得有趣，并非因为有报酬。这意味着我们始终尽力以专业和积极的态度迅速响应，但同时也意味着我们提供给您的所有内容都基于“尽力而为”的原则 -
维护这样的软件需要大量的时间，而且我们也只是普通人 :)

如果您对 XIVLauncher、Dalamud 或其中插件有任何疑问，请随时在我们的 [QQ频道](https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&inviteCode=CZtWN&from=181074&biz=ka&shareSource=5)
中提问。我们是一个主要讲中文的社区，对其他语言的支持可能有限。

#### XIVLauncher 安全细节

以下是关于 XIVLauncher 自身的一些附加细节。

1. XIVLauncher 是开源的。您可以在我们的开源仓库 [XIVLauncher GitHub Repo](https://github.com/ottercorp/FFXIVQuickLauncher/) 中审核代码。
2. XIVLauncher 的发布版本现在直接在 GitHub 上构建。您下载的任何内容都可以确保来自于 GitHub 仓库中所列出的开源代码版本。XIVLauncher 版本检查文件被缓存到私有的 VPS 上，以帮助减少遇到 GitHub API 限制和特定国家
   ISP 阻止的可能性。文件下载会显示我们的代理域名（`ffxiv.wang`），但这会重定向到 GitHub 或中国大陆的 CDN/云存储 （如果需要的话）。 您可以使用您选择的网络分析工具来验证此行为。并且只有极少部分开发者可以通过控制台进行访问。
3. 如果 XIVLauncher 已被修改，或者您正在运行用于开发的版本，它将清楚地表明它是调试版本或其他测试/不受支持的版本。 ![unsupported xivlauncher build](images/xivlauncher_unsupported.png).
4. XIVLauncher 使用 Windows 凭据管理器安全地存储您的帐户凭据（包括密码和快速登录凭据）。 您的密码和凭据已加密，只能由授权程序访问。 但是，这确实意味着如果有人设法访问您的计算机，他们可以从技术上提取您的密码与凭据。（但这种情况下您需要优先考虑的或许不只是账号安全的问题。）
    * XLCore（Linux 原生版 XIVLauncher）使用 `libsecret` 安全存储您的帐户凭据。`gnome-keyring`、`kwallet`（提供 KDE Framework 版本 5.97.0 或更新版本）以及其他实现了 `org.freedesktop.secrets`
      的密钥管理器可以用于存储和管理这些凭据。
5. XIVLauncher 仅与我们的安全代理、GitHub 和最终幻想14官方网站进行通信。
6. XIVLauncher 旨在完全复制与官方启动器相同的登录和授权过程。 已采取措施确保它始终与官方匹配，直至遇到相同的登录问题。 补丁下载是从SE/盛趣提供的启动器的同一个补丁列表中获得的，所有补丁文件在应用之前都经过验证是正确的。

#### Dalamud 安全细节

以下是关于 Dalamud 的一些附加细节。

1. Dalamud **是一个代码注入框架**。按定义，它看起来和行为类似于病毒程序。您的杀毒软件甚至可能将其视为有害或潜在有害软件！您可以在 FAQ
   中的[将 Dalamud 列入白名单](#q-如何将-xivlauncher-和-dalamud-加入防病毒白名单以免受到防病毒软件的干扰)，将 Dalamud 添加到白名单。**我们建议将其添加到白名单以获得最佳体验，但是您的计算环境可能不需要这样做
   **。
2. Dalamud 允许您读取游戏内存和网络数据包。 您可以将此行为与使用 ACT （Advanced Combat Tracker） 进行类比。
3. Dalamud 框架自带修改游戏内存/Hook游戏客户端内存的能力和插件可以调用的函数。 然而，我们仅在官方 [Dalamud 游戏数据 API](https://goatcorp.github.io/Dalamud/api/index.html) 中提供对游戏数据的只读访问（在适用的情况下）。

#### 插件安全细节

以下是关于 Dalamud 插件的一些额外细节。

1. 我们官方插件库中的插件已被我们视为“可以安全使用”。
2. 官方支持的插件应始终从`/xlplugins`插件安装程序直接下载/安装在游戏中。您无需手动下载或手动安装它们。
3. Dalamud 不支持第三方插件库，请阅读以下补充说明以了解：

- 我们不会为非官方插件提供技术支持。
- 虽然许多非官方插件可以安全使用，但某些插件可能会利用游戏或创建不安全的状态，以将无效数据发送到游戏服务器从而导致账号封禁。在启用不受支持的插件之前，请谨慎行事。我们不为第三方插件开发者承担任何责任。
- 不支持的插件的故障排除和问题应提交给对应插件的开发人员或其相关社区。请不要在我们的官方频道为这些插件寻求官方支持，即使它们没有另外的支持渠道。

#### 网络安全细节

除了最终幻想14官方网站外，您可能也看到以下列表的网络流量。所有连接都尽可能使用 HTTPS。（Square-Enix 和盛趣很笨，他们的一些服务不使用 HTTPS。我们不喜欢这样，但无法控制它。）

您可以在[此处](https://github.com/ottercorp/XLWebServices-fastapi)找到我们其他 Web 服务的源代码，国服可能并没有完全使用：

1. `ffxiv.wang` - 这是 XIVLauncher CN 背后的私有 VPS，由 XIVLauncher_CN 的维护者运行，用于代理和缓存 XIVLauncher 和 Dalamud 检查其版本的一些常用文件。它被用来减少到 GitHub
   的网络连接数量，这样用户就不必担心达到速率限制和连接不良/被他们国家的防火墙阻止，然后根据需要将流量引导到 GitHub。 VPS
   使用国内的CDN/云服务依次缓存数据，并且只有极少部分开发者可以通过控制台进行访问。此外，插件的使用情况和统计信息也会发送到本VPS，用于用户数据分析和制定相应的对策（敏感的用户信息将始终进行哈希处理）。
2. `github.com`、`raw.githubusercontent.com` 和 `ottercorp.github.io` - 这是 GitHub。
3. `act1.ff.sdo.com` - 检查服务器状态的盛趣站点。

<hr>

### Q: 如何卸载 XIVLauncher？

您可以通过控制面板或 Windows 10 设置应用程序像任何普通 Windows 程序一样卸载 XIVLauncher。 如果要清除它的任何痕迹，请检查并删除这些文件夹。

程序安装和旧版本：
`%localappdata%\XIVLauncher`（国际服）
`%localappdata%\goatsoft`（如果存在）

设置/插件和其他用户配置
`%appdata%\XIVLauncher`（国际服）
`安装目录\Roaming\`（国服）

<hr>

### Q: 插件/ XIVLauncher 是否在更新日可用？

请记住，许多开发者有学业/工作/两者兼顾，并且分布在各种时区。更新将在可以进行时进行。"XL 随时可能消失" 的观念仍然存在。**我们无法预测任何可能的补丁需要多少工作/时间，也无法给出任何预计时间 - 这是不可能的。**
请不要催促我们，我们在补丁日需要提供更多的支持，这样我们就无法解决问题。

#### XIVLauncher_CN：

- 用户不需要采取任何预防措施来保证 XIVLauncher 与新补丁的兼容性。
- 除非 SE 决定彻底更改身份验证或补丁下载/更新的工作方式，否则启动器将在补丁日正常工作。

#### Dalamud：

**请留意我们的[QQ频道](https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&inviteCode=CZtWN&from=181074&biz=ka&shareSource=5) 公告，在公告宣布支持之前使用注入器注入可能会导致游戏崩溃。**

- Dalamud 有一个内部机制，用于检查客户端版本和一个已列入白名单的兼容性文件。
- 如果客户端版本与白名单不匹配，Dalamud 将不会加载。
- 一旦 Dalamud 被列入白名单，下次使用 XIVLauncher 启动时它将加载。（我们也会在 Discord 上发布公告）
- Dalamud 可能或可能不需要更新以与当前客户端兼容。这取决于内部有多少变化，我们无法提供任何关于列入白名单所需时间的估计。

#### 插件：

- 预计每个补丁都会导致所有插件停止工作。
- 一旦 Dalamud 被列入白名单以适应新补丁，它将尝试加载插件。
- 完全有可能一个补丁对 Dalamud 没有问题，但却破坏了一个插件。（如果发生这种情况，您需要禁用/移除插件，直到其更新为止）

<hr>

### Q: 我能在补丁上线之前使用 XIVLauncher 提前登录吗？

**不能。**

与每次补丁维护一样，大厅服务器通常会像往常一样下线。即使您在维护期间下载和应用了补丁，您的授权几乎肯定会在系统恢复之前过期。

您可以使用 XIVLauncher 的“等待维护结束”功能，坐等启动补丁（无需登录），然后在补丁一般可用时提示您登录进行游戏补丁。

“等待维护结束”功能还可以每 ~15 秒检查服务器是否在线，以便您在服务器启动后立即登录。

与任何补丁一样，**在 Dalamud 更新以适应新的补丁内容之前，游戏内插件将被自动禁用**。请不要手动将 Dalamud 注入为启动应用程序，除非您想让客户端崩溃！
<hr>

### Q: 我在哪里可以找到我的 FFXIV 安装路径？

（也就是说，XIVLauncher 的“游戏路径”是什么意思？）

FFXIV 的安装位置取决于您是使用官方安装程序还是 Steam，安装时间以及是否安装了免费试用版等因素。这里是一些常见的路径。

无论如何，请勿选择 `boot` 或 `game` 文件夹。但是，如果您已经安装了 FFXIV 的副本，您需要选择包含它们的文件夹。

官方启动器：

- `C:\Program Files (x86)\上海数龙科技有限公司\最终幻想XIV\`

![示例](images/xivlaunchersSettings.png)


<hr>

<!--
### Q: 如何将 FFXIV 和/或 XIVLauncher 文件从旧的 Wine 前缀迁移到新的前缀？\[Linux\]

在创建了新的基于 XIVLauncher 的前缀之后，您可以从旧的 FFXIV 前缀中复制以下文件：

#### 将 FFXIV 安装从一个前缀复制到另一个前缀（或根据需要移动/创建符号链接）

- 从此处复制：`~/Games/<旧前缀>/drive_c/Program Files (x86)/SquareEnix/FINAL FANTASY XIV - A Realm Reborn`
- 复制到：
  - (Lutris) `~/Games/<新前缀>/drive_c/Program Files (x86)/SquareEnix/FINAL FANTASY XIV - A Realm Reborn`
  - (Proton) `~/.steam/steam/steamapps/steamapps/common/FINAL FANTASY XIV Online`
  - (XLCore) `~/.xlcore/ffxiv`

#### 复制用户/角色设置

- 从此处复制：`~/Games/<旧前缀>/drive_c/users/<用户名>/My Documents/My Games/FINAL FANTASY XIV - A Realm Reborn`
- 复制到：
  - (Lutris) `~/Games/<新前缀>/drive_c/users/<用户名>/Documents/My Games/FINAL FANTASY XIV - A Realm Reborn`
  - (Proton) `~/.local/share/Steam/steamapps/compatdata/39210/pfx/drive_c/users/steamuser/My Documents/My Games/FINAL FANTASY XIV - A Realm Reborn`
  - (XLCore) `~/.xlcore/ffxivConfig`

#### 复制 XIVLauncher 配置（请重新安装插件）

- 从此处复制：`~/Games/<旧前缀>/drive_c/users/<用户名>/Application Data/XIVLauncher/pluginConfigs`
- 复制到：
  - (Lutris) `~/Games/<新前缀>/drive_c/users/<用户名>/AppData/Roaming/XIVLauncher/pluginConfigs`
  - (XLCore) `~/.xlcore/pluginConfigs`

### 复制其他文件和程序到 Wine 前缀

- 从此处复制：`~/Games/<旧前缀>/drive_c`
- 复制到：
  - (Lutris) `~/Games/<新前缀>/drive_c`
  - (XLCore) `~/.xlcore/wineprefix/drive_c`

---
-->

### Q: 如何将 FFXIV 和/或 XIVLauncher 文件从旧的安装迁移到新的安装？\[Windows\]

#### 复制 FFXIV 安装文件

就大部分而言，FFXIV 是可移植的。您只需确保已根据需要安装了 DirectX。我建议先使用 SE 的安装程序安装启动器，然后如果您不想打补丁，再用备份文件替换它。

**注意**：如果您安装了 TexTools，则不应执行此操作。或者至少在执行之前，请确保还原索引/修复游戏，因为 TexTools 可能会破坏您的客户端。

- 复制用户/角色设置：`\上海数龙科技有限公司\最终幻想XIV\game\My Games`
- 复制 XIVLauncher 配置（请重新安装插件）：`[XIVLauncher_CN安装目录]\Roaming\pluginConfigs`
    - **注意**：请不要复制其他配置或文件夹，因为这些是特定于该计算机的。您应该根据每台计算机进行设置。

---
<!--
### Q: Steam 支持是怎么回事？

在 Steam 上购买 FFXIV 的玩家需要在官方启动器中将他们的 Steam 帐户与 Square Enix 帐户关联起来。我们无法绕过这一点，因此如果您拥有 Steam 服务账户，您需要确保 Steam 已经登录到正确的账户。

如果您想在非 Steam 服务账户上使用 Steam 的交互界面，请通过 Steam 将 XIVLauncher 添加为非 Steam 游戏。如果您想让 Steam 统计 FFXIV 的游戏时间，您可以在 Steam 的游戏库中右键点击该游戏，选择“属性”，然后在“启动选项”中设置为 `C:\Users\**YOUR USERNAME HERE**\AppData\Local\XIVLauncher\XIVLauncher.exe %command%`。
---
-->

### Q: 打开程序时，我收到一条错误消息，提示 XIVLauncher 无法检查更新

XIVLauncher 无法打开有几个不同的原因。 这里有几个常见的。

#### XIVLauncher 被防病毒/防火墙阻止

有关如何将 XIVLauncher 列入白名单，请参阅[防病毒 FAQ 帖子](#q-如何将-xivlauncher-和-dalamud-加入防病毒白名单以免受到防病毒软件的干扰)，了解如何将 XIVLauncher 加入白名单。

<!-- #### GitHub Rate Limits
If you've made a lot of queries to github recently, it's possible they may have rate-limited you. This is usually a combined effort of XIVLauncher, Dalamud, Dalamud plugin updates, Gshade, etc all being done in rapid succession, which shouldn't happen under normal circumstances.

1. Try to visit <https://api.github.com/rate_limit> and see if the post loads (or downloads a json file)
2. Look for `resources.core.remaining`. If it's 0, you've hit GitHub's rate limit
3. If you've hit the limit, grab the timestamp number from resources.core.reset and convert the UTC timestamp into a human-readable date. <https://www.unixtimestamp.com/> works great for this.
4. Wait the alloted time before launching again, or the timeout period could be extended (if you absolutely need to get in game, use the official launcher during this time) -->

#### 网络原因？

请尝试访问我们的[Web API](https://aonyx.ffxiv.wang/Proxy/Update/Release/RELEASES)，如果可以在浏览器访问，请自行排查本地网络设置（如代理）。

#### 仍未解决？

为了获得最快的支持，请前往 QQ频道 并在 #xivlauncher 问答帮助 频道中发布您遇到的错误、屏幕截图（如果可能）以及可以在 `Roaming`中 找到的 `output.log` 文件。
<hr>

### Q: 我在 Linux 上不断收到“XIVLauncher 失败，无法更新”的错误

在一些较新的 Linux 发行版上，已禁用了 TLS 1.0 和 1.1。这会导致 Wine 和 FFXIV/XIVLauncher 出现问题，因为它们可能无法正确协商 TLS。

您可以通过将 `dssenh` DLL 覆盖设置为 native 来解决此问题（作为环境变量或在 Lutris 中设置 `dssenh=n`）。

这也已添加到 xivlauncher Lutris 脚本中。

感谢 kainz0r 提供的提示！
![示例](images/LinuxConfigScreenshot.png)

在 **Fedora** 上？您需要运行 `sudo update-crypto-policies --set DEFAULT:FEDORA32` 以放宽安全策略，因为 Fedora 33 及更高版本的 SSL/TLS 设置更为严格。如果 `FEDORA32`
不起作用，请尝试：`sudo update-crypto-policies --set LEGACY`。
<hr>

### Q: 为什么游戏内插件 (Dalamud) 不起作用或插件不显示？

与许多其他游戏工具一样，Dalamud 通过注入 FFXIV 进程并挂钩 DirectX 来工作。 有时，它会与其他工具发生冲突或因此而无法工作。

一些可能导致问题的常见原因是：

- **常见的第三方杀毒**程序。
- **FRAPS** 请确保在打开 FFXIV 时 FRAPS 已关闭。它为 FPS 显示和/录制挂钩 DirectX。您可以在游戏运行后再打开它。
- **Logitech GHub** 我们不知道为什么这是一个有问题的程序，但确实如此。该程序可能会导致 Dalamud 在退出游戏时崩溃，让您处于卡住的黑屏状态，并且必须强行关闭。
- **MacType** 对 FFXIV 没有任何作用，因为游戏不使用系统字体。请阻止它与 FFXIV 挂钩，你会没事的。
- **MSI Afterburner** 包含 RTSS。见下文。
- **OBS** 一些直播模式涉及挂钩 DirectX 以获得更好的捕获。这可能导致插件在直播流中呈现或根本不呈现。您可能需要更改捕获方法。
- **RivaTuner**/**RTSS** 要么将 FFXIV 列入自动挂钩例外，要么 [设置 RTSS 加载延迟](#q-how-to-set-an-an-injection-delay-in-rivatunerrtss)。 RTSS 可以在 Dalamud 加载后使用，没有问题。
- **SpecialK** 这也注入到 DirectX 中，并且可以搞砸 Dalamud 的注入。它并不兼容，但您可能不应该使用它，除非您有办法在 Dalamud 加载后使其挂钩。
- **国服启动游戏时黑屏** 可能是由于国服特有的游戏公约造成了游戏的实际启动时间落后，如果游戏启动马上注入有一定的可能造成游戏黑屏，请在 XIVLauncher 的设置界面设置 5～10 秒的注入延迟。

<hr>

### Q: 如何将 XIVLauncher 和 Dalamud 加入防病毒白名单，以免受到防病毒软件的干扰？

请将以下文件夹添加到例外（或白名单）列表中：

- `(XIVLauncher_CN安装路径)`
- `%AppData%\XIVLauncher`
- 您的 FFXIV 游戏安装文件夹

之后请重新启动计算机。

**注意**：大多数程序不允许您使用 `%localappdata%` 和 `%appdata%` 的缩写。您需要使用它们的完整/真实路径（通常是 `C:\Users\AppData`，后跟 `Local` 或 `Roaming`）。

#### 重置 Dalamud

您可能还需要重置 Dalamud（插件系统）。要重置 Dalamud，请删除 `(XIVLauncher_CN安装路径)\Roaming\addon\Hooks` 文件夹。

#### 额外的例外情况

如果可能，请尝试将以下文件加入白名单：

- `(您的 FFXIV 安装路径)\game\ffxiv_dx11.exe`
- `(XIVLauncher_CN安装路径)\XIVLauncherCN.exe`
- `(XIVLauncher_CN安装路径)\app-X.Y.Z\XIVLauncher.exe`
    - **注意**：将 X.Y.Z 替换为最新可用版本。**每次启动器更新都会更改！**
- `(XIVLauncher_CN安装路径)\Roaming\addon\Hooks\W.X.Y.Z\Dalamud.Injector.exe`
    - **注意**：将 W.X.Y.Z 替换为最新可用版本。**每次 Dalamud 更新都会更改！**
- `(XIVLauncher_CN安装路径)\Roaming\addon\Hooks\W.X.Y.Z\DalamudCrashHandler.exe`
    - **注意**：将 X.Y.Z 替换为最新可用版本。**每次启动器更新都会更改！**
- `(XIVLauncher_CN安装路径)\Roaming\addon\Hooks\W.X.Y.Z\Dalamud.dll`
    - **注意**：将 W.X.Y.Z 替换为最新可用版本。**每次 Dalamud 更新都会更改！**
- `(XIVLauncher_CN安装路径)\Roaming\runtime`

#### 个别防病毒软件的操作指南

- Avast: <https://support.avast.com/en-ww/article/Antivirus-scan-exclusions>
- AVG: <https://support.avg.com/SupportArticleView?l=en&urlname=AVG-Antivirus-scan-exclusions>
- Bitdefender: <https://www.bitdefender.com/consumer/support/answer/13427/>
    - **注意**：BitDefender 用户还需要通过[BitDefender 防火墙](https://www.bitdefender.com/consumer/support/answer/13425/)将 XIVLauncher 的程序文件（`%LocalAppData%` 目录下的文件）添加到白名单中。否则，XIVLauncher
      将无法检查更新，可能无法应用补丁，并且无法下载插件。
- Kaspersky Internet Security: <https://usa.kaspersky.com/blog/kaspersky-add-exclusion/11075/>
    - **注意**：请在杀毒软件组件的“威胁和排除”部分添加**文件和文件夹**的排除项。有关详细信息，请参阅上述列表。您还可能需要明确管理需要禁用的 AV
      扫描程序。[查看此图片示例](https://user-images.githubusercontent.com/10376708/131000436-35097d20-f186-4942-ab43-73e51ff77609.png)。
    - **注意 2**：您还可能需要在**[Kaspersky 防火墙](https://support.kaspersky.com/15163)**的“应用程序规则”中将 XIVLauncher 的程序文件添加到白名单中。如果您收到与检查更新、应用补丁或下载插件相关的错误消息，并且日志显示访问权限问题，那么您就需要执行此操作。
- McAfee: <https://service.mcafee.com/webcenter/portal/cp/home/articleview?articleId=TS102056>
    - **注意**：McAfee 不允许您将文件夹添加到白名单。相反，您需要将文件添加到白名单，这更麻烦，而且还与特定版本有关。请参阅上述列表。
- Norton: <https://support.norton.com/sp/en/us/home/current/solutions/v3672136> 或 <https://www.lifewire.com/exclude-files-from-norton-antivirus-scans-153348>
    - **注意**：您还可能需要从“主动检测”或其他类似名称的功能中进行排除。
- Windows Defender: <https://support.microsoft.com/en-us/help/4028485/windows-10-add-an-exclusion-to-windows-security>

（**请谨慎操作**。如果您正在安装开发插件、第三方插件或其他非正常`/xlplugins`方法的内容，我们无法确保插件能正常工作、在游戏中不被检测到，并且不会对您的计算机造成损害。）

---

### Q: XIVLauncher 不保存我的新密码 / 如何清除保存的密码？

XIVLauncher 将用户凭据保存在 Windows 凭据管理器中。它们将被适当标记，以便您可以找到要编辑/删除的确切条目。

1. 打开 Windows 凭据管理器应用程序。最快的方法是在开始菜单中开始输入它的名称。
2. 选择 Windows 凭据按钮。
3. 滚动到看到类似 FINAL FANTASY XIV-username 的条目，并展开该条目。
4. 删除该条目。XIVLauncher 将无法加载它。
5. 现在打开 XIVLauncher 并尝试登录。

如果需要更多帮助，可以在<https://pureinfotech.com/credential-manager-windows-10/>上找到基本指南。

---

### Q: 我认为 XIVLauncher 导致了蓝屏死机。哪些信息有助于缩小问题范围？

（注意：这可能不是 XIVLauncher 的问题，但以下信息将帮助我们验证。）

1. 您获得了什么停止代码？
2. 哪个应用程序或驱动程序出现故障？
3. 这个问题是什么时候开始的？
4. 您安装了哪些插件？如果禁用它们，然后逐个选择重新启用它们，问题是否仍然存在？
5. 您是否对 XIVLauncher 进行了完全卸载和重新安装？（请参阅上面的几个帖子以获取详细信息）

如果对某些细节不确定或者如果 Windows 事件查看器没有提供相关信息，[BlueScreenView](https://www.nirsoft.net/utils/blue_screen_view.html) 可以读取内存转储文件（请让计算机在将内存转储到硬盘时完成，不要按重置按钮中断该过程）。

---

### Q: 如何解决启动时的崩溃问题？

请尝试从 Microsoft 的 <https://github.com/abbodi1406/vcredist/releases/latest> 下载并安装 VC Redist，以及 .NET 4.8
Runtime <https://dotnet.microsoft.com/download/dotnet-framework/thank-you/net48-web-installer>。

如果问题仍然存在，请加入我们的[QQ频道](https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&inviteCode=CZtWN&from=181074&biz=ka&shareSource=5) 寻求帮助。  
**注意：请确保自己没有使用任何第三方插件、没有在使用Dalamud/XIVLauncher_CN前执行特定操作**

---

### Q: 网络连接正常但是无法更新XIVLauncher_CN、Dalamud或者无法加载主库插件列表

这是一个加速器或者代理设置问题。

#### 如果你使用了加速器

已知部分加速器会导致网络问题，如`UU加速器`。请在使用加速器的时候尽量使用路由模式。  
此外，多数加速器不兼容最终幻想14（国服）和 FINAL FANTASY XIV（国际服）分别加速，请不要在使用国际服加速线路的时候，在国服使用XIVLauncher_CN或Dalamud。

#### 代理问题

代理问题不属于我们的支持项目，唯一能够提供的信息是：XIVLauncher_CN、Dalamud和主库插件列表均不需要使用代理，我们的服务会自动将国内的请求分流到国内主干网CDN上。  
如果你遇到了网络问题且没有使用加速器，请在Dalamud设置中关闭使用自定义代理，并且重启游戏。

#### 我们的服务故障

我们的独立服务器托管在与世界前列云运营商相同的机房，国内CDN使用了中国电信提供的CDN服务，而国外则使用了著名的cloudflare提供的CDN服务。  
理论上我们的服务故障的可能性极小，而且我们还有一定的灾备策略。  
如果您真的怀疑不是您自己的原因导致的无法加载，可以尝试使用浏览器访问 `https://aonyx.ffxiv.wang/` 以确定是否是服务故障。

#### 滥用/网络攻击导致的防火墙自动禁用

网络攻击无处不在，因此我们通过CDN和源服务器两层进行了网络攻击过滤。其中CDN层比较宽松，源服务器层相对严格。  
正常使用的情况下，99.99%以上都不会触发到防火墙。  
原则上我们不提供被防火墙禁止后的解封。

<!--
我们可以推荐 [MUDFISH](https://mudfish.net) 作为游玩 FFXIV 的 VPN，它价格便宜且似乎工作可靠。如果在更新补丁时出现错误，我们推荐使用 [ProtonVPN](https://protonvpn.com/)
或 [Cloudflare WARP](https://1.1.1.1/)。

要进行故障排除，您可以对 SE 的日本登录服务器 `frontier.ffxiv.com` 进行 Ping 测试。
-->
---

### Q: 官方启动器无法工作 / XIVLauncher_CN 在检查更新时失败 / 无法验证补丁文件

最有可能的情况是您的网络连接或连接到盛趣服务器和/或我们的在线服务出现了问题。但是，XIVLauncher 实际上只能获得“出现了问题”的信息。

虽然这通常是家庭网络问题，但不能保证在同一位置的多台计算机会被平衡负载到相同的服务器上（这就是为什么一台计算机正常工作而另一台不工作的原因）。

如果您确定这不是防火墙问题或速率限制问题，可以尝试以下几个方法：

- 重新启动计算机
- 重新启动网络设备（调制解调器和路由器）
- 确保硬盘不是满的
- 尝试不同的 DNS
    - DNSPod 提供 119.29.29.29 （推荐）
    - Google 提供 8.8.8.8 和 8.8.4.4
    - CloudFlare 提供 1.1.1.1 和 1.0.0.1
    - Level3 提供 4.2.2.2 和 4.2.2.4
- 检查加速器设置或者代理设置  
    - 参考[网络连接正常但是无法更新XIVLauncher_CN、Dalamud或者无法加载主库插件列表](#q-the-launcher-shows-a-red-world-icon-and-an-error-message-when-trying-to-log-in-and-the-official-launcher-doesnt-open)
- 从另一台计算机复制可正常运行的 FFXIV 安装文件
    - 最简单的方法是将文件夹复制到一个大容量的闪存驱动器或外部硬盘上。
    - 如果您熟悉设置 Windows 共享，您还可以从一台可正常工作的计算机共享驱动器/文件夹，然后通过网络将其复制到您的计算机。

---

### Q: 如何在 RivaTuner/RTSS 中设置注入延迟

1. 打开 `C:\Program Files (x86)\RivaTuner Statistics Server\Profiles\\`。
2. 使用您选择的文本编辑器打开 `ffxiv_dx11.exe.cfg` 文件。
3. 找到 `[Hooking]` 部分，并更改其中的两个参数：

```text
InjectionDelay=15000
InjectionDelayTriggers=KERNEL32.dll,USER32.dll
```

如果它们不存在，请添加它们。

---

### Q: 我可以修复我的FFXIV安装吗？

暂时不可以，但是你可以检查哪个文件出错，并让朋友拷贝给你。
如果你想要使用这个功能，在XIVLauncher_CN中，右键点击“登录”并选择“修复游戏文件”。

**请不要使用官方启动器中的修复功能！**它只会修复官方登录器**。

---

### Q: 在尝试更新FFXIV时，如何修复版本检查错误？

1. 进入`\上海数龙科技有限公司\最终幻想XIV\game\My Games`。
2. 打开`FFXIV_BOOT.cfg`文件，使用您选择的文本编辑器。
3. 将`BootVersionCheckMode`更改为`1`。
4. 重新启动游戏。

---

### Q: 我在安装了 TexTools 的情况下更新了游戏。如何修复崩溃问题？

您会知道是否受到此问题的影响，因为官方启动器也会崩溃。这个问题不是由XIVLauncher引起的。

备份您的模组文件，并[按照这个FAQ条目修复游戏](#q-can-i-repair-my-ffxiv-installation)。请注意，您的模组将被卸载。  
~~_*请不要使用tt，tt只会带来不幸——獭爹*_~~

---

### Q: XL 环境变量

如果适用，您可以设置 `XL_PRERELEASE=true` 来测试 XIVLauncher 的新版本。**如果您在不了解其作用的情况下启用此选项，我们将不会在发生问题时提供帮助。**

不再使用 wine 环境变量。只需使用与 SquirrelSetup 兼容的正常工作的 Lutris 脚本。

**如果您未使用当前版本的 XL、Dalamud 和插件，则不提供支持。请谨慎使用，因为过时的版本可能会导致崩溃。**

---

### Q: WTFast 配置

![WTFast 配置设置](images/wtfastconfig.png)

---


想要添加一个新的常见问题解答？ 请使用下面的模板，PR 到主 [常见问题](https://github.com/ottercorp/faq)

```
### Q: Basic Title
FAQ content
<hr>
```

然后使用“[Name/Title here]（#anchor here）将其添加到目录中<br>

[Return to the top](#table-of-contents)<br>
[Return to the main Readme](https://goatcorp.github.io/faq)
