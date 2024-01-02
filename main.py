import os
from time import sleep
from packaging import version
from flask import Flask, request, jsonify
import openai
from openai import OpenAI
# import functions

# Check OpenAI version is correct
required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)
print(version.parse(openai.__version__))
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
if current_version < required_version:
  raise ValueError(f"Error: OpenAI version {openai.__version__}"
                   " is less than the required version 1.1.1")
else:
  print("OpenAI version is compatible.")

# Start Flask app
app = Flask(__name__)

# Init client
client = OpenAI(
    api_key=OPENAI_API_KEY
)  # should use env variable OPENAI_API_KEY in secrets (bottom left corner)

# Create new assistant or load existing
# assistant_id = functions.create_assistant(client)

# Load existing assistant -> OLD Version
# assistant_id = 'asst_Z45R0z1FtzO4VnASmip5BfSL'

# GPT-4 version
assistant_id = 'asst_dGTiNs8TQne7VTBdZ7Gkkaw3'
# GPT-3.5 version
# assistant_id = 'asst_Z45R0z1FtzO4VnASmip5BfSL'
# Start conversation thread
@app.route('/session/createonly', methods=['GET'])
def start_conversation():
  print("Starting a new conversation...")  # Debugging line
  thread = client.beta.threads.create()
  print(f"New session created with ID: {thread.id}")  # Debugging line
  return jsonify({"session_id": thread.id})

@app.route('/session/create', methods=['POST'])
def create_session_with_ini_msg():
  data = request.data.decode('utf-8')
  ini_message = data
  print("Starting a new session with ini_message...")  # Debugging line
  thread = client.beta.threads.create()
  print(f"New session created with ID: {thread.id} with {ini_message}")  # Debugging line
  client.beta.threads.messages.create(thread_id=thread.id,
                                      role="user",
                                      content=ini_message)
  # Run the Assistant
  run = client.beta.threads.runs.create(thread_id=thread.id,
                                        assistant_id=assistant_id)

  # Check if the Run requires action (function call)
  while True:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread.id,
                                                   run_id=run.id)
    print(f"Run status: {run_status.status}")
    if run_status.status == 'completed':
      break
    sleep(1)  # Wait for a second before checking again

  # Retrieve and return the latest message from the assistant
  messages = client.beta.threads.messages.list(thread_id=thread.id)
  response = messages.data[0].content[0].text.value

  print(f"Assistant response: {response}")  # Debugging line
  return jsonify({"session_id": thread.id, "msg_text": response})
  
  # return jsonify({"session_id": thread.id})

@app.route('/session/send', methods=['POST'])
def send_receive():
  data = request.json
  thread_id = data.get('session_id')
  user_input = data.get('msg_text', '')

  if not thread_id:
    print("Error: Missing session_id")  # Debugging line
    return jsonify({"error": "Missing session_id"}), 400

  print(f"Received message: {user_input} for session_id: {thread_id}"
        )  # Debugging line

  # Add the user's message to the thread
  client.beta.threads.messages.create(thread_id=thread_id,
                                      role="user",
                                      content=user_input)

  # Run the Assistant
  run = client.beta.threads.runs.create(thread_id=thread_id,
                                        assistant_id=assistant_id)

  # Check if the Run requires action (function call)
  while True:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                   run_id=run.id)
    print(f"Run status: {run_status.status}")
    if run_status.status == 'completed':
      break
    sleep(1)  # Wait for a second before checking again

  # Retrieve and return the latest message from the assistant
  messages = client.beta.threads.messages.list(thread_id=thread_id)
  response = messages.data[0].content[0].text.value

  print(f"Assistant response: {response}")  # Debugging line
  return jsonify({"session_id": thread_id, "msg_text": response})

# Generate response
@app.route('/chat', methods=['POST'])
def chat():
  data = request.json
  thread_id = data.get('session_id')
  user_input = data.get('msg_text', '')

  if not thread_id:
    print("Error: Missing session_id")  # Debugging line
    return jsonify({"error": "Missing session_id"}), 400

  print(f"Received message: {user_input} for session_id: {thread_id}"
        )  # Debugging line

  # Add the user's message to the thread
  client.beta.threads.messages.create(thread_id=thread_id,
                                      role="user",
                                      content=user_input)

  # Run the Assistant
  run = client.beta.threads.runs.create(thread_id=thread_id,
                                        assistant_id=assistant_id)

  # Check if the Run requires action (function call)
  while True:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                   run_id=run.id)
    print(f"Run status: {run_status.status}")
    if run_status.status == 'completed':
      break
    sleep(1)  # Wait for a second before checking again

  # Retrieve and return the latest message from the assistant
  messages = client.beta.threads.messages.list(thread_id=thread_id)
  response = messages.data[0].content[0].text.value

  print(f"Assistant response: {response}")  # Debugging line
  return jsonify({"msg_text": response})


# Run server
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
