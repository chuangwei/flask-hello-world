from flask import Flask, jsonify
from flask import request

from utils.openai_wrapper import create_ass_thread, create_ass_run_message, delete_ass_thread, get_run_status, \
    ass_get_vision

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


@app.route('/thread', methods=['GET', 'DELETE'])
def create_thread():
    if request.method == "GET":
        thread_id = create_ass_thread()
        return return_result(data={"thread_id": thread_id})
    elif request.method == "DELETE":
        thread_id = request.values.get("thread_id")
        delete_ass_thread(thread_id)
        return return_result()
    else:
        return return_result(code='3', msg="请求方式错误!", show_type=3)


@app.route('/message', methods=['POST'])
def get_ass_message():
    if request.method != "POST":
        return return_result(code='3', msg="请求方式错误!", show_type=3)
    thread_id = request.json.get("thread_id")
    content = request.json.get("content")
    thread_id, run_id = create_ass_run_message(thread_id=thread_id, content=content)
    return return_result(data={"thread_id": thread_id, "run_id": run_id})


@app.route('/message_status', methods=['GET'])
def delete_thread():
    if request.method != "GET":
        return return_result(code='3', msg="请求方式错误!", show_type=3)
    thread_id = request.values.get("thread_id")
    run_id = request.values.get("run_id")
    data = get_run_status(thread_id, run_id)
    return return_result(data=data)


@app.route('/vision', methods=['POST'])
def delete_thread():
    if request.method != "POST":
        return return_result(code='3', msg="请求方式错误!", show_type=3)
    message = request.json.get("message")
    data = ass_get_vision(message)
    return return_result(data=data)
