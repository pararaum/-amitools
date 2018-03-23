from amitools.vamos.machine import MockMemory
from amitools.vamos.mem import MemoryCache


def mem_cache_rwx_write_test():
  mem = MemoryCache(0x100, 0x210)
  # build cache contents
  mem.w8(0x100, 42)
  assert mem.r8(0x100) == 42
  mem.w16(0x200, 0xdead)
  assert mem.r16(0x200) == 0xdead
  mem.w32(0x300, 0xcafebabe)
  assert mem.r32(0x300) == 0xcafebabe
  mem.write(0, 0x101, 43)
  assert mem.read(0, 0x101) == 43
  mem.write(1, 0x202, 0x1234)
  assert mem.read(1, 0x202) == 0x1234
  mem.write(2, 0x304, 0x11223344)
  assert mem.read(2, 0x304) == 0x11223344
  # write to main mem
  main_mem = MockMemory()
  mem.write_cache(main_mem)
  # check main mem
  assert main_mem.r8(0x100) == 42
  assert main_mem.r16(0x200) == 0xdead
  assert main_mem.r32(0x300) == 0xcafebabe
  assert main_mem.read(0, 0x101) == 43
  assert main_mem.read(1, 0x202) == 0x1234
  assert main_mem.read(2, 0x304) == 0x11223344


def mem_cache_rwx_read_test():
  mem = MockMemory()
  # build main mem contents
  mem.w8(0x100, 42)
  assert mem.r8(0x100) == 42
  mem.w16(0x200, 0xdead)
  assert mem.r16(0x200) == 0xdead
  mem.w32(0x300, 0xcafebabe)
  assert mem.r32(0x300) == 0xcafebabe
  mem.write(0, 0x101, 43)
  assert mem.read(0, 0x101) == 43
  mem.write(1, 0x202, 0x1234)
  assert mem.read(1, 0x202) == 0x1234
  mem.write(2, 0x304, 0x11223344)
  assert mem.read(2, 0x304) == 0x11223344
  # write to cache
  cmem = MemoryCache(0x100, 0x210)
  cmem.read_cache(mem)
  # check cache mem
  assert cmem.r8(0x100) == 42
  assert cmem.r16(0x200) == 0xdead
  assert cmem.r32(0x300) == 0xcafebabe
  assert cmem.read(0, 0x101) == 43
  assert cmem.read(1, 0x202) == 0x1234
  assert cmem.read(2, 0x304) == 0x11223344


def mem_cache_block_write_test():
  mem = MemoryCache(0x100, 0x220)
  data = "hello, world!"
  mem.w_block(0x100, data)
  assert mem.r_block(0x100, len(data)) == data
  bdata = bytearray(data)
  mem.w_block(0x180, bdata)
  assert mem.r_block(0x180, len(bdata)) == bdata
  mem.clear_block(0x200, 100, 42)
  assert mem.r_block(0x200, 100) == chr(42) * 100
  mem.copy_block(0x200, 0x300, 20)
  assert mem.r_block(0x300, 21) == chr(42) * 20 + chr(0)
  # write to main mem
  main_mem = MockMemory()
  mem.write_cache(main_mem)
  assert main_mem.r_block(0x100, len(data)) == data
  assert main_mem.r_block(0x180, len(bdata)) == bdata
  assert main_mem.r_block(0x200, 100) == chr(42) * 100
  assert main_mem.r_block(0x300, 21) == chr(42) * 20 + chr(0)


def mem_cache_block_read_test():
  mem = MockMemory()
  data = "hello, world!"
  mem.w_block(0x100, data)
  assert mem.r_block(0x100, len(data)) == data
  bdata = bytearray(data)
  mem.w_block(0x180, bdata)
  assert mem.r_block(0x180, len(bdata)) == bdata
  mem.clear_block(0x200, 100, 42)
  assert mem.r_block(0x200, 100) == chr(42) * 100
  mem.copy_block(0x200, 0x300, 20)
  assert mem.r_block(0x300, 21) == chr(42) * 20 + chr(0)
  # write to main mem
  cmem = MemoryCache(0x100, 0x220)
  cmem.read_cache(mem)
  assert cmem.r_block(0x100, len(data)) == data
  assert cmem.r_block(0x180, len(bdata)) == bdata
  assert cmem.r_block(0x200, 100) == chr(42) * 100
  assert cmem.r_block(0x300, 21) == chr(42) * 20 + chr(0)


def mem_cache_cstr_write_test():
  mem = MemoryCache(0x100, 0x100)
  data = "hello, world"
  mem.w_cstr(0x100, data)
  assert mem.r_cstr(0x100) == data
  empty = ""
  mem.w_cstr(0x120, empty)
  assert mem.r_cstr(0x120) == empty
  # to main
  main_mem = MockMemory()
  mem.write_cache(main_mem)
  assert main_mem.r_cstr(0x100) == data
  assert main_mem.r_cstr(0x120) == empty


def mem_cache_cstr_read_test():
  mem = MockMemory()
  data = "hello, world"
  mem.w_cstr(0x100, data)
  assert mem.r_cstr(0x100) == data
  empty = ""
  mem.w_cstr(0x120, empty)
  assert mem.r_cstr(0x120) == empty
  # to cache
  cmem = MemoryCache(0x100, 0x100)
  cmem.read_cache(mem)
  assert cmem.r_cstr(0x100) == data
  assert cmem.r_cstr(0x120) == empty


def mem_cache_bstr_write_test():
  mem = MemoryCache(0x100, 0x100)
  data = "hello, world"
  mem.w_bstr(0x100, data)
  assert mem.r_bstr(0x100) == data
  empty = ""
  mem.w_bstr(0x180, empty)
  assert mem.r_bstr(0x180) == empty
  # to main
  main_mem = MockMemory()
  mem.write_cache(main_mem)
  assert main_mem.r_bstr(0x100) == data
  assert main_mem.r_bstr(0x180) == empty


def mem_cache_bstr_read_test():
  mem = MockMemory()
  mem = MemoryCache(0x100, 0x100)
  data = "hello, world"
  mem.w_bstr(0x100, data)
  assert mem.r_bstr(0x100) == data
  empty = ""
  mem.w_bstr(0x180, empty)
  assert mem.r_bstr(0x180) == empty
  # to cache
  cmem = MemoryCache(0x100, 0x100)
  cmem.read_cache(mem)
  assert cmem.r_bstr(0x100) == data
  assert cmem.r_bstr(0x180) == empty