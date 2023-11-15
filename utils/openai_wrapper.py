import time
import os

from openai import OpenAI

asstID = "asst_kreOeRbzGR1IFd4Yule0uiZq"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def create_ass_thread():
    thread = client.beta.threads.create(timeout=300)
    return thread.id


def ass_message(thread_id, content):
    message = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=content, timeout=300)

    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=asstID, instructions="", timeout=300)

    while True:
        # 查询消息的状态
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id, timeout=300)
        # 如果状态完成，则获取结果，break
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            result = messages.data[0].content[0].text.value
            break
        # 继续请求
        time.sleep(0.1)

    return result


def delete_ass_thread(thread_id):
    response = client.beta.threads.delete(thread_id, timeout=300)


if __name__ == "__main__":
    thread_id = create_ass_thread()
    print(ass_message(thread_id, "我要变漂亮需要怎么做？"))
    print(ass_message(thread_id, "怎么画眉毛？"))
    print(ass_message(thread_id, "怎么画口红？"))
    delete_ass_thread(thread_id)
