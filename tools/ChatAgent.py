
import json
from openai import OpenAI
from tools.Pusher import Pusher

def push(text):
    pusher = Pusher()
    pusher.push_notification(text)
    # TOOLS FOR THE AGENT
def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}
    

class ChatAgent:
    """
    ChatAgent is responsible for managing conversational interactions with users,
    leveraging the OpenAI API for generating responses and utilizing various tools
    for enhanced functionality.

    This class provides:
    - Integration with the OpenAI API for chat-based interactions.
    - Tool definitions for recording user details and unknown questions.
    - Mechanisms for pushing notifications and storing context about the conversation.

    Attributes:
        name (str): The name of the agent.
        openai (OpenAI): An instance of the OpenAI API client.
        about_me (str): Information about the agent or user, used for context.
        pusher (Pusher): An instance for sending push notifications.
        tools (list): A list of tool definitions for function-calling with OpenAI.
    """
    record_user_details_json = {
        "name": "record_user_details",
        "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The email address of this user"
                },
                "name": {
                    "type": "string",
                    "description": "The user's name, if they provided it"
                }
                ,
                "notes": {
                    "type": "string",
                    "description": "Any additional information about the conversation that's worth recording to give context"
                }
            },
            "required": ["email"],
            "additionalProperties": False
        }
    }

    record_unknown_question_json = {
        "name": "record_unknown_question",
        "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question that couldn't be answered"
                },
            },
            "required": ["question"],
            "additionalProperties": False
        }
    }

    def __init__(self, about_me: str):
        self.name = "Camilo Posada"
        self.openai = OpenAI()
        self.about_me = about_me
        self.pusher = Pusher()
        self.tools = [{"type": "function", "function": self.record_user_details_json},
                {"type": "function", "function": self.record_unknown_question_json}]

    def handle_tool_call(self, tool_calls):
        """
        Handles the invocation of tools (functions) requested by the language model during a chat session.

        Args:
            tool_calls (list): A list of tool call objects, each representing a function/tool the model wants to invoke.
                Each tool_call is expected to have:
                    - function.name: The name of the function/tool to call.
                    - function.arguments: A JSON string of arguments for the function.
                    - id: The unique identifier for the tool call.

        Returns:
            list: A list of dictionaries, each representing the result of a tool call, formatted for the chat API.
                Each dictionary contains:
                    - "role": Always "tool"
                    - "content": The JSON-serialized result of the tool call
                    - "tool_call_id": The id of the tool call
        """
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results


    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
            particularly questions related to {self.name}'s career, background, skills and experience. \
            Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
            You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
            Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
            If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
            If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:QA Automation Engineer\n\n## LinkedIn Profile:\n{self.about_me}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
        

    def chat(self, message, history):
        """
        Handles a chat interaction with the agent, maintaining conversation history and invoking tools as needed.

        Args:
            message (str): The latest user message to process.
            history (list): A list of previous message dictionaries representing the conversation history.

        Returns:
            str: The agent's response message content.
        """
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=self.tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
