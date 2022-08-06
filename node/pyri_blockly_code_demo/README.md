# PyRI Blockly Code Demo

The PyRI Blockly Code Demo as a modified version of the Blockly Code demo that is used to allow modifying blockly
diagrams and generating XML of the blocks, or compiling into target languages. This version of the code
demo will use the blocks defined in PyRI, and generate the Python that would be executed in the sandbox.

To use, first restore the npm packages:

    npm install

Next, build blockly_blocks.json and blockly_toolbox.json:

   python build_pyri_blockly_json.py

Now open index.html in Chrome or Firefox.