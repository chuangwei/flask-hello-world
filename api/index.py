from flask import Flask, jsonify
from flask import request

from utils.openai_wrapper import create_ass_thread, ass_message, delete_ass_thread

app = Flask(__name__)


def return_result(code='0', msg='success', show_type=0, data=None, **kwargs):
    success = True
    if not data:
        data = {}
    if code != '0':
        show_type = 2
        success = False
    res = {"code": code, "msg": msg, "data": data, "success": success, "showType": show_type, **kwargs}
    # res = dict(code=code, msg=msg, data=data, success=success, showType=show_type, **kwargs)
    return jsonify(res)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/about')
def about():
    return 'About'


@app.route('/get_thread', methods=['GET'])
def create_thread():
    if request.method != "GET":
        return 'ERROR'
    thread_id = create_ass_thread()
    return return_result(data={"thread_id": thread_id})


@app.route('/ass_message', methods=['POST'])
def get_ass_message():
    if request.method != "POST":
        return 'ERROR'
    thread_id = request.json.get("thread_id")
    content = request.json.get("content")
    result = ass_message(thread_id=thread_id, content=content)
    return return_result(data={"result": result})


@app.route('/delete_thread', methods=['DELETE'])
def create_thread():
    thread_id = request.values.get("thread_id")
    delete_ass_thread(thread_id)
    return return_result()
