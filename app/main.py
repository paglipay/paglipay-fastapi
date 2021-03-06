from fastapi import FastAPI
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware
import random
import DTree
import json
import uuid
import threading
from .schemas import PostSsh
# models.Base.metadata.create_all(bind=engine)

flask_process_data = {}
flask_process = {}
import_obj_instance_hash = {}

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(post.router)
# app.include_router(user.router)
# app.include_router(auth.router)
# app.include_router(vote.router)


@app.get("/")
def root():
    lucky_num = random.randint(1, 1000)
    return {"message": f"Hello World pushing out to ubuntu. Your lucky number for today is {lucky_num}"}


@app.post('/ssh_check/{hash}')
def ssh_check(hash, postData: PostSsh):
    d = {}
    name = hash
    data = {
        "./json/paramiko/ubuntu/open/form_dic.json": [
            {
                "username": [
                    postData.username
                ],
                "password": [
                    postData.password
                ],
                "ip": [
                    postData.ip
                ],
                "send_cmd": [
                    postData.send_cmd
                ]
            }
        ],
        "jobs": [
            {
                "import": "Key"
            },
            {
                "True": [
                    {
                        "import": "RequestsObj"
                    },
                    {
                        "open": {
                            "ip": "http://corp.paglipay.info:5003/start",
                            "extra_pass": [
                                "./json/paramiko/ubuntu/open/form_dic.json"
                            ],
                            "jobs": [
                                {
                                    "import": "Key"
                                },
                                {
                                    "True": [
                                        {
                                            "True": "./json/paramiko/ubuntu/open/_create_list.json"
                                        },
                                        {
                                            "True": "./json/paramiko/ubuntu/send_cmd/_create_list.json"
                                        },
                                        {
                                            "True": "./json/paramiko/ubuntu/send_cmd/do.json"
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "True": "end"
                    }
                ]
            }
        ]
    }
    print('data: ', data)
    if 'jobs' in data:
        name = data.pop('jobs')

    d = data
    
    if hash in flask_process_data:
        flask_process_data[hash].update(d)
        import_obj_instance = import_obj_instance_hash[hash]

    else:
        print('NEW HASH: ', hash)
        flask_process_data[hash] = d
        import_obj_instance_hash[hash] = {}
        import_obj_instance = import_obj_instance_hash[hash]

    d = flask_process_data[hash]

    # name = 'start.json'

    thread = threading.Thread(
        target=do_process, args=(d, name, import_obj_instance,))
    flask_process[hash] = thread
    thread.daemon = False
    thread.start()
    thread.join()

    return flask_process_data[hash]


@app.get('/show/{hash}')
def show(hash):
    return flask_process_data[hash]


@app.post('/start/{hash}')
def start(hash, data: dict = Body(...)):
    d = {}
    name = hash
    # data = request.get_json()
    print('data: ', data)
    if 'jobs' in data:
        name = data.pop('jobs')
    d = data
    if hash in flask_process_data:
        flask_process_data[hash].update(d)
        import_obj_instance = import_obj_instance_hash[hash]

    else:
        print('NEW HASH: ', hash)
        flask_process_data[hash] = d
        import_obj_instance_hash[hash] = {}
        import_obj_instance = import_obj_instance_hash[hash]

    d = flask_process_data[hash]

    # name = 'start.json'

    thread = threading.Thread(
        target=do_process, args=(d, name, import_obj_instance,))
    flask_process[hash] = thread
    thread.daemon = False
    thread.start()
    thread.join()
    return {"message": f"HI {hash}", "data": flask_process_data[hash]}


def do_process(flask_data, json_file, import_obj_instance):
    if '.json' in json_file:
        c = DTree.DTree(json.load(open(json_file)), name=json_file,
                        import_obj_instance=import_obj_instance, data=flask_data)
    else:
        c = DTree.DTree(json_file, name=uuid.uuid1(),
                        import_obj_instance=import_obj_instance, data=flask_data)

def thread_process(data):
    pass
