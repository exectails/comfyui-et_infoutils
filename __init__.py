from .nodes.input import ETTextBoxNode, ETStringBoxNode, ETIntBoxNode
from .nodes.info import ETTokenCountNode, ETShowDataNode, ETInspectTextNode

et_nodes = {
    ("Token Counter", ETTokenCountNode),
    ("Show Data", ETShowDataNode),
    ("Inspect Text", ETInspectTextNode),

    ("Text Box", ETTextBoxNode),
    ("String Box", ETStringBoxNode),
    ("Int Box", ETIntBoxNode),
}

NODE_CLASS_MAPPINGS = {cls.__name__: cls for display_name, cls in et_nodes}
NODE_DISPLAY_NAME_MAPPINGS = {cls.__name__: display_name for display_name, cls in et_nodes}

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
