from .nodes.input import ETTextBoxNode, ETStringBoxNode, ETIntBoxNode
from .nodes.info import ETTokenCountNode, ETShowDataNode, ETInspectTextNode

NODE_CLASS_MAPPINGS = {
    "ETTextBoxNode": ETTextBoxNode,
    "ETStringBoxNode": ETStringBoxNode,
    "ETIntBoxNode": ETIntBoxNode,

    "ETTokenCountNode": ETTokenCountNode,
    "ETShowDataNode": ETShowDataNode,
    "ETInspectTextNode": ETInspectTextNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ETTokenCountNode": "Token Counter",
    "ETShowDataNode": "Show Data",
    "ETInspectTextNode": "Inspect Text",

    "ETTextBoxNode": "Text Box",
    "ETStringBoxNode": "String Box",
    "ETIntBoxNode": "Int Box",
}

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
