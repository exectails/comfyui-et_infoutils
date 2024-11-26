class ETTextBoxNode:
    """
    A multi-line string primitive node.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "", "multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    CATEGORY = "exectails/Info"
    FUNCTION = "process"

    def process(self, text: str) -> tuple:
        return (text,)


class ETStringBoxNode:
    """
    A string primitive node. Useful for any type inputs where the official
    primitive nodes don't work as expected.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    CATEGORY = "exectails/Info"
    FUNCTION = "process"

    def process(self, value) -> tuple:
        return (value,)


class ETIntBoxNode:
    """
    An integer primitive node. Useful for any type inputs where the official
    primitive nodes don't work as expected.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("INT", {"default": 0}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("text",)

    CATEGORY = "exectails/Info"
    FUNCTION = "process"

    def process(self, value: int) -> tuple:
        return (value,)
