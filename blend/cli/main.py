from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.widgets import Input, Static
from textual.message import Message


class ChatMessage(Static):
    """Individual chat message widget"""

    def __init__(self, content: str, is_user: bool = True, **kwargs):
        self.content = content
        self.is_user = is_user

        if is_user:
            message_text = content  # User message content only, without label and time
            classes = "user-message"
        else:
            message_text = content  # AI message content only, without label and time
            classes = "ai-message"

        super().__init__(message_text, classes=classes, **kwargs)


class ChatContainer(ScrollableContainer):
    """Scrollable container for chat messages"""

    def add_message(self, content: str, is_user: bool = True):
        """Add new message"""
        message = ChatMessage(content, is_user)
        self.mount(message)
        """Scroll to bottom"""
        self.scroll_end(animate=False)


class MessageInput(Input):
    """Custom Input widget for message input"""

    class MessageSent(Message):
        """Event fired when message is sent"""

        def __init__(self, message: str):
            self.message = message
            super().__init__()

    def on_key(self, event):
        """Send message when Enter key is pressed"""
        if event.key == "enter" and self.value.strip():
            message = self.value.strip()
            self.value = ""
            self.post_message(self.MessageSent(message))


class BlendAIApp(App):
    """Main class for Blend AI chat application"""

    CSS = """
    Screen {
        background: $surface;
    }

    .input-container {
        height: auto;
        margin: 0 1;
        padding: 1;
        background: $panel;
        border: none;
    }

    .user-message {
        margin: 1 2;
        padding: 1;
        background: $primary 20%;
        border: none;
    }

    .ai-message {
        margin: 1 2;
        padding: 1;
        background: transparent;
        border: none;
        width: 90%;
    }

    MessageInput {
        width: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        with Container():
            yield ChatContainer(id="chat")

        with Horizontal(classes="input-container"):
            yield MessageInput(
                placeholder="Enter your message... (Press Enter to send)",
                id="message-input"
            )

    def on_mount(self):
        """Execute when app starts"""
        chat = self.query_one("#chat", ChatContainer)
        chat.add_message("Hello! Welcome to Blend AI. How can I help you today?", is_user=False)

    def on_message_input_message_sent(self, event: MessageInput.MessageSent):
        """Handle when message is sent from input widget"""
        self.send_message(event.message)

    def on_key(self, event):
        """Handle keyboard events"""
        if event.key == "ctrl+c":
            self.exit()

    def send_message(self, message: str):
        """Send user message and simulate AI response"""
        chat = self.query_one("#chat", ChatContainer)

        # Add user message
        chat.add_message(message, is_user=True)

        # Simulate AI response (replace with actual AI model call)
        ai_response = self.generate_ai_response(message)
        chat.add_message(ai_response, is_user=False)

        # Refocus input field
        message_input = self.query_one("#message-input", MessageInput)
        message_input.focus()

    def generate_ai_response(self, user_message: str) -> str:
        """Generate AI response (currently simulation, replace with actual AI model later)"""
        responses = {
            "hello": "Hello! Have a great day!",
            "help": "How can I help you? Feel free to ask me anything.",
            "weather": "Sorry, I can't provide weather information at the moment. Real-time data connection is needed.",
            "hi": "Hi! This is Blend AI. What do you need help with?",
        }

        # Simple keyword matching
        for keyword, response in responses.items():
            if keyword in user_message.lower():
                return response

        # Default response
        return f"You mentioned '{user_message}'. This is currently in basic response mode. More natural conversations will be possible once connected to an actual AI model!"


def main():
    """Run the application"""
    app = BlendAIApp()
    app.run()


if __name__ == "__main__":
    main()