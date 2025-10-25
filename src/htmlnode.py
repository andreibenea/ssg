class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        if self.props:
            for prop in self.props:
                result += f' {prop}="{self.props[prop]}"'
        return f"{result}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, children = None, props=None):
        super().__init__(tag, value, children, props)
        self.children = None

    def to_html(self):
        if self.value == None:
            raise ValueError("all leafs must have value")
        if self.tag == None:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, value=None, props=None):
        super().__init__(tag, value, children, props)
        self.value = None
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("all parents must have tags")
        if self.children == None:
            raise ValueError("all parents must have children")
        else:
            result = f"<{self.tag}>"
            for child in self.children:
                result += child.to_html()
            result += f"</{self.tag}>"
            return result