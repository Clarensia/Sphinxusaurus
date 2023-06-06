# Sphinxusaurus

Generate a docusaurus documentation from a Sphinx Python project.

Be careful, this generator works only with: [Human-Readable-OpenAPI-Client](https://github.com/Clarensia/Human-Readable-OpenAPI-Client-Generator)

## Format to respect

### Method

All class methods docstring should look like the one below.

Please note, the "Example response" is very important.

```python
    async def exchanges(self, page: int = 1, blockchain: str | None = None) -> Exchanges:
        """Get the list of supported exchanges by the API

        :raises BlockchainNotSupportedException: When an invalid blockchain id is given
        :raises InvalidPageException: When an invalid page is given

        :param page: You can ignore this value for this version of the API., defaults to 1
        :type page: int, Optional
        :param blockchain: The blockchain from which you want to get the exchanges, defaults to None
        :type blockchain: str, Optional
        :return: The list of all supported exchange of the API.
        
        You can use the exchange id responded from this for other API calls.


        Example response:
        ```json
        {
            "page": 1,
            "total_pages": 1,
            "data": [
                {
                    "exchange": "lydia_finance_avalanche",
                    "blockchain": "avalanche",
                    "name": "Lydia Finance",
                    "url": "https://exchange.lydia.finance/#/swap",
                    "fee": 200
                },
                {
                    "exchange": "oliveswap_avalanche",
                    "blockchain": "avalanche",
                    "name": "Oliveswap",
                    "url": "https://avax.olive.cash/",
                    "fee": 250
                }
            ]
        }

        ```
        :rtype: Exchanges
        """
        pass
```

### Class

For class documentation, you can use normal docstring without attributes.
