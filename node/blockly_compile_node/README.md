# PyRI Sandbox Blockly Compiler Source

The node.js script `blockly_compile.js`  is used to compile Blockly programs into Python, since Blockly is a JavaScript 
application and can't be used directly in Python. The source script in this directory is combined into a single
file, installed into the Python directory using the command `npm install_blockly_compiler`. For development,
the `PYRI_SANDBOX_BLOCKLY_COMPILER_DIR` can be set to the directory containing `blockly_compile.js`.

The node program is designed to use the same format as Chrome "Native Messaging",
where json is communicated between Python and a Javascript subprocess using stdin/stdout with uint32 prefixed length
for each message.

Without arguments, the `blockly_compile.js` script will wait for stdin/stdout communication. The script can also read
an "args" file, containing the arg json file output by the compiler:

```
python -m pyri.sandbox.blockly_compiler --args args.json my_blockly_procedure.xml
node blockly_compile.js compile args.json
```

Where `my_blockly_procedure.xml` is a Blockly procedure in XML format.
