import time
import os

from openai import OpenAI

asstID = "asst_kreOeRbzGR1IFd4Yule0uiZq"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
model = "gpt-4-vision-preview"


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


def create_ass_run_message(thread_id, content):
    message = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=content, timeout=300)
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=asstID, instructions="", timeout=300)
    return thread_id, run.id


def get_run_status(thread_id, run_id):
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id, timeout=300)
    # run.status:
    # queued, in_progress, requires_action, cancelling, cancelled, failed, completed, or expired
    if run.status == "completed":
        # limit: A limit on the number of objects to be returned.
        # Limit can range between 1 and 100, and the default is 20
        messages = client.beta.threads.messages.list(thread_id=thread_id, limit=1)
        result = messages.data[0].content[0].text.value
        return {"thread_id": thread_id, "run_id": run_id, "result": result, "status": "completed"}
    elif run.status in ["queued", "in_progress", "requires_action"]:
        return {"thread_id": thread_id, "run_id": run_id, "result": None, "status": "pending"}
    else:
        return {"thread_id": thread_id, "run_id": run_id, "result": None, "status": "failed"}


def delete_ass_thread(thread_id):
    response = client.beta.threads.delete(thread_id, timeout=300)


def ass_get_vision(message):
    """
    url:
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What’s in this image?"},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
          },
        },
      ],
    }
    base64:
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
    :param message:
    :return:
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            message
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(time.localtime())
    message = {
        "role": "user",
        "content": [
            {"type": "text", "text": "图片里面有什么?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "",
                },
            },
        ],
    }
    ret = ass_get_vision(message)
    print(ret)
    print(time.localtime())
