from enum import Enum
import re
from textnode import TextNode, TextType


class Delimiters(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    block_list = []
    blocks = str(markdown).split("\n\n")
    for block in blocks:
        if len(block.strip()) == 0:
            continue
        block_list.append(block.strip())
    print(f"COPYBLOCKLIST##############{block_list}")
    return block_list


def block_to_block_type(block):
    print(f"PARSING BLOCK: {block}")
    if len(block) == 0:
        return ""
    print(block[0])
    match str(block[0]):
        case "#":
            heading_counter = 1
            for i in range(1, 7):
                if block[i] == "#":
                    heading_counter += 1
                elif block[i] == " ":
                    return BlockType.HEADING
                else:
                    break
            return BlockType.PARAGRAPH
        case "`":
            code_start = str(block).find("```")
            code_end = str(block).rfind("```")
            if code_end > code_start:
                return BlockType.CODE
            return BlockType.PARAGRAPH
        case ">":
            return BlockType.QUOTE
        case "-":
            return BlockType.UNORDERED_LIST
        case "1":
            num_start = str(block).find("1. ")
            if num_start == 0:
                return BlockType.ORDERED_LIST
            return BlockType.PARAGRAPH
        case _:
            return BlockType.PARAGRAPH


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    split_bold = split_nodes_delimiter([node], Delimiters.BOLD.value, TextType.BOLD)
    split_italic = split_nodes_delimiter(
        split_bold, Delimiters.ITALIC.value, TextType.ITALIC
    )
    split_code = split_nodes_delimiter(
        split_italic, Delimiters.CODE.value, TextType.CODE
    )
    split_images = split_nodes_image(split_code)
    split_urls = split_nodes_link(split_images)
    print(f"final result:\n{split_urls}")
    return split_urls


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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        print(f"parsing node: {node}")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            print("Not a TXT node..adding as is")
            continue
        print(f"text to extract img from: {node.text}")
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        txt_to_process = node.text
        for image in images:
            if len(txt_to_process) == 0:
                break
            expression = f"![{image[0]}]({image[1]})"
            left, right = txt_to_process.split(expression, 1)
            print(f"left_split: {left}")
            print(f"right_split: {right}")
            if len(left) != 0:
                new_node = TextNode(left, TextType.TEXT)
                print(f"adding left as node: {new_node}")
                new_nodes.append(new_node)
            new_node = TextNode(image[0], TextType.IMAGE, image[1])
            new_nodes.append(new_node)
            print(f"adding image as node: {new_node}")
            txt_to_process = right
        if len(txt_to_process) != 0:
            new_node = TextNode(txt_to_process, TextType.TEXT)
            print(f"adding remainder: {txt_to_process}")
            new_nodes.append(new_node)
    print(f"resulting list:\n{new_nodes}")
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        print(f"parsing node: {node}")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            print("Not type text. Adding as is..")
            continue
        print(f"text to extract url from: {node.text}")
        urls = extract_markdown_links(node.text)
        if not urls:
            print(f"no urls found, adding as is..")
            new_nodes.append(node)
            continue
        txt_to_process = node.text
        for url in urls:
            if len(txt_to_process) == 0:
                break
            expression = f"[{url[0]}]({url[1]})"
            left, right = txt_to_process.split(expression, 1)
            print(f"left_split: {left}")
            print(f"right_split: {right}")
            if len(left) != 0:
                new_node = TextNode(left, TextType.TEXT)
                print(f"adding left as node: {new_node}")
                new_nodes.append(new_node)
            new_node = TextNode(url[0], TextType.LINK, url[1])
            new_nodes.append(new_node)
            print(f"adding link as node: {new_node}")
            txt_to_process = right
        if len(txt_to_process) != 0:
            new_node = TextNode(txt_to_process, TextType.TEXT)
            print(f"adding remainder: {txt_to_process}")
            new_nodes.append(new_node)
    print(f"resulting list:\n{new_nodes}")
    return new_nodes


def extract_markdown_images(input):
    expression = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(expression, input)
    print(f"extr imgs returns: ")
    return matches


def extract_markdown_links(input):
    expression = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(expression, input)
    print(f"extr urls returns: ")
    return matches
