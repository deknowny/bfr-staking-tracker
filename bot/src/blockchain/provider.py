import dataclasses
import enum

import loguru
import web3.eth
import web3.net

import src.envs


_async_eth_module = {"eth": (web3.eth.AsyncEth,), "net": (web3.net.AsyncNet,)}
ARBITRUM_PROVIDER = web3.Web3(
    web3.Web3.AsyncHTTPProvider(src.envs.ARBITRUM_RPC_URL),
    modules=_async_eth_module,
    middlewares=[],
)
