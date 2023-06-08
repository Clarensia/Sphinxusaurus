import os

from src.dataclasses.Project import Project
from src.dataclasses.main_class.MainClass import MainClass
from src.dataclasses.main_class.MainClassMethod import MainClassMethod
from src.utils import create_folder_name


class Writer:

    def __init__(self, dest_path: str):
        self._dest_path = dest_path
        self._verify_folder()

    def _verify_folder(self):
        if os.path.exists(self._dest_path):
            print(f"Destination path: {self._dest_path} exists, can't run the program")
            os.exit(1)

    def _create_folder_in_dest(self, folder: str):
        os.mkdir(os.path.join(self._dest_path, folder))

    def _create_dest_folder(self):
        os.mkdir(self._dest_path)
        self._create_folder_in_dest("models")
        self._create_folder_in_dest("exceptions")

    def _get_metadata(self, title: str, description: str, sidebar_class_name: str | None) -> str:
        """Create the metadata header for the given file

        :param title: The title of the file
        :type title: str
        :param description: The short description
        :type description: str
        :param sidebar_class_name: If we are in a description of th main file, we put the
                                   class name here. If not, then we create a normal header
        :type sidebar_class_name: str | None
        :return: The metadata that we wrote
        :rtype: str
        """
        ret = "---\n"
        ret += f"title: {title}\n"
        ret += f"description: {description}"
        if sidebar_class_name is not None:
            ret += "sidebar_position: 3\n"
            ret += f"sidebar_class_name: {sidebar_class_name}\n"
        ret += "---\n"
        
        return ret

    def _create_module_main_file(self, folder_name: str, class_name: str, short_description: str, long_description: str):
        to_write = self._get_metadata(class_name, short_description, f"sidebar-{folder_name}")
        to_write += "\n"

        to_write += long_description

        with open(os.path.join(self._dest_path, folder_name, f"{folder_name}.md"), "w+") as f:
            f.write(to_write)

    def _get_usage(self, method: MainClassMethod, main_class_name: str) -> str:
        """Get the usage of a method. Example return value:

        ```py
        import asyncio

        from blockchainapis import BlockchainAPIs

        async def print_amount_out():
            # Create the BlockchainAPIs instance
            # You can additionaly add an API key if needed
            blockchain_apis = BlockchainAPIs()
            # Get the amount of tokenOut that you will get after selling amountIn tokenIn
            amount_out = await blockchain_apis.amount_out(
                blockchain="ethereum", # The id of the blockchain on which this exchange take place
                tokenIn="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", # The address of the token that you sell
                tokenOut="0xdAC17F958D2ee523a2206206994597C13D831ec7", # The address of the token that you buy
                amountIn=1000000000000000000, # The amount of token0 that you sell
                exchange="uniswapv2" # The exchange on which you want to do the trade (optional)
            )
            print(amount_out)
            # We need to close our instance once we are done with BlockchainAPIs
            await blockchain_apis.close()

        asyncio.run(print_amount_out())
        ```

        :param method: The method that we have to use
        :type method: MainClassMethod
        :return: The usage string
        :rtype: str
        """
        instance_name = create_folder_name(main_class_name).replace("-", "_")
        ret = f'''```py
import asyncio

from {main_class_name} import {main_class_name}

async def print_{method.name}():
    # Create the {main_class_name} instance
    # You can additionaly add an API key if you want
    {instance_name} = {main_class_name}()
    # {method.short_description}
    {method.name} = await {instance_name}.{method.name}('''
        for param in method.parameters:
            example = f'"{param.example}"' if param.param_type == "str" else param.example
            ret += f"        {param.name}={example}\n"

        ret += f'''    )
    print({method.name})
    # We need to close our instance once we are done with BlockchainAPIs
    await {main_class_name}.close()

asyncio.run(print_{method.name}())
```
'''

        return ret

    def _write_method(self, folder_name: str, method: MainClassMethod):
        to_write = self._get_metadata(method.name, method.short_description)
        to_write += "\n"
        to_write += "import CodeBlock from '@theme/CodeBlock';\n\n"
        to_write += "```py\n"
        to_write += method.definition
        to_write += "```\n\n"
        to_write += method.long_description
        to_write += "\n\n## Parameters\n\n"
        for parameter in method.parameters:
            to_write += f" - [{parameter.name}](#{parameter.name}): {parameter.description}\n"
        to_write += "\n## Returns\n\n"
        to_write += '<CodeBlock language="python">\n'
        if "List" in method.return_type:
            list_object = method.return_type.replace("List[", "")
            list_object = method.return_type.replace("]", "")
            link_to_return_type = f'<a href="/docs/python-sdk/models/{list_object}">{list_object}</a>'
            to_write += f'    List[{link_to_return_type}]\n'
        else:
            to_write += f'    <a href="/docs/python-sdk/models/{method.return_type}">{method.return_type}</a>'
            to_write += "\n"

        to_write += '</CodeBlock>\n\n'

        to_write += method.return_description
        to_write += "\n\n"
        to_write += "## Example\n\n"
        to_write += "### Usage\n\n"
        to_write += self._get_usage(method)
        to_write += "\n"
        to_write += "### Example response\n\n"
        to_write += method.example_response
        to_write += "\n## Exceptions\n\n"
        for exception in method.exceptions:
            to_write += f'- [{exception.exception}](/docs/python-sdk/exceptions/{exception.exception}): {exception.description}\n'
        to_write += "\n## Parameters detailed"
        to_write += "\n"
        for parameter in method.parameters:
            to_write += f"### {parameter.name}\n\n"
            to_write += parameter.description
            to_write += "\n"
            to_write += f'- type: `{parameter.param_type}`\n'
            to_write += f'- example: `{parameter.example}`\n'
            to_write += "\n"

        with open(os.path.join(folder_name, f"{method.name.replace('_', '-')}.mdx"), "w+") as f:
            f.write(to_write)

    def _write_main_class(self, main_class: MainClass):
        folder_name = create_folder_name(main_class.name)
        self._create_folder_in_dest(folder_name)
        self._create_module_main_file(self,
                                      folder_name,
                                      main_class.name,
                                      main_class.short_description,
                                      main_class.long_description)
        for method in main_class.methods:
            self._write_method(folder_name, method)

    def write(self, project: Project):
        self._create_dest_folders()
        for main_class in project.main_classes:
            self._write_main_class(main_class)
