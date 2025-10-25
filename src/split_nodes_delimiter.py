from enum import Enum
import re
from textnode import TextNode, TextType


class Delimiters(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    print(f"size of initial nodes array: {len(old_nodes)}")
    for node in old_nodes:
        print(f"checking out node: {node}")
        print(f"set delimiter: {delimiter}")
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("invalid markdown syntax")
        if node.text[0] == delimiter or node.text[0:1] == delimiter:
            special_flag = True
        else:
            special_flag = False
        if node.text_type != TextType.TEXT:
            print(f"node type not text..adding node as is")
            new_nodes.extend([node])
        else:
            print(f"node text to split: {node.text}")
            slices = node.text.split(delimiter)
            print(f"text slices: {slices}")
            for slice in slices:
                if special_flag:
                    new_node = TextNode(slice, text_type)
                    new_nodes.extend([new_node])
                    special_flag = not special_flag
                    print(f"added {new_node}")
                    print(f"special flag now: {special_flag}")
                elif not special_flag and slice != "":
                    new_node = TextNode(slice, node.text_type)
                    new_nodes.extend([new_node])
                    special_flag = not special_flag
                    print(f"added {new_node}")
                    print(f"special flag now: {special_flag}")

    print(f"delimiter output:\n{new_nodes}")
    return new_nodes
