import re
from enum import Enum
from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode, ParentNode, LeafNode
from src.convert_txt_to_html import text_node_to_html_node


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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    all_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            print(f"FOUND CODE TYPE")
            clean_block = block.replace("```", "")
            clean_block = clean_block.lstrip("\n")
            print(f"CLEAN BLOCK: {clean_block}")
            new_node = TextNode(clean_block, TextType.CODE)
            html_node = text_node_to_html_node(new_node)
            new_node = ParentNode("pre", [html_node])
            all_nodes.append(new_node)
        else:
            nodes_in_block = text_to_textnodes(block)
            child_nodes = []
            for node in nodes_in_block:
                print(f"node in block: {node}")
                html_node = text_node_to_html_node(node)
                child_nodes.append(html_node)
            print(f"children: {child_nodes}")
            match block_type:
                case BlockType.PARAGRAPH:
                    for child in child_nodes:
                        print(f"CHILD: {child}")
                        if getattr(child, "tag", None) is None and isinstance(
                            child.value, str
                        ):
                            child.value = child.value.replace("\n", " ")
                    new_node = ParentNode("p", child_nodes)
                    print(f"RETURNING HTMLNODE: {new_node}")
                    print(f"TOHTML{new_node.to_html()}")
                    all_nodes.append(new_node)
                case BlockType.HEADING:
                    print(f"FOUND HEADING TYPE")
                    print(f"heading block: {block}")
                    count = str(block).count("#", 0, 6)
                    print(f"heading level: {count}")
                    block = block[count:].lstrip()
                    print(f"heading block: {block}")
                    for child in child_nodes:
                        child.value = child.value[count:].lstrip()
                    new_node = ParentNode(f"h{count}", child_nodes)
                    print(f"RETURNING HTMLNODE: {new_node}")
                    print(f"TOHTML{new_node.to_html()}")
                    all_nodes.append(new_node)
                case BlockType.QUOTE:
                    print("FOUND QUOTE TYPE")
                    lines = str(block).splitlines()
                    clean_lines = []
                    for line in lines:
                        line = line.strip()
                        if line.startswith(">"):
                            line = line[1:]
                            if line.startswith(" "):
                                line = line[1:]
                        if len(line) == 0:
                            continue
                        clean_lines.append(line)
                    print(f"CLEAN LINES: {clean_lines}")
                    joined_nodes = " ".join(clean_lines)
                    print(f"JOINED NODES: {joined_nodes}")
                    quote_children = [text_node_to_html_node(node) for node in text_to_textnodes(joined_nodes)]
                    # p_node = ParentNode("p", quote_children)
                    new_node = ParentNode("blockquote", quote_children)
                    all_nodes.append(new_node)
                case BlockType.ORDERED_LIST:
                    print("FOUND ORDERED LIST TYPE")
                    lines = str(block).splitlines()
                    child_nodes = []
                    for i in range(len(lines)):
                        prefix = f"{i + 1}. "
                        if len(lines[i]) == 0:
                            continue
                        if lines[i].startswith(prefix):
                            line_text = lines[i][len(prefix):].strip()
                            line_children = [text_node_to_html_node(n) for n in text_to_textnodes(line_text)]
                            child_nodes.append(ParentNode("li", line_children))
                    new_node = ParentNode("ol", child_nodes)
                    all_nodes.append(new_node)

                case BlockType.UNORDERED_LIST:
                    print("FOUND UNORDERED LIST TYPE")
                    print(f"UL block: {block}")
                    lines = str(block).splitlines()
                    print(f"UL LINES: {lines}")
                    child_nodes = []
                    for line in lines:
                        if len(line) == 0:
                            continue
                        if str(line).startswith("- "):
                            line_txt = line[2:].strip()
                            line_children = [
                                text_node_to_html_node(n)
                                for n in text_to_textnodes(line_txt)
                            ]
                            child_nodes.append(ParentNode("li", line_children))
                    new_node = ParentNode("ul", child_nodes)
                    all_nodes.append(new_node)

    div_node = ParentNode("div", all_nodes)
    print(f"#################FINAL DIV NODE: {div_node.to_html()}")
    return div_node


def markdown_to_blocks(markdown):
    block_list = []
    blocks = str(markdown).split("\n\n")
    for block in blocks:
        if len(block.strip()) == 0:
            continue
        block_list.append(block.strip())
    print(f"BLOCKLIST##############{block_list}")
    return block_list


def block_to_block_type(block):
    print(f"PARSING BLOCK:\n{block}")
    if len(block) == 0:
        return ""
    print(f"first char: {block[0]}")
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
            block = block.strip()
            lines = str(block).split("\n")
            print(lines)
            for line in lines:
                print(line)
                print(line.startswith("- "))
                if not line.startswith("- "):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        case "1":
            block = block.strip()
            lines = str(block).split("\n")
            for i in range(len(lines)):
                if not lines[i].startswith(f"{i+1}."):
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
        case _:
            print("ELSE CASE HIT")
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
    print(f"FINAL SPLIT:\n{split_urls}")
    return split_urls


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    print(f"size of initial nodes array: {len(old_nodes)}")
    for node in old_nodes:
        print(f"checking out node: {node}")
        print(f"set delimiter: {delimiter}")
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("invalid markdown syntax")
        # if len(node.text) > 1:
        #     if node.text[0] == delimiter or node.text[0:1] == delimiter:
        #         special_flag = True
        #     else:
        #         special_flag = False
        if node.text_type != TextType.TEXT:
            print(f"node type not text..adding node as is")
            new_nodes.extend([node])
        else:
            print(f"node text to split: {node.text}")
            slices = node.text.split(delimiter)
            print(f"text slices: {slices}")
            i = 0
            for slice in slices:
                if slice == "":
                    i += 1
                    continue
                if i % 2 != 0:
                # if special_flag:
                    new_node = TextNode(slice, text_type)
                    new_nodes.extend([new_node])
                    # special_flag = not special_flag
                    print(f"added {new_node}")
                    # print(f"special flag now: {special_flag}")
                elif i % 2 == 0:
                # elif not special_flag and slice != "":
                    new_node = TextNode(slice, node.text_type)
                    new_nodes.extend([new_node])
                    # special_flag = not special_flag
                    print(f"added {new_node}")
                    # print(f"special flag now: {special_flag}")
                i += 1

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
