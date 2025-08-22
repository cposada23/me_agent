from tools.Text_extractor import TextExtractor
from tools.ChatAgent import ChatAgent
import gradio as gr

def main():
    # pusher.push_notification("test")
    pdf_text = TextExtractor.extract_from_pdf("resources/Resume.pdf")
    print(pdf_text)
    chat_agent = ChatAgent(pdf_text)
    gr.ChatInterface(chat_agent.chat, type="messages").launch()

if __name__ == "__main__":
    main()
