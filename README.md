# ☢️ PYSCX

![Technical banner](https://github.com/user-attachments/assets/a82243e5-6f38-46a9-89bd-453bb051b557)

![GitHub Release](https://img.shields.io/github/v/release/Oidaho/pyscx)
![GitHub Downloads](https://img.shields.io/github/downloads/Oidaho/pyscx/total)

![GitHub watchers](https://img.shields.io/github/watchers/oidaho/pyscx)
![GitHub Repo stars](https://img.shields.io/github/stars/Oidaho/pyscx)

This library is designed to simplify your interaction with the **STALCRAFT: X API**, providing a robust and developer-friendly interface for accessing game data.

Whether you're building tools, analyzing game statistics, or creating custom applications, this library offers an intuitive way to retrieve and work with **STALCRAFT: X** data.

> [!NOTE]
> STALCRAFT: X API - v1.1.0
>
> Python 3.13+

---

## ✨ Features

- **Easy-to-use interface**  
  Designed with simplicity in mind, so you can focus on building awesome stuff!  
- **Full coverage of endpoints**
  Access all available API endpoints without hassle.  
- **Automatic data wrapping**  
  Get your data in a clean, ready-to-use format.  
- **Flexible token setup**  
  Easily configure and manage your API tokens.  

## 📦 Installation

To install the library, run the following command:

```bash
pip install pyscx
```

Or, if you want to install the library directly from GitHub:

```bash
pip install git+https://github.com/Oidaho/pyscx.git
```

## 🛠️ Quick Start

Here’s a quick example to get you started:

```python
import os
from dotenv import load_dotenv

from pyscx import Server, API
from pyscx.token import Token, TokenType


load_dotenv()

app_token = Token(
    value=os.getenv("DEMO_APP_ACCESS_TOKEN"),
    type=TokenType.APPLICATION,
)
user_token = Token(
    value=os.getenv("DEMO_USER_ACCESS_TOKEN"),
    type=TokenType.USER,
)


api = API(server=Server.DEMO, tokens=[user_token, app_token])

print(api.clans(region="EU").get_all())
```

## 📚 Documentation

For detailed documentation, check out the official [docs](https://Oidaho.github.io/pyscx/)

\* at the moment, the link doesn't lead anywhere.

## 🚀 Project Ideas

Here are some cool project ideas to inspire you:

- **Auction Analyzer**: Build a tool to track item prices and find profitable deals.
- **Emission Tracker**: Create a notification system for emission start and end times.
- **Player Statistics Dashboard**: Develop a dashboard to analyze player and clan stats.
- **Social Tracker**: Monitor friends programmatically.

## 🤝 Contributing

We welcome contributions! If you have ideas, suggestions, or found a bug, please open an [issue](https://github.com/Oidaho/pyscx/issues) or submit a pull request.

## 📜 License

This project is licensed under the [GPL-3.0 License](https://github.com/Oidaho/pyscx/blob/main/LICENSE).
