from pyri.sandbox import blockly_compiler
import io

def test_blockly_compiler_simple():
    hello_world_blockly_json = \
"""
{
  "blocks": {
    "languageVersion": 0,
    "blocks": [
      {
        "type": "procedures_defnoreturn",
        "id": "ig-@O/ylKy_@*tL~m@X|",
        "x": 138,
        "y": 88,
        "icons": {
          "comment": {
            "text": "Describe this function...",
            "pinned": false,
            "height": 80,
            "width": 160
          }
        },
        "fields": {
          "NAME": "hello_world_blockly"
        },
        "inputs": {
          "STACK": {
            "block": {
              "type": "text_print",
              "id": "leNnyydaklEu0$|E4fU~",
              "inputs": {
                "TEXT": {
                  "shadow": {
                    "type": "text",
                    "id": "wWggJq|t$BAzKbOf`dtu",
                    "fields": {
                      "TEXT": "Hello World from Blockly!"
                    }
                  }
                }
              }
            }
          }
        }
      }
    ]
  }
}
"""
    expected_pysrc = "# Describe this function...\ndef hello_world_blockly():\n  print('Hello World from Blockly!')\n"

    json_io = io.StringIO(hello_world_blockly_json)
    output_io = io.StringIO()

    blockly_compiler.compile_blockly_file(json_io, output_io)
    output_io.seek(0)
    pysrc_str = output_io.read()
    print(pysrc_str)
    assert pysrc_str == expected_pysrc

