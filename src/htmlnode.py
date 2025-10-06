from typing import Sequence


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: Sequence["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_as_text = [f' {key}="{value}"' for key, value in self.props.items()]
        return "".join(props_as_text)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag, self.value, self.children, self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("a leaf node must have a value")
        if self.tag is None:
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: Sequence[HTMLNode],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("parent node must have a tag")
        if not self.children:
            raise ValueError("parent node must have children")
        children_content = [child.to_html() for child in self.children]
        props = self.props_to_html()
        result = f"<{self.tag}{props}>{''.join(children_content)}</{self.tag}>"
        return result
