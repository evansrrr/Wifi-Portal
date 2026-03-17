# Wifi-Portal

WiFi 钓鱼攻击模拟工具（Captive Portal Phishing Demo）

**仅限合法安全研究、教育、授权测试使用。严禁非法用途。**

## 功能

- 快速创建开放 WiFi 热点
- 仿冒常见 captive portal 登录页
  - 中国移动/联通/电信
  - 星巴克、麦当劳、机场、高铁、酒店等
- 捕获账号密码 / 手机号 / 验证码
- 支持自定义页面模板
- 凭证实时显示 + 保存到文件
- 轻量级，支持 Kali / 树莓派

## 快速开始

```bash
git clone https://github.com/evansrrr/Wifi-Portal.git
cd Wifi-Portal
```

# 安装依赖（仅一次）

```bash
pip install os csv datetime flask subprocess colorama
```

# 配置（SSID、模板等）

```bash
vim wifi_portal.py
```

# 启动

```bash
sudo python3 wifi_portal.py
```

# 博文地址

[原post](https://ich.cc.cd/2026/03/16/Wifi%E9%92%93%E9%B1%BC%E6%94%BB%E5%87%BB%E6%A8%A1%E6%8B%9F/)