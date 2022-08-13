from pyri.plugins.blockly import get_all_blockly_blocks, get_all_blockly_categories, blockly_block_to_json
import json
import importlib_resources
import typedload

def get_toolbox_json(blocks):
    blocks_by_category=dict()

    for b in blocks.values():
        if b.category not in blocks_by_category:
            blocks_by_category[b.category] = [b]
        else:
            blocks_by_category[b.category].append(b)

    toolbox_json_text = importlib_resources.files("pyri.webui_server").joinpath('blockly_standard_toolbox.json').read_text()
    toolbox_json = json.loads(toolbox_json_text)

    cat = get_all_blockly_categories()
    for c in cat.values():
        c_json = c.blockly_json
        if isinstance(c_json,str):
            c_json = json.loads(c_json)
        c_name = c_json["name"]
        if c_name in blocks_by_category:
            contents = []
            for b in blocks_by_category[c_name]:
                contents.append(
                    {
                        "kind": "block",
                        "type": b.name
                    }
                )
            c_json["contents"] = contents
        toolbox_json["contents"].append(c_json)
    return json.dumps(toolbox_json, indent=4)


def main():
    blockly_blocks = get_all_blockly_blocks()
    blockly_blocks_json = []
    for b in blockly_blocks.values():
        blockly_blocks_json.append(blockly_block_to_json(b))

    with open("blockly_blocks.js", "w") as f:
        f.write("PYRI_BLOCKLY_BLOCKS=" + json.dumps(blockly_blocks_json,indent=4))

    with open("blockly_toolbox.js", "w") as f:
        f.write("BLOCKLY_TOOLBOX=" + get_toolbox_json(blockly_blocks))

    


if __name__ == "__main__":
    main()