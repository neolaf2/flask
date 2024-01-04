---
title: Flask
description: A popular minimal server framework for Python
tags:
  - python
  - flask
---

# Python Flask Example

This is a [Flask](https://flask.palletsprojects.com/en/1.1.x/) app that serves a simple JSON response.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/zUcpux)

## ✨ Features

- Python
- Flask

## 💁‍♀️ How to use

- Install Python requirements `pip install -r requirements.txt`
- Start the server for development `python3 main.py`

# ChatSession API 2024.1.1 V4

# API Base URL

[https://flask-production-1e97.up.railway.app/](https://flask-production-1e97.up.railway.app/)

# API Endpoints

### 1. Create Session with Initial Message

```json
@app.route('/session/create', methods=['POST'])
```

**Endpoint:** `POST /session/create`

**Description:** This API creates a new chat session with an initial message.

**Request Parameters:**

- `ini_message` (JSON): A JSON object containing the initial message for the chat session.

**Response:**

- `session_id` (string): Unique identifier for the created chat session.
- `msg_text` (string): The message text to start the session by agent.

**Example Request:**

```json
{
  "ini_message": {.....}
}

```

**Example Response:**

```json
{
  "session_id": "12345", 
	"msg_text": "I noticed that you've skipped several learning cards in a row. Can you tell me why?"
}

```

### 2. Send Message to Session and Get Agent Response

```python
# These two endpoints are the same.
@app.route('/session/send', methods=['POST'])
@app.route('/chat', methods=['POST'])
```

**Endpoint:** `POST /session/send` or `POST /chat`

**Description:** Sends a message to an existing chat session.

**Request Parameters:**

- `session_id` (string): The session identifier.
- `msg_text` (string): The message text sent by the user.

**Response:**

- `msg_text` (string): The response from the agent to user

**Example Request:**

```json
{
  "session_id": "12345",
  "msg_text": "Hello, this is a student."
}

```

**Example Response:**

```json
{
  "msg_text": "Hello, this is a student."
}

```

### 3. Terminate Session (Not Necessary Right Now)

**Endpoint:** `Delete /session/end`

**Description:** Terminates an existing chat session.

**Query Parameters:**

- `session_id` (string): The session identifier to be terminated.

**Response:**

- `status` (string): Status of the termination request (e.g., "success", "failed").

**Example Request:**

```
Delete /Session/end?session_id=12345

```

**Example Response:**

```json

204
```

# Samples
