import time
from openai import OpenAI

# Enter your Assistant ID here.
ASSISTANT_ID = "asst_Of2rJSAhLl8qNRc2m9Y9VuMj"

# Make sure your API key is set as an environment variable.
client = OpenAI()

content = """
    "08:39AM Yen Rebounds Strongly After First Slide Past 160 Since 1990",
    "08:16AM Fed in holding pattern as inflation delays approach to soft landing",
    "07:42AM Musk's surprise China trip clears two key hurdles for Tesla",
    "07:40AM Stock futures climb following S&P 500's best week since November",
    "07:10AM Stock Market Today: Tesla Boosts S&P 500 and Nasdaq Futures",
    "06:45AM What tech’s choppy action means for stocks this week, according to this 20-year analysis"
"""

# Create a thread with a message.
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            # Update this with the query you want to use.
            "content": content, 
        }
    ]
)

# Submit the thread to the assistant (as a new run).
run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
print(f"👉 Run Created: {run.id}")

# Wait for run to complete.
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(f"🏃 Run Status: {run.status}")
    time.sleep(1)
else:
    print(f"🏁 Run Completed!")

# Get the latest message from the thread.
message_response = client.beta.threads.messages.list(thread_id=thread.id)
messages = message_response.data

# Print the latest message.
latest_message = messages[0]
print(f"💬 Response: {latest_message.content[0].text.value}")
