import ollama
import os
from datetime import datetime
from termcolor import colored

# Function to save conversation history
def save_history(history):
    with open('conversation_history.txt', 'a') as file:
        for entry in history:
            file.write(f"{entry['timestamp']} - {entry['role']}: {entry['content']}\n")

# Function to clear conversation history file
def clear_history_file():
    with open('conversation_history.txt', 'w') as file:
        file.write('')

# Initialize conversation history
conversation_history = []

while True:
    # Ask the user for a query
    user_query = input("Please enter your query (type 'exit' or 'quit' to stop, 'clear' to clear previous output, or 'clear history' to clear conversation history): ")

    # Check if the user wants to exit
    if user_query.lower() in ['exit', 'quit']:
        print("Exiting...")
        save_history(conversation_history)
        break

    # Check if the user wants to clear the console
    if user_query.lower() == 'clear':
        os.system('cls')  # Clear the console on Windows
        continue

    # Check if the user wants to clear the conversation history file
    if user_query.lower() == 'clear history':
        clear_history_file()
        print("Conversation history cleared.")
        continue

    # Check if the input is empty
    if not user_query.strip():
        continue

    # Add user query to conversation history with timestamp
    conversation_history.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'role': 'user',
        'content': user_query
    })

    print("Generating response...")
    print("")

    try:
        # Example of a chat interaction with streaming
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {'role': 'user', 'content': user_query}
            ],
            stream=True  # Hypothetical streaming parameter
        )

        # Print each chunk of the response as it is received
        response_content = ""
        for chunk in response:
            chunk_content = chunk.get('message', {}).get('content', '')
            print(colored(chunk_content, 'green'), end='', flush=True)
            response_content += chunk_content
        print("")  # Print a newline after the response is complete

        # Add response to conversation history with timestamp
        conversation_history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'role': 'bot',
            'content': response_content
        })

    except Exception as e:
        print(colored(f"An error occurred: {e}", 'red'))