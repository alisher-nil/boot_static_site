class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        html_props = []
        for prop_name, prop_value in self.props.items():
            html_props.append(f' {prop_name}="{prop_value}"')
        return "".join(html_props)

    def __repr__(self) -> str:
        return (
            f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
        )
