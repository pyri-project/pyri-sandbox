'use strict';

const nativeMessage = require('chrome-native-messaging');
const fs = require('fs');
let Blockly = require('blockly');

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

    const xmlText = args.blockly_xml_src;

    args.blockly_blocks.forEach(b => {
        let block_json = {"name": "unknown"}
        try {
            let block_json_text = b.blockly_json;
            block_json = JSON.parse(block_json_text)
            Blockly.defineBlocksWithJsonArray([block_json])
        }
        catch (e) {
            e.message = "Error loading block definition \"" + file + "\": " + e.message;
            throw e;
        }

        try {
            // We need to include the js generator directly. This isn't a secure design,
            // but there isn't much that can be done otherwise
            let block_gen_js_text = b.blockly_pygen;
            eval(block_gen_js_text)
        }
        catch (e) {
            e.message = "Error loading block generator \"" + block_json.name + "\": " + e.message;
            throw e;
        }

    });

    let xml = Blockly.Xml.textToDom(xmlText);

    let workspace = new Blockly.Workspace();
    Blockly.Xml.domToWorkspace(xml, workspace);
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

Blockly.Python.finish = function (code) {
    // Convert the definitions dictionary into a list.
    let imports = [];
    let definitions = [];
    for (let name in Blockly.Python.definitions_) {
        let def = Blockly.Python.definitions_[name];
        // TODO: Don't add top level variables. Find better way to handle this
        if (name === 'variables') {
            continue;
        }

        def = def.replace(/^\s*global\s+.*$/m, '');

        if (def.match(/^(from\s+\S+\s+)?import\s+\S+/)) {
            imports.push(def);
        } else {
            definitions.push(def);
        }
    }
    // Clean up temporary data.
    delete Blockly.Python.definitions_;
    delete Blockly.Python.functionNames_;
    Blockly.Python.variableDB_.reset();
    let allDefs = definitions.join('\n\n');
    return allDefs.replace(/\n\n+/g, '\n\n').replace(/\n*$/, '\n\n\n') + code;

};

const defaultBlocklyNames = Object.keys(Blockly.Blocks);
const defaultPythonNames = Object.keys(Blockly.Python);

if (process.argv.length > 2) {
    if (process.argv[2] != "compile") {
        error("Invalid command");
    }

    for (let i = 0; i < 100; i++) {
        let json_arg_rawdata = fs.readFileSync(process.argv[3]);
        let compile_arg = JSON.parse(json_arg_rawdata);
        let compile_res = compile_blockly(compile_arg);
        //console.log(JSON.stringify(compile_res));
        reset_blockly();
        console.log(compile_res);
    }
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

