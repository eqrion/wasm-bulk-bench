# bulk-memory-operations benchmark

See [bulk-memory-operations#111](https://github.com/WebAssembly/bulk-memory-operations/issues/111) for background.

## Use
```
./run.py --shell-path=JS_SHELL [--shared] [--full] [--iterations=ITERATIONS]
```

Requires the [wabt](https://github.com/WebAssembly/wabt) to be built and in $PATH.

Also requires a built version of a JS shell. Tested with V8's `d8`, and SM's `js`.
