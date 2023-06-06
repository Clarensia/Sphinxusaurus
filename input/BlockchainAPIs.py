class BlockchainAPIs:
    """High-frequency DEX API
    """

    async def blockchains(self) -> List[Blockchain]:
        """Get the list of blockchains supported by the API


        :return: The list of the blockchains supported by the API.
        
        Using this method, you can find the id of the blockchain that you can use for
        other function calls.


        Example response:
        ```json
        [
            {
                "blockchain": "avalanche",
                "name": "Avalanche",
                "chain_id": 43114,
                "explorer": "https://snowtrace.io/"
            }

        ]
        ```
        :rtype: List[Blockchain]
        """
        ret = await self._do_request("/v0/blockchains/")
        return [
            Blockchain(
                blockchain=r["blockchain"],
                name=r["name"],
                chain_id=r["chain_id"],
                explorer=r["explorer"]
            )
            for r in ret
        ]

    async def exchanges(self, page: int = 1, blockchain: str | None = None) -> Exchanges:
        """Get the list of supported exchanges by the API

        :raises BlockchainNotSupportedException: When an invalid blockchain id is given
        :raises InvalidPageException: When an invalid page is given

        :param page: You can ignore this value for this version of the API., defaults to 1
        :type page: int, Optional
        :example page: 1
        :param blockchain: The blockchain from which you want to get the exchanges, defaults to None
        :type blockchain: str, Optional
        :example blockchain: ethereum
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
        params = {}
        params["page"] = page
        if blockchain is not None:
            params["blockchain"] = blockchain
        ret = await self._do_request("/v0/exchanges/", params)
        return Exchanges(
            page=ret["page"],
            total_pages=ret["total_pages"],
            data=[
                Exchange(
                    exchange=d["exchange"],
                    blockchain=d["blockchain"],
                    name=d["name"],
                    url=d["url"]
                )
                for d in ret["data"]
            ]
        )
