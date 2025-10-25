from enum import Enum
import re
from textnode import TextNode, TextType


class Delimiters(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    print(f"old_nodes len: {len(old_nodes)}")
    for node in old_nodes:
        print(f"node: {node}")
        print(f"delimiter: {delimiter}")
        if node.text[0] == delimiter:
            special_flag = True
        else:
            special_flag = False
        if node.text_type != TextType.TEXT:
            print(f"type not text..adding node as is")
            new_nodes.extend([node])
        else:
            print(f"node text: {type(node.text)}")
            slices = node.text.split(delimiter)
            print(f"slices: {slices}")
            for slice in slices:
                if special_flag:
                    new_node = TextNode(slice, text_type)
                    new_nodes.extend([new_node])
                    special_flag = not special_flag
                    print(f"added {new_node}")
                else:
                    new_node = TextNode(slice, node.text_type)
                    new_nodes.extend([new_node])
                    special_flag = not special_flag
                    print(f"added {new_node}")

    print(f"output test result:\n{new_nodes}")
    return new_nodes
