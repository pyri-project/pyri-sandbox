const http = require('http')
const {URL} = require('url')
const fs = require('fs');
const path = require('path');
var Blockly = require('node-blockly');
const { parse: parseQuery } = require('querystring');


function reset_blockly()
{
  Blockly = null;
  for (const property in require.cache)
    {
    if (property.includes("node-blockly"))
    {
        delete require.cache[property]
    }
    }

    Blockly = require('node-blockly');
}


function compile_blockly(working_dir)
{ 
    // Clear all data loaded into blockly by previous runs 
    reset_blockly()
    
    const xmlText = fs.readFileSync(path.join(working_dir,"blockly_src.xml"), 'utf8')
    
    var xml = Blockly.Xml.textToDom(xmlText);

    var workspace = new Blockly.Workspace();
    Blockly.Xml.domToWorkspace(xml, workspace);
    var code = Blockly.Python.workspaceToCode(workspace);

    
    fs.writeFileSync(path.join(working_dir,"blockly_src_compiled.py"), code)
    
}


function do_compile(command, arg)
{
    try
    {        
        if (command === "quit")
        {
            return "quit"
        }
        else if (command === "compile")
        {
            compile_blockly(arg)
            return "done"
        }
        else
        {
            return "invalid"            
        }
    }
    catch (e)
    {
        return "error;" + JSON.stringify(e)
    }
    
}

serverOrigin = 'http://localhost:57001'

const requestListener = function (req, res) {
    
    req.socket.setNoDelay(true);
    const url = new URL(req.url, serverOrigin);
    query = parseQuery(url.search.substr(1));
    res.writeHead(200, {'Content-Type': 'text/plain'});
    output = do_compile(query.command,query.arg)
    res.end(output + "\n")
    
    
  }
  
  const server = http.createServer(requestListener);
  listener = server.listen(0,'127.0.0.1',function()
  { 
    port = listener.address().port
    console.log("ready;" + port)
  });

