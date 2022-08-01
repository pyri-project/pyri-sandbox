from pyri.sandbox import blockly_compiler
import io

def test_blockly_compiler_simple():
    hello_world_blockly_xml = """<xml xmlns="https://developers.google.com/blockly/xml">
                        <block type="procedures_defnoreturn" id="ig-@O/ylKy_@*tL~m@X|" x="138" y="88">
                            <field name="NAME">hello_world_blockly</field>
                            <comment pinned="false" h="80" w="160">Describe this function...</comment>
                            <statement name="STACK">
                            <block type="text_print" id="leNnyydaklEu0$|E4fU~">
                                <value name="TEXT">
                                <shadow type="text" id="wWggJq|t$BAzKbOf`dtu">
                                    <field name="TEXT">Hello World from Blockly!</field>
                                </shadow>
                                </value>
                            </block>
                            </statement>
                        </block>
                        </xml>"""
    expected_pysrc = "# Describe this function...\ndef hello_world_blockly():\n  print('Hello World from Blockly!')\n"

    xml_io = io.StringIO(hello_world_blockly_xml)
    output_io = io.StringIO()

    blockly_compiler.compile_blockly_file(xml_io, output_io)
    output_io.seek(0)
    pysrc_str = output_io.read()
    print(pysrc_str)
    assert pysrc_str == expected_pysrc

