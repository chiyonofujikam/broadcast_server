# 🛰️ Broadcast Server
Roadmap Projedct : https://roadmap.sh/projects/broadcast-server


A lightweight **WebSocket-based broadcast chat server** built with **Python**, **asyncio**, and **websockets** allowing multiple clients to connect and exchange real-time messages.

This project is ideal for learning async networking in Python, or as a base for building live chat systems, notification hubs, or collaborative apps.

---

## 🚀 Features

✅ Real-time message broadcasting between multiple connected clients  
✅ Handles client disconnections gracefully  
✅ Fully asynchronous (using `asyncio` and `websockets`)  
✅ Simple CLI interface (`broadcast-server start` / `broadcast-server connect`)  
✅ Logging to both console and file (`server.log`, `client.log`)  
✅ Clean async input handling using `aioconsole`

---

## 🧱 Project Structure

```
├── README.md
├── broadcast_server
│   ├── __init__.py
│   ├── cli.py          # Command-line interface entrypoint
│   ├── client.py       # Client-side WebSocket logic
│   ├── config.py       # Shared configuration (port, host)
│   └── server.py       # WebSocket broadcast server
├── pyproject.toml      # uv project configuration
├── .logs/
└── uv.lock

````

---

## ⚙️ Requirements

- Python **≥ 3.14**
- `uv` (for dependency & virtualenv management)
- Internet access (for installing dependencies)

---

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/chiyonofujikam/broadcast_server.git
   cd broadcast_server
````

2. Create and sync your environment using **uv**:

   ```bash
   uv sync
   ```

3. (Optional) Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

---

## 🖥️ Usage

The project installs a CLI command called **`broadcast-server`**.

### 🟢 Start the server

```bash
broadcast-server start
```

This runs the WebSocket server at:

```
ws://localhost:<PORT>
```

By default, the port is defined in `config.py` (example: `8088`).

Logs will be saved to `server.log`.

---

### 💬 Connect as a client

Open another terminal and run:

```bash
broadcast-server connect
```

You can open multiple clients (each in its own terminal).
When one sends a message, all other connected clients receive it instantly.

Logs will be saved to `client.log`.

---

## 🧠 How It Works

### Server (`server.py`)

* Uses `websockets.serve()` to accept connections.
* Keeps a set of all connected clients (`connected_clients`).
* When a message arrives from one client:

  * It’s **broadcast** to all other connected clients.
* Detects disconnections and removes stale connections automatically.
* Logs all activity (connections, messages, disconnections).

### Client (`client.py`)

* Connects to the server using `websockets.connect()`.
* Uses `aioconsole` to read user input asynchronously without blocking incoming messages.
* Displays received messages in real time while still allowing input.
* Supports `exit` or `quit` commands to close gracefully.

---

## 🛠️ Development CLI (`cli.py`)

The CLI is built with **argparse**, and provides these commands:

| Command                    | Description                             |
| -------------------------- | --------------------------------------- |
| `broadcast-server start`   | Starts the WebSocket server             |
| `broadcast-server connect` | Connects a client to the running server |

Internally, it uses `subprocess.run()` to execute either `server.py` or `client.py` from the package directory.

---

## 📁 Example Run

**Terminal 1:**

```bash
$ broadcast-server start
✅ Server started at ws://localhost:8088
2025-11-10 21:10:59,319 [INFO] Client 135847012982064 connected. Total clients: 1
```

**Terminal 2:**

```bash
$ broadcast-server connect
2025-11-10 21:11:02,624 [INFO] ✅ Connected to chat server!
Enter message: hello
2025-11-10 21:11:05,736 [INFO] 📩 Received: Client 135847012982064: hello
```

**Terminal 3:**

```bash
$ broadcast-server connect
Enter message: hi there 👋
2025-11-10 21:11:12,445 [INFO] 📩 Received: Client 135847012982100: hi there 👋
```

---

## 📚 Configuration

Configuration is centralized in `config.py`.
Example:

```python
class Config:
    SERVER_HOST = "localhost"
    SERVER_PORT = 8088
```

You can adjust the host/port to your liking before running.

---

## 🧰 Tech Stack

* **Python 3.14**
* **websockets** — async WebSocket communication
* **aioconsole** — non-blocking console input
* **argparse** — command-line interface
* **uv** — modern Python project & dependency manager

---

## 🧹 Logs

* Server logs → `server.log`
* Client logs → `client.log`

They include timestamps, connection events, and messages.
