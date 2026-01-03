from .nodes import ProductPromptGeneratorSimple

NODE_CLASS_MAPPINGS = {
    "ProductPromptGeneratorSimple": ProductPromptGeneratorSimple
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ProductPromptGeneratorSimple": "ProductPromptGenerator(Simple)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
