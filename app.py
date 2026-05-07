import streamlit as st
import anthropic
import json
from dotenv import load_dotenv
import os

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

tools = [
    {
        "name": "search_patient_records",
        "description": "Look up patient appointment history by patient ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "The patient ID"}
            },
            "required": ["patient_id"]
        }
    },
    {
        "name": "check_insurance",
        "description": "Check insurance status for a patient",
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "The patient ID"}
            },
            "required": ["patient_id"]
        }
    },
    {
        "name": "schedule_appointment",
        "description": "Schedule a new appointment for a patient",
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "The patient ID"},
                "specialty": {"type": "string", "description": "Medical specialty"},
                "preferred_day": {"type": "string", "description": "Preferred day"}
            },
            "required": ["patient_id", "specialty"]
        }
    }
]

def execute_tool(tool_name, tool_input):
    if tool_name == "search_patient_records":
        return f"Patient {tool_input['patient_id']} has 3 upcoming appointments: cardiology Mon, GP Wed, dermatology Fri."
    elif tool_name == "check_insurance":
        return f"Patient {tool_input['patient_id']} insurance is active — Blue Cross PPO, expires Dec 2026."
    elif tool_name == "schedule_appointment":
        return f"Appointment scheduled for patient {tool_input['patient_id']} with {tool_input['specialty']} on {tool_input.get('preferred_day', 'next available')}."

def run_agent(user_query):
    messages = [{"role": "user", "content": user_query}]
    steps = []

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    steps.append(f"🔧 Used `{block.name}` → {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            messages.append({"role": "user", "content": tool_results})

        elif response.stop_reason == "end_turn":
            return response.content[0].text, steps

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# UI
st.title("🏥 Healthcare AI Agent")
st.write("Ask me about patient records, insurance, or scheduling appointments.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
query = st.chat_input("Ask about a patient...")

if query:
    # Show user message
    with st.chat_message("user"):
        st.write(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, steps = run_agent(query)
        if steps:
            with st.expander("🔍 Tools used"):
                for step in steps:
                    st.write(step)
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})