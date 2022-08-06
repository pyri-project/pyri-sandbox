
function load_blockly_blocks(blockly_blocks)
{
    blockly_blocks.forEach(b => {
        load_blockly_block(b);
    });
}

function load_blockly_block(b) {
    let block_json = {"name": "unknown"}
    try {
        //let block_json_text = b.blockly_json;
        //block_json = JSON.parse(block_json_text)
        let block_json = b.blockly_json
        Blockly.defineBlocksWithJsonArray([block_json])
    }
    catch (e) {
        e.message = "Error loading block definition \"" + block_json.name + "\": " + e.message;
        throw e;
    }

    try {
        
        if(b.sandbox_function_name || b.sandbox_function_name_selector)
        {
            Blockly.Python[b.name] = sandbox_function_pygen.bind(b);
        }
        else if (b.python_generator !== undefined && b.python_generator !== null)
        {
            // We need to include the js generator directly. This isn't a secure design,
            // but there isn't much that can be done otherwise
            let pygen_func = (function() {return eval(b.python_generator)})();
            if (pygen_func !== undefined && pygen_func !== null)
            {
                Blockly.Python[b.name] = pygen_func;
            }
        }
    }
    catch (e) {
        e.message = "Error loading block generator \"" + block_json.name + "\": " + e.message;
        throw e;
    }
}

function sandbox_function_pygen(block)
{
    let block_fields = {};
    this.blockly_json.args0.forEach(f => {
        block_fields[f.name] = f.type;
    })

    let sandbox_name = this.sandbox_function_name;
    if (!sandbox_name)
    {
        if(!this.sandbox_function_name_selector)
        {
            throw new Exception("No sandbox function specified for block " + this.name);
        }

        let blockly_selected_op = block.getFieldValue(this.sandbox_function_name_selector.selector_field);
        sandbox_name = this.sandbox_function_name_selector.sandbox_function_names[blockly_selected_op];
    }

    let python_args = [];

    this.sandbox_function_arguments.forEach(a => {
        if (block_fields[a.blockly_arg_name].startsWith("input"))
        {
            python_args.push(Blockly.Python.valueToCode(block, a.blockly_arg_name, Blockly.Python.ORDER_ATOMIC));
        }
        else
        {
            switch(a.arg_interpretation)
            {
                case "code":            
                    python_args.push(Blockly.Python.valueToCode(block, a.blockly_arg_name, Blockly.Python.ORDER_ATOMIC))
                    break;
                case "int":
                    python_args.push("int(" + block.getFieldValue(a.blockly_arg_name) + ")")
                    break
                case "float":
                    python_args.push("float(" + block.getFieldValue(a.blockly_arg_name) + ")")
                    break
                case "bool":
                    python_args.push("True" ? block.getFieldValue(a.blockly_arg_name).toUppercase() == "TRUE" : "False")
                    break
                default:
                    python_args.push("\"" + block.getFieldValue(a.blockly_arg_name) + "\"")
                    break;
            }
            
        }
    })
    
    let code = sandbox_name + "(" + python_args.join(", ") + ")";

    if (this.blockly_json.output === undefined)
    {
        return code + "\n";
    }
    else
    {
        return  [code, Blockly.Python.ORDER_NONE];
    }
}

blockly_finish = function (code) {
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


if(typeof exports === 'undefined'){
    var exports = this['blockly_compile_util'] = {};
 }

 exports.load_blockly_blocks = load_blockly_blocks;
 exports.load_blockly_block = load_blockly_block;
 exports.blockly_finish = blockly_finish;
