#!/usr/bin/env python

import sys
import os
import subprocess
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--shell-path", required=True, help="the path to the JS shell")
parser.add_argument("--shared", help="use shared memory", action="store_true")
parser.add_argument("--json", help="format results with json instead of csv", action="store_true")
parser.add_argument("--full", help="run with more sizes")
parser.add_argument("--iterations", help="iterations to run per test", type=int)

args = parser.parse_args()

args.shell_path = os.path.expanduser(args.shell_path)

sizes_pow2 = [1, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
sizes_mids = [2, 3, 6, 7, 12, 13, 24, 25, 48, 49, 96, 97, 192, 193, 384, 385, 768, 769, 1536, 1537]
sizes = sizes_pow2
if args.full:
  sizes += sizes_midss

iterations = 10000000
if args.iterations is not None:
  iterations = int(args.iterations)

support = open('support.wat').read()

def make_wat():
  wat = '(module '
  if args.shared:
    wat += '(memory 1 1 shared) '
  else:
    wat += '(memory 1 1) '  
  wat += support
  for size in sizes:
    wat += '''
  (func (export "bulk_memcpy_down_{size}")
    (memory.copy (i32.const 0x2000) (i32.const 0x3000) (i32.const {size}))
    (memory.copy (i32.const 0x3000) (i32.const 0x4000) (i32.const {size}))
    (memory.copy (i32.const 0x4000) (i32.const 0x5000) (i32.const {size}))
    (memory.copy (i32.const 0x5000) (i32.const 0x6000) (i32.const {size}))
    (memory.copy (i32.const 0x6000) (i32.const 0x7000) (i32.const {size}))
    (memory.copy (i32.const 0x7000) (i32.const 0x8000) (i32.const {size}))
    (memory.copy (i32.const 0x8000) (i32.const 0x9000) (i32.const {size}))
    (memory.copy (i32.const 0x9000) (i32.const 0xA000) (i32.const {size}))
    (memory.copy (i32.const 0xA000) (i32.const 0xB000) (i32.const {size}))
  )
  (func (export "bulk_memcpy_up_{size}")
    (memory.copy (i32.const 0x3000) (i32.const 0x2000) (i32.const {size}))
    (memory.copy (i32.const 0x4000) (i32.const 0x3000) (i32.const {size}))
    (memory.copy (i32.const 0x5000) (i32.const 0x4000) (i32.const {size}))
    (memory.copy (i32.const 0x6000) (i32.const 0x5000) (i32.const {size}))
    (memory.copy (i32.const 0x7000) (i32.const 0x6000) (i32.const {size}))
    (memory.copy (i32.const 0x8000) (i32.const 0x7000) (i32.const {size}))
    (memory.copy (i32.const 0x9000) (i32.const 0x8000) (i32.const {size}))
    (memory.copy (i32.const 0xA000) (i32.const 0x9000) (i32.const {size}))
    (memory.copy (i32.const 0xB000) (i32.const 0xA000) (i32.const {size}))
  )
  (func (export "bulk_memcpy_mixed_{size}")
    (memory.copy (i32.const 0x2000) (i32.const 0x9000) (i32.const {size}))
    (memory.copy (i32.const 0x3000) (i32.const 0x8000) (i32.const {size}))
    (memory.copy (i32.const 0x4000) (i32.const 0x7000) (i32.const {size}))
    (memory.copy (i32.const 0x5000) (i32.const 0x6000) (i32.const {size}))
    (memory.copy (i32.const 0x6000) (i32.const 0x5000) (i32.const {size}))
    (memory.copy (i32.const 0x7000) (i32.const 0x4000) (i32.const {size}))
    (memory.copy (i32.const 0x8000) (i32.const 0x3000) (i32.const {size}))
    (memory.copy (i32.const 0x9000) (i32.const 0x2000) (i32.const {size}))
    (memory.copy (i32.const 0xA000) (i32.const 0x1000) (i32.const {size}))
  )
  (func (export "bulk_memset_{size}")
    (memory.fill (i32.const 0x2000) (i32.const 0x99) (i32.const {size}))
    (memory.fill (i32.const 0x3000) (i32.const 0x88) (i32.const {size}))
    (memory.fill (i32.const 0x4000) (i32.const 0x77) (i32.const {size}))
    (memory.fill (i32.const 0x5000) (i32.const 0x66) (i32.const {size}))
    (memory.fill (i32.const 0x6000) (i32.const 0x55) (i32.const {size}))
    (memory.fill (i32.const 0x7000) (i32.const 0x44) (i32.const {size}))
    (memory.fill (i32.const 0x8000) (i32.const 0x33) (i32.const {size}))
    (memory.fill (i32.const 0x9000) (i32.const 0x22) (i32.const {size}))
    (memory.fill (i32.const 0xA000) (i32.const 0x11) (i32.const {size}))
  )
  (func (export "plain_memcopy_down_{size}")
    (call $memcpy (i32.const 0x2000) (i32.const 0x3000) (i32.const {size}))
    (call $memcpy (i32.const 0x3000) (i32.const 0x4000) (i32.const {size}))
    (call $memcpy (i32.const 0x4000) (i32.const 0x5000) (i32.const {size}))
    (call $memcpy (i32.const 0x5000) (i32.const 0x6000) (i32.const {size}))
    (call $memcpy (i32.const 0x6000) (i32.const 0x7000) (i32.const {size}))
    (call $memcpy (i32.const 0x7000) (i32.const 0x8000) (i32.const {size}))
    (call $memcpy (i32.const 0x8000) (i32.const 0x9000) (i32.const {size}))
    (call $memcpy (i32.const 0x9000) (i32.const 0xA000) (i32.const {size}))
    (call $memcpy (i32.const 0xA000) (i32.const 0xB000) (i32.const {size}))
  )
  (func (export "plain_memcopy_up_{size}")
    (call $memcpy (i32.const 0x3000) (i32.const 0x2000) (i32.const {size}))
    (call $memcpy (i32.const 0x4000) (i32.const 0x3000) (i32.const {size}))
    (call $memcpy (i32.const 0x5000) (i32.const 0x4000) (i32.const {size}))
    (call $memcpy (i32.const 0x6000) (i32.const 0x5000) (i32.const {size}))
    (call $memcpy (i32.const 0x7000) (i32.const 0x6000) (i32.const {size}))
    (call $memcpy (i32.const 0x8000) (i32.const 0x7000) (i32.const {size}))
    (call $memcpy (i32.const 0x9000) (i32.const 0x8000) (i32.const {size}))
    (call $memcpy (i32.const 0xA000) (i32.const 0x9000) (i32.const {size}))
    (call $memcpy (i32.const 0xB000) (i32.const 0xA000) (i32.const {size}))
  )
  (func (export "plain_memcopy_mixed_{size}")
    (call $memcpy (i32.const 0x2000) (i32.const 0x9000) (i32.const {size}))
    (call $memcpy (i32.const 0x3000) (i32.const 0x8000) (i32.const {size}))
    (call $memcpy (i32.const 0x4000) (i32.const 0x7000) (i32.const {size}))
    (call $memcpy (i32.const 0x5000) (i32.const 0x6000) (i32.const {size}))
    (call $memcpy (i32.const 0x6000) (i32.const 0x5000) (i32.const {size}))
    (call $memcpy (i32.const 0x7000) (i32.const 0x4000) (i32.const {size}))
    (call $memcpy (i32.const 0x8000) (i32.const 0x3000) (i32.const {size}))
    (call $memcpy (i32.const 0x9000) (i32.const 0x2000) (i32.const {size}))
    (call $memcpy (i32.const 0xA000) (i32.const 0x1000) (i32.const {size}))
  )
  (func (export "plain_memset_{size}")
    (call $memset (i32.const 0x2000) (i32.const 0x99) (i32.const {size}))
    (call $memset (i32.const 0x3000) (i32.const 0x88) (i32.const {size}))
    (call $memset (i32.const 0x4000) (i32.const 0x77) (i32.const {size}))
    (call $memset (i32.const 0x5000) (i32.const 0x66) (i32.const {size}))
    (call $memset (i32.const 0x6000) (i32.const 0x55) (i32.const {size}))
    (call $memset (i32.const 0x7000) (i32.const 0x44) (i32.const {size}))
    (call $memset (i32.const 0x8000) (i32.const 0x33) (i32.const {size}))
    (call $memset (i32.const 0x9000) (i32.const 0x22) (i32.const {size}))
    (call $memset (i32.const 0xA000) (i32.const 0x11) (i32.const {size}))
  )
'''.format(size=size)

    # plain wasm loads and stores to emulate a copy
    wat += ('''
  (func (export "plain_loadstores_{size}")''').format(size=size)
    for (src, dest) in zip([0x3000, 0x5000, 0x5000, 0x6000, 0x7000, 0x8000, 0x9000, 0xA000, 0xB000],
                           [0x2000, 0x3000, 0x4000, 0x5000, 0x6000, 0x7000, 0x8000, 0x9000, 0xA000]):
      wat += ('''
    (; memory.copy (i32.const 0x{dest:x}) (i322.const 0x{src:x}) ;)'''
        ).format(src=src, dest=dest)

      for offset in range(0, size):
        wat += ('''
    (i32.store8 (i32.const 0x{j:x}) (i32.load8_u (i32.const 0x{i:x})))'''
          ).format(i=src + offset, j=dest + offset)

    wat += '''
  )
'''

    # plain wasm stores to emulate a fill
    wat += '''
 (func (export "plain_stores_{size}")
'''.format(size=size)
    for (value, dest) in zip([0x99, 0x88, 0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11],
                             [0x2000, 0x3000, 0x4000, 0x5000, 0x6000, 0x7000, 0x8000, 0x9000, 0xA000]):
      wat += ('''
  (; memory.fill (i32.const 0x{dest:x}) (i322.const 0x{value:x}) ;)'''
        ).format(dest=dest, value=value)
      for offset in range(0, size):
        i = dest + offset
        wat += ('''
  (i32.store8 (i32.const 0x{i:x}) (i32.const 0x{value:x}))'''
          ).format(i=i, value=value)
    wat += '''
 )
'''
  wat += '''
)
'''
  return wat

def make_script():
  parameters = '''
const iterations = {iterations};
const json = {json};
const sizes = {sizes};
const tests = ['bulk_memcpy_down',
               'bulk_memcpy_up',
               'bulk_memcpy_mixed',
               'bulk_memset',
               'plain_memcopy_down',
               'plain_memcopy_up',
               'plain_memcopy_mixed',
               'plain_memset',
               'plain_loadstores',
               'plain_stores'];
'''.format(json=('true' if args.json else 'false'), sizes=sizes, iterations=iterations)

  code = '''
let bin = read('tmp/bench.wasm', 'binary');
let instance = new WebAssembly.Instance(new WebAssembly.Module(bin));

let results = {};

for (let name of tests) {
  results[name] = {};

  for (let size of sizes) {
    let test = instance.exports[`${name}_${size}`];

    let start = performance.now();
    for (let i = 0; i < iterations; i++) {
        test();
    }
    let end = performance.now();
    let delta = end - start;

    print(`${name}(${size}) = ${delta}`);
    results[name][size] = delta;
  }
}

if (json) {
  print(JSON.stringify(results));
} else {
  print('size,' + tests.join(','));
  for (let size of sizes) {
    print(`${size},` + Object.values(results).map((x) => x[size]).join(','));
  }
}

quit();
'''
  return parameters + code

# Build

if not os.path.exists('tmp'):
  os.mkdir('tmp')
open('tmp/script.js', 'w').write(make_script())
open('tmp/bench.wat', 'w').write(make_wat())

subprocess.call(['wat2wasm',
                 '--enable-threads',
                 '--enable-bulk-memory',
                 'tmp/bench.wat',
                 '-o',
                 'tmp/bench.wasm'])

# Run

subprocess.call([args.shell_path,
                 '-i',
                 'tmp/script.js'])
