'use strict';

const nativeMessage = require('chrome-native-messaging');
const fs = require('fs');
const Blockly = require('blockly');
const blockly_compile_util = require('./blockly_compile_util')

function reset_blockly() {
    let removeNamesBlockly = Object.keys(Blockly.Blocks).filter(x => !defaultBlocklyNames.includes(x));
    let removeNamesPython = Object.keys(Blockly.Python).filter(x => !defaultPythonNames.includes(x));

    removeNamesBlockly.forEach(n => {
        delete Blockly.Blocks[n];
    });

    removeNamesPython.forEach(n => {
        delete Blockly.Python[n];
    });
}


function compile_blockly(args) {
    // Clear all data loaded into blockly by previous runs 
    reset_blockly()

    blockly_compile_util.load_blockly_blocks.bind({"Blockly": Blockly})(args.blockly_blocks)

    let workspace = new Blockly.Workspace();
    Blockly.serialization.workspaces.load(args.blockly_json_src, workspace);
    let code = Blockly.Python.workspaceToCode(workspace);
    return code;
}


function do_compile(msg) {
    lastKeepalive = Date.now();
    try {        
        if (msg.command === "quit") {
            output({ "return": "quit" });
            process.exit(0);
        }
        else if (msg.command === "compile") {
            let pysrc = compile_blockly(msg.arg);
            output({ "return": "done", "py_src": pysrc })
        }
        else if (msg.command == "keepalive") {
            output({"return": "keepalive"});
        }
        else {
            output({ "return": "invalid" });
        }
    }
    catch (e) {
        output({ "return": "error", "error": e.toString(), "stack": e.stack.toString() })
    }

}

Blockly.Python.finish = blockly_compile_util.blockly_finish.bind({"Blockly": Blockly});

const defaultBlocklyNames = Object.keys(Blockly.Blocks);
const defaultPythonNames = Object.keys(Blockly.Python);

if (process.argv.length > 2) {
    if (process.argv[2] != "compile") {
        error("Invalid command");
    }

    
    let json_arg_rawdata = fs.readFileSync(process.argv[3]);
    let compile_arg = JSON.parse(json_arg_rawdata);
    let compile_res = compile_blockly(compile_arg);
    //console.log(JSON.stringify(compile_res));
    reset_blockly();
    console.log(compile_res);
    
    process.exit(0);
}

process.stdin
    .pipe(new nativeMessage.Input())
    .on('data', function (msg) {
        do_compile(msg)
    });

const output_s = new nativeMessage.Output();
output_s.pipe(process.stdout);

function output(msg) {
    output_s.write(msg);
}

console.log = console.error;

let lastKeepalive = Date.now();

function keepaliveTimer()
{
    let now = Date.now();
    if ((now - lastKeepalive) > 60000)
    {
        console.error("Blockly compiler exiting due to inactivity");
        process.exit(0);
    }
}

setInterval(keepaliveTimer,15000);

