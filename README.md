# Clash Rules & Dialer Proxy Generator# 简介



一个用于生成 Clash 订阅转换配置和动态代理分组的工具集。支持 AI 服务分组、落地节点优化、dialer-proxy 模式等高级功能。本项目生成适用于 [**Clash Premium 内核**](https://github.com/Dreamacro/clash/releases/tag/premium)的规则集（RULE-SET），同时适用于所有使用 Clash Premium 内核的 Clash 图形用户界面（GUI）客户端。使用 GitHub Actions 北京时间每天早上 6:30 自动构建，保证规则最新。



## 📁 项目文件## 说明



### 核心配置文件本项目规则集（RULE-SET）的数据主要来源于项目 [@Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat) 和 [@v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)；[`Apple`](https://github.com/Loyalsoldier/clash-rules/blob/release/apple.txt) 和 [`Google`](https://github.com/Loyalsoldier/clash-rules/blob/release/google.txt) 列表里的域名来源于项目 [@felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list)；中国大陆 IPv4 地址数据使用 [@17mon/china_ip_list](https://github.com/17mon/china_ip_list)。



- **`chash_rules_for_ai.ini`** - Clash 订阅转换 INI 配置文件本项目的规则集（RULE-SET）只适用于 Clash **Premium** 版本。Clash Premium 相对于普通版，增加了 **TUN 增强模式**，能接管设备所有 TCP 和 UDP 流量。

  - 包含 17 个规则集（ruleset）

  - 定义 29 个代理分组（custom_proxy_group）### Clash Premium 各版本下载地址

  - 支持 AI 服务独立分组（OpenAI、Claude、Gemini、XAI、自定义 AI）

  - 包含 7 个国家/地区自动测速组（HK/TW/SG/JP/US/KR/AU）> ⚠️ 由于 Clash 及其部分周边生态项目于 2023 年 11 月上旬删库跑路，现提供部分官方原版安装包、可执行文件，详情见 [**hidden**](https://github.com/Loyalsoldier/clash-rules/tree/hidden) 分支。

  

- **`generate_dialer_proxy.js`** - 动态代理生成脚本- Clash Premium **命令行**版：

  - 自动为节点添加 `[落地]` 前缀并配置 dialer-proxy  - [官方版](https://github.com/Loyalsoldier/clash-rules/tree/hidden/software/clash-premium)（适用于 Windows、macOS、Linux、OpenWRT 等多种平台）

  - 智能构建代理列表，确保所有分组包含必要节点  - [衍生版 Clash.Meta](https://github.com/MetaCubeX/Clash.Meta/releases)（适用于 Windows、macOS、Linux、OpenWRT 等多种平台）

  - 支持图标自动匹配- Clash Premium **图形用户界面**版：

  - 生成 29 个代理组（含自动测速和手动选择）  - [ClashN](https://github.com/2dust/clashN/releases)（适用于 Windows）

  - [ClashX Pro](https://github.com/Loyalsoldier/clash-rules/tree/hidden/software/clashx-pro)（适用于 macOS）

### 其他文件  - [Clash-verge](https://github.com/zzzgydi/clash-verge/releases)（适用于 Windows、macOS、Linux）

  - [Clash for Windows](https://github.com/Loyalsoldier/clash-rules/tree/hidden/software/clash-for-windows)（适用于 Windows、macOS、Linux）

- `oneclick.js` - 快速处理脚本  - [Clash for Android](https://apkpure.com/clash-for-android/com.github.kr328.clash/versions)（适用于 Android）

- `proxyUS.ini` - 美国节点配置

- `AI.list` - AI 服务规则列表## 规则文件地址及使用方式

- `LICENSE` - 项目许可证

### 在线地址（URL）

## 🎯 核心功能

> 如果无法访问域名 `raw.githubusercontent.com`，可以使用第二个地址（`cdn.jsdelivr.net`），但是内容更新会有 12 小时的延迟。以下地址填写在 Clash 配置文件里的 `rule-providers` 里的 `url` 配置项中。

### 1. AI 服务独立分组

- **直连域名列表 direct.txt**：

5 个 AI 服务独立管理，每个默认使用 `🌍 落地节点`：  - [https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/direct.txt](https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/direct.txt)

  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt)

- 🤖 OpenAI- **代理域名列表 proxy.txt**：

- 🤖 Claude    - [https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/proxy.txt](https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/proxy.txt)

- 🤖 Gemini  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt)

- 🤖 XAI- **广告域名列表 reject.txt**：

- 🤖 自定义 AI（包含 Copilot、Perplexity）  - [https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/reject.txt](https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/reject.txt)

  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt)

### 2. 落地节点优化架构- **私有网络专用域名列表 private.txt**：

  - [https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/private.txt](https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/private.txt)

```  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/private.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/private.txt)

🌍 落地节点- **Apple 在中国大陆可直连的域名列表 apple.txt**：

  ├─ 🌐 落地节点 - 自动选择 (url-test)  - [https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/apple.txt](https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/apple.txt)

  ├─ 香港 - 节点选择  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/apple.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/apple.txt)

  ├─ 台湾 - 节点选择- **iCloud 域名列表 icloud.txt**：

  ├─ 新加坡 - 节点选择  - [https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/icloud.txt](https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/icloud.txt)

  ├─ 日本 - 节点选择  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/icloud.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/icloud.txt)

  ├─ 美国 - 节点选择- **[慎用]Google 在中国大陆可直连的域名列表 google.txt**：

  ├─ 韩国 - 节点选择  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/google.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/google.txt)

  ├─ 澳大利亚 - 节点选择- **GFWList 域名列表 gfw.txt**：

  ├─ 手动选择  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/tld-not-cn.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/tld-not-cn.txt)

  └─ DIRECT- **Telegram 使用的 IP 地址列表 telegramcidr.txt**：

```  - [https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/telegramcidr.txt](https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/telegramcidr.txt)

  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/telegramcidr.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/telegramcidr.txt)

### 3. Dialer-Proxy 模式- **局域网 IP 及保留 IP 地址列表 lancidr.txt**：

  - [https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/lancidr.txt](https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/lancidr.txt)

脚本自动为每个原始节点生成对应的 `[落地]` 节点：  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/lancidr.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/lancidr.txt)

- **中国大陆 IP 地址列表 cncidr.txt**：

```javascript  - [https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/cncidr.txt](https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/cncidr.txt)

// 原始节点  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cncidr.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cncidr.txt)

{ name: "香港 01", server: "hk1.example.com", ... }- **需要直连的常见软件列表 applications.txt**：

  - [https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/applications.txt](https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/applications.txt)

// 生成落地节点  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/applications.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/applications.txt)

{

  name: "[落地] 香港 01",### 使用方式

  type: "dialer-proxy",

  dialer-proxy: "🔗 前置节点组"要想使用本项目的规则集，只需要在 Clash 配置文件中添加如下 `rule-providers` 和 `rules`。

}

```#### Rule Providers 配置方式



### 4. 功能分组```yaml

rule-providers:

**流媒体：**  reject:

- 🎬 奈飞分组（包含所有国家选择 + 默认全局策略）    type: http

    behavior: domain

**社交/视频/音乐：**    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt"

- 📱 社交媒体（Facebook、Telegram）    path: ./ruleset/reject.yaml

- 📺 YouTube    interval: 86400

- 🎵 Spotify

- 🎮 游戏平台  icloud:

    type: http

**系统服务：**    behavior: domain

- 💻 微软服务    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/icloud.txt"

- 🍎 苹果服务    path: ./ruleset/icloud.yaml

- 🔒 IP 伪装    interval: 86400



**核心策略：**  apple:

- 🔮 全局策略（默认使用落地节点）    type: http

- 🔗 前置节点组（DIRECT + 各国家 + 手动选择）    behavior: domain

- 🐟 漏网之鱼    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/apple.txt"

- 🛑 广告拦截    path: ./ruleset/apple.yaml

- 🎯 全球直连    interval: 86400



## 📋 代理分组统计  google:

    type: http

总计：**29 个代理组**    behavior: domain

    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/google.txt"

| 分类 | 数量 | 说明 |    path: ./ruleset/google.yaml

|-----|------|------|    interval: 86400

| 核心组 | 3 | 全局策略、前置节点组、落地节点 |

| AI 服务 | 5 | OpenAI、Claude、Gemini、XAI、自定义 AI |  proxy:

| 功能组 | 8 | 奈飞、社交、YouTube、Spotify、游戏、微软、苹果、IP伪装 |    type: http

| 地区自动 | 7 | HK/TW/SG/JP/US/KR/AU - 自动选择 |    behavior: domain

| 地区手动 | 1 | US - 节点选择 |    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt"

| 落地自动 | 1 | 🌐 落地节点 - 自动选择 |    path: ./ruleset/proxy.yaml

| 工具组 | 4 | 手动选择、漏网之鱼、广告拦截、全球直连 |    interval: 86400



## 🚀 使用方法  direct:

    type: http

### 1. 订阅转换使用    behavior: domain

    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt"

将 `chash_rules_for_ai.ini` 上传到订阅转换服务（如 subconverter），配合订阅链接使用：    path: ./ruleset/direct.yaml

    interval: 86400

```

https://your-converter.com/sub?target=clash&url=订阅链接&config=chash_rules_for_ai.ini  private:

```    type: http

    behavior: domain

### 2. 脚本动态生成    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/private.txt"

    path: ./ruleset/private.yaml

在支持自定义脚本的 Clash 客户端中使用 `generate_dialer_proxy.js`：    interval: 86400



```javascript  gfw:

// 在 Clash 配置中引用    type: http

// script: ./generate_dialer_proxy.js    behavior: domain

```    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/gfw.txt"

    path: ./ruleset/gfw.yaml

脚本会自动：    interval: 86400

- 清理不需要的字段（UDP、skip-cert-verify 等）

- 生成落地节点（dialer-proxy 模式）  tld-not-cn:

- 构建完整的代理组结构    type: http

- 添加图标 URL    behavior: domain

    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/tld-not-cn.txt"

### 3. 规则集来源    path: ./ruleset/tld-not-cn.yaml

    interval: 86400

主要使用以下高质量规则集：

  telegramcidr:

**广告拦截：**    type: http

- ACL4SSR BanAD    behavior: ipcidr

- lwd-temp Anti-IP-Attribution    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/telegramcidr.txt"

    path: ./ruleset/telegramcidr.yaml

**AI 服务：**    interval: 86400

- blackmatrix7 (OpenAI、Claude、Gemini、Copilot)

- cutethotw (Grok、Perplexity)  cncidr:

    type: http

**流媒体：**    behavior: ipcidr

- blackmatrix7 (Netflix、YouTube、Spotify、Game)    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cncidr.txt"

    path: ./ruleset/cncidr.yaml

**社交：**    interval: 86400

- blackmatrix7 (Facebook)

- Loyalsoldier (Telegram CIDR)  lancidr:

    type: http

**系统服务：**    behavior: ipcidr

- blackmatrix7 (Microsoft、Apple)    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/lancidr.txt"

    path: ./ruleset/lancidr.yaml

**代理/直连：**    interval: 86400

- ACL4SSR ProxyGFWlist

- Loyalsoldier (proxy、direct、cncidr 等)  applications:

    type: http

## ⚙️ 配置特点    behavior: classical

    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/applications.txt"

### 默认策略    path: ./ruleset/applications.yaml

    interval: 86400

| 分组类型 | 默认策略 |```

|---------|---------|

| AI 服务（5个） | 🌍 落地节点 |#### 白名单模式 Rules 配置方式（推荐）

| 奈飞分组 | 🔮 全局策略 |

| 其他功能组（8个） | 🔮 全局策略 |- 白名单模式，意为「**没有命中规则的网络流量，统统使用代理**」，适用于服务器线路网络质量稳定、快速，不缺服务器流量的用户。

| 全局策略 | 🌍 落地节点 |- 以下配置中，除了 `DIRECT` 和 `REJECT` 是默认存在于 Clash 中的 policy（路由策略/流量处理策略），其余均为自定义 policy，对应配置文件中 `proxies` 或 `proxy-groups` 中的 `name`。如你直接使用下面的 `rules` 规则，则需要在 `proxies` 或 `proxy-groups` 中手动配置一个 `name` 为 `PROXY` 的 policy。

- 如你希望 Apple、iCloud 和 Google 列表中的域名使用代理，则把 policy 由 `DIRECT` 改为 `PROXY`，以此类推，举一反三。

### 自动测速配置- 如你不希望进行 DNS 解析，可在 `GEOIP` 规则的最后加上 `,no-resolve`，如 `GEOIP,CN,DIRECT,no-resolve`。



```ini```yaml

url: https://www.gstatic.com/generate_204rules:

interval: 600  - RULE-SET,applications,DIRECT

tolerance: 50  - DOMAIN,clash.razord.top,DIRECT

```  - DOMAIN,yacd.haishan.me,DIRECT

  - RULE-SET,private,DIRECT

### 节点匹配规则  - RULE-SET,reject,REJECT

  - RULE-SET,icloud,DIRECT

**地区正则表达式：**  - RULE-SET,apple,DIRECT

- 香港：`(香港|HK|Hong\s?Kong|🇭🇰)`  - RULE-SET,google,PROXY

- 台湾：`(台湾|台灣|TW|Taiwan|🇹🇼)`  - RULE-SET,proxy,PROXY

- 新加坡：`(新加坡|狮城|SG|Singapore|🇸🇬)`  - RULE-SET,direct,DIRECT

- 日本：`(日本|JP|Japan|东京|大阪|🇯🇵)`  - RULE-SET,lancidr,DIRECT

- 美国：`(美国|US|USA|United\s?States|🇺🇸)`  - RULE-SET,cncidr,DIRECT

- 韩国：`(韩国|KR|Korea|首尔|🇰🇷)`  - GEOIP,LAN,DIRECT

- 澳大利亚：`(澳大利亚|AU|Australia|🇦🇺)````
#### 黑名单模式 Rules 配置方式



**落地节点：**- 黑名单模式，意为「**只有命中规则的网络流量，才使用代理**」，适用于服务器线路网络质量不稳定或不够快，或服务器流量紧缺的用户。通常也是软路由用户、家庭网关用户的常用模式。

- 匹配模式：`(\[落地\])`- 以下配置中，除了 `DIRECT` 和 `REJECT` 是默认存在于 Clash 中的 policy（路由策略/流量处理策略），其余均为自定义 policy，对应配置文件中 `proxies` 或 `proxy-groups` 中的 `name`。如你直接使用下面的 `rules` 规则，则需要在 `proxies` 或 `proxy-groups` 中手动配置一个 `name` 为 `PROXY` 的 policy。



## 📝 更新日志```yaml

### 2026-04-02

**精简地区分组并同步性能基线：**
- ✅ 移除 DE / UK / CA / FR / NL 五个国家地区组及其所有引用
- ✅ 保留 HK / TW / SG / JP / US / KR / AU 七个地区自动测速组
- ✅ 代理组总数从 34 组下调到 29 组
- ✅ 基于两条真实订阅建立本地 benchmark，对比分组匹配与输出结果
- ✅ 正则地区分组从 15 组降到 10 组，正则匹配次数从 1380 次降到 920 次

rules:

### 2025-11-07  - RULE-SET,applications,DIRECT

  - DOMAIN,clash.razord.top,DIRECT

**优化落地节点结构：**  - DOMAIN,yacd.haishan.me,DIRECT

- ✅ 移除了多余的 "🧭 落地节点 - 手动选择" 组  - RULE-SET,private,DIRECT

- ✅ "🌍 落地节点" 现在直接包含：自动选择 + 12国家地区 + 手动选择 + DIRECT  - RULE-SET,reject,REJECT

- ✅ 减少嵌套层级，提升用户体验  - RULE-SET,tld-not-cn,PROXY

- ✅ 总分组数从 46 个优化到 45 个  - RULE-SET,gfw,PROXY

  - RULE-SET,telegramcidr,PROXY

**修复 buildProxies 函数：**  - MATCH,DIRECT

- ✅ AI 服务正确默认到落地节点```

- ✅ 其他服务正确默认到全局策略

- ✅ 确保所有分组包含完整的核心节点列表## 致谢



**配置同步：**- [@Loyalsoldier/geoip](https://github.com/Loyalsoldier/geoip)

- ✅ INI 文件与 JS 脚本完全匹配- [@Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat)

- ✅ 所有分组名称统一- [@gfwlist/gfwlist](https://github.com/gfwlist/gfwlist)

- ✅ 移除冗余配置- [@v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)

- [@felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list)

## 🛠️ 技术细节- [@17mon/china_ip_list](https://github.com/17mon/china_ip_list)



### JS 脚本关键函数## 项目 Star 数增长趋势



**`generateLandingNodes(proxies)`**[![Stargazers over time](https://starchart.cc/Loyalsoldier/clash-rules.svg)](https://starchart.cc/Loyalsoldier/clash-rules)

- 为每个节点生成 [落地] 前缀版本
- 配置 dialer-proxy 指向前置节点组

**`cleanProxyFields(proxies)`**
- 移除 UDP 支持（dialer-proxy 不支持）
- 移除 skip-cert-verify、sni 等字段

**`buildProxies(preferredFirst, extras)`**
- 智能构建代理列表
- AI 服务优先落地节点，其他优先全局策略
- 确保包含：落地节点、全局策略、前置节点组、手动选择、DIRECT、12个地区

**`getIconForGroup(groupName)`**
- 自动匹配分组图标 URL
- 使用 Koolson/Qure 图标库

### INI 配置结构

```ini
[custom]
; 规则集定义
ruleset=分组名称,规则集URL

; 分组定义
custom_proxy_group=分组名称`类型`选项1`选项2`...

; 规则生成器
enable_rule_generator=true
overwrite_original_rules=true
```

## 📚 相关资源

- [Clash Premium](https://github.com/Dreamacro/clash/releases/tag/premium)
- [ACL4SSR 规则集](https://github.com/ACL4SSR/ACL4SSR)
- [Loyalsoldier 规则集](https://github.com/Loyalsoldier/clash-rules)
- [blackmatrix7 规则集](https://github.com/blackmatrix7/ios_rule_script)

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [@Loyalsoldier](https://github.com/Loyalsoldier) - 高质量规则集
- [@ACL4SSR](https://github.com/ACL4SSR) - 全面的规则库
- [@blackmatrix7](https://github.com/blackmatrix7) - iOS 规则脚本
- [@cutethotw](https://github.com/cutethotw) - AI 服务规则
- [@lwd-temp](https://github.com/lwd-temp) - Anti-IP-Attribution

---

**最后更新：** 2025年11月7日  
**维护者：** mci77777
