import io
from . import blockly_compiler

def run_blockly_compile_test(blockly_json, expected_pysrc):
    json_io = io.StringIO(blockly_json)
    output_io = io.StringIO()

    blockly_compiler.compile_blockly_file(json_io, output_io)
    output_io.seek(0)
    pysrc_str = output_io.read()
    print(pysrc_str)
    assert pysrc_str == expected_pysrc