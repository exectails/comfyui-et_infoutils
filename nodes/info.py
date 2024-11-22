from typing import Any
from server import PromptServer


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


anyType = AnyType("*")

def updateTextWidget(node, widget, text):
    """
    Raises an event to update a widget's text.
    """
    # It's my understanding this is supposed to work via the "ui" return
    # value, but that appears to no longer be the case in the latest
    # version of ComfyUI.
    PromptServer.instance.send_sync("exectails.text_updater.node_processed", {"node": node, "widget": widget, "text": text})


class ETTokenCountNode:
    """
    A node that counts the number of tokens in a given text. Passes the
    text through and returns the token count.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "clip": ("CLIP",),
                "tokens": ("STRING", {"default": "", "multiline": False}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("text", "count")
    OUTPUT_NODE = True

    CATEGORY = "exectails"
    FUNCTION = "process"

    def process(self, text: str, clip: Any, tokens: str, unique_id: str):
        tokens = clip.tokenize(text)
        tokenCount = 0

        if 'g' in tokens and len(tokens['g']) > 0:
            real_tokens = [token for token in tokens['g'][0] if token[0] != 0]
            tokenCount = len(real_tokens)

        tokenCountStr = str(tokenCount)

        updateTextWidget(unique_id, "tokens", tokenCountStr)
        return {"ui": {"tokens": tokenCountStr}, "result": (text, tokenCountStr,)}


class ETShowDataNode:
    """
    A node that takes any value and displays it as a string.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input": (anyType, {"forceInput": True}),
                "data": ("STRING", {"default": "", "multiline": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ()
    INPUT_IS_LIST = (True,)
    OUTPUT_NODE = True

    CATEGORY = "exectails"
    FUNCTION = "process"

    def process(self, input, data, unique_id):
        displayText = self.render(input)

        updateTextWidget(unique_id, "data", displayText)
        return {"ui": {"data": displayText}}

    def render(self, input):
        if not isinstance(input, list):
            return str(input)

        listLen = len(input)

        if listLen == 0:
            return ""

        if listLen == 1:
            return str(input[0])

        result = "List:\n"

        for i, element in enumerate(input):
            result += f"- {str(input[i])}\n"

        return result


class ETInspectTextNode:
    """
    A node that takes any value, displays it as a string, and passes
    through on as output.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "display": ("STRING", {"default": "", "multiline": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    INPUT_IS_LIST = (True,)
    OUTPUT_IS_LIST = (True,)
    OUTPUT_NODE = True

    CATEGORY = "exectails"
    FUNCTION = "process"

    def process(self, text, display, unique_id):
        displayText = self.render(text)

        updateTextWidget(unique_id, "display", displayText)
        return {"ui": {"display": displayText}, "result": (text,)}

    def render(self, input):
        if not isinstance(input, list):
            return input

        listLen = len(input)

        if listLen == 0:
            return ""

        if listLen == 1:
            return input[0]

        result = "List:\n"

        for i, element in enumerate(input):
            result += f"- {input[i]}\n"

        return result
