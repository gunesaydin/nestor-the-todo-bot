import json

from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse

from command import Command, CommandType
from todo_list import TodoList

class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self):
        print("==========================")
        post_json = json.loads(self.post_data.decode("utf-8")) if self.post_data else {}
        print(f"POST_JSON: {post_json}")

        command, message = self.export_message_text(post_json.get("message").get("text"))
        command = Command(command)
        chat_id = post_json.get("message").get("chat").get("id")
        first_name = post_json.get("message").get("chat").get("first_name")

        response_json = self.handle_command(command, message, first_name, chat_id)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response_json.encode("utf-8"))

    def do_POST(self):
        self.do_GET()

    def get_response(self, chat_id, text="Got it!"):
        return json.dumps(
            {
                "path": self.url.path,
                "query_data": self.query_data,
                "post_data": self.post_data.decode("utf-8"),
                "form_data": self.form_data,
                "cookies": {
                    name: cookie.value
                    for name, cookie in self.cookies.items()
                },
                "method": "sendMessage",
                "text": text,
                "chat_id": chat_id,
            }
        )
    
    def export_message_text(self, text:str) -> str | str:
        """
        Export command and message body from text to a string.
        """
        stripped_text = text.strip()
        if stripped_text.strip().startswith("/"):
            command, *message = stripped_text.split(" ")
            message = " ".join(message)
        else:
            command = None
            message = stripped_text

        return command, message
    
    def handle_command(self, command:Command, message:str, first_name:str, chat_id:int) -> str:
        match command.type:
            case CommandType.START:
                return json.dumps(
                    {
                        "path": self.url.path,
                        "query_data": self.query_data,
                        "post_data": self.post_data.decode("utf-8"),
                        "form_data": self.form_data,
                        "cookies": {
                            name: cookie.value
                            for name, cookie in self.cookies.items()
                        },
                        "method": "sendMessage",
                        "text": f"Welcome {first_name}! I am Nestor, your task assistant. Use /help to see available commands.",
                        "chat_id": chat_id,
                    }
                )
            case CommandType.HELP:
                text = "/start - Begin interaction \n" + \
                    "/help - List commands and their descriptions \n" + \
                    "/add - Add a new task (e.g. /add Buy stamps)\n" + \
                    "/remove - Remove a task by index (e.g. /remove 2)\n" + \
                    "/insert - Insert a task at a specific index (e.g. /insert 3 Wash the dishes)\n" + \
                    "/list - List current tasks \n" + \
                    "/whatnow - Show current task \n" + \
                    "/done - Mark current task done\n" + \
                    "/clear - Clear all tasks \n"
            case CommandType.ADD:
                TodoList().add_task(message)
                text = f"Task added successfully. \n" + \
                    f"Task List: \n" + \
                    f"{TodoList().get_ordered_list_string()}"
            case CommandType.REMOVE:
                op = TodoList().remove_task_by_index(int(message.split(" ")[0]) - 1)
                if op:
                    text = f"Task removed successfully. \n" + \
                        f"Task List: \n" + \
                        f"{TodoList().get_ordered_list_string()}"
                else:
                    text = "Invalid task index. Please provide a valid index."
            case CommandType.INSERT:
                index, *task = message.split(" ")
                task = " ".join(task)
                if index.isnumeric() == False:
                    text = "Invalid index. Please provide a valid index."
                else:
                    TodoList().insert_task(int(index) - 1, task)
                    text = f"Task inserted successfully. \n" + \
                        f"Task List: \n" + \
                        f"{TodoList().get_ordered_list_string()}"
            case CommandType.LIST:
                if len(TodoList().get_all_tasks()) == 0:
                    text = "No tasks available."
                else:
                    text = f"Task List: \n" + \
                        f"{TodoList().get_ordered_list_string()}"
            case CommandType.WHATNOW:
                text = f"Current Task: \n" + \
                    f"-{TodoList().get_current_task()}"
            case CommandType.DONE:
                TodoList().complete_task()
                if len(TodoList().get_all_tasks()) > 0:
                    text = f"Task completed!. \n" + \
                        f"Your next task is: \n" + \
                        f"{TodoList().get_current_task()}"
                else:
                    text = "No tasks available."
            case CommandType.CLEAR:
                TodoList().clear_tasks()
                text = "All tasks cleared."
            case _:
                text = "Unknown command. Use /help to see available commands."
            
        return json.dumps(
                    {
                        "path": self.url.path,
                        "query_data": self.query_data,
                        "post_data": self.post_data.decode("utf-8"),
                        "form_data": self.form_data,
                        "cookies": {
                            name: cookie.value
                            for name, cookie in self.cookies.items()
                        },
                        "method": "sendMessage",
                        "text": text,
                        "chat_id": chat_id,
                    }
                )