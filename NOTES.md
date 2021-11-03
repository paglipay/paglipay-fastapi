{
    "my_packages/JinjaObj/json/ip.txt":"R1\nR2\nR123\nSQWE",
    "jobs": [
        {"import":"Key"},
        "my_packages/RequestsObj/RequestsObjTest.json"
    ]
}
{
    "./json/paramiko/ubuntu/open/form_dic.json": [
        {
            "username": [
                "vagrant"
            ],
            "password": [
                "vagrant"
            ],
            "ip": [
                "192.168.2.81"
            ],
            "send_cmd": [
                "ls -la"
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
                        "ip": "http://192.168.2.213:5000/start",
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