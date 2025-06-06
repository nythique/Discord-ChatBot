# Discord AI Bot

A powerful and customizable Discord bot powered by AI, using the Groq API for natural language processing. Easily deployable with Docker.

---

## Features

- 🤖 **AI-Powered Conversations:** Interact with the bot in any channel or DM. The bot uses the Groq API for intelligent, context-aware responses.
- 🛡️ **User & Server Blacklist:** Restrict access for specific users or servers.
- 📝 **Logging:** Security and error logs are automatically managed and can be cleared with commands.
- 🔄 **Status Rotation:** The bot can automatically rotate its status message.
- 🛠️ **Admin Commands:** View error logs, clear logs, and manage configuration directly from Discord.
- 🐳 **Docker Support:** Easy deployment and management using Docker and Docker Compose.

---

## Requirements

- Python 3.10+
- Docker (optional, for containerized deployment)
- A Discord bot token ([How to create a bot](https://discord.com/developers/applications))
- Groq API key

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ia-discord-bot.git
cd ia-discord-bot
```

### 2. Configure Environment

- Copy your Discord bot token and Groq API key into the appropriate config files (see `config/` folder).
- Edit `config/controller/controller.json` to set up admin users, blacklists, etc.

### 3. Run with Python

```bash
pip install -r requirements.txt
python run.py
```

### 4. Or Run with Docker

Build and start the bot using Docker Compose:

```bash
docker-compose up --build -d
```

---

## Usage

- **Mention the bot** or send it a DM to start chatting.
- **Admin commands** (for authorized users):
  - `/empty` — Clear the bot's log files.
  - `!errors` — Show the last lines of the error log.
  - `!ping` — Check the bot's latency.

---

## Configuration

- All configuration files are in the `config/` directory.
- Logs are stored in the `logs/` directory.
- Edit `controller.json` to manage admin users, blacklists, and alert channels.

---

## Docker Volumes

- `VolumeC` — Stores configuration files.
- `VolumeLog` — Stores log files.

Make sure these Docker volumes exist or are defined in your `docker-compose.yml`.

---

## License

MIT License  
Copyright (c) 2024 Nythique

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Credits

- Developed by Nythique
- Powered by [Groq API](https://groq.com/)
- Discord.py library

---

## Support

For issues or feature requests, please open an issue on the [GitHub repository](https://github.com/nythique/discord-chatbot).