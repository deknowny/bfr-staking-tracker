import asyncio
import dataclasses

import loguru
import vkquick as vq

from src.blockchain import addresses, abi
from src.blockchain.provider import ARBITRUM_PROVIDER
from src.users import USERS


pkg = vq.Package()


@dataclasses.dataclass
class ClaimableRewardsReport:
    esbfr_claimable: int
    mp_claimable: int
    usdc_claimable: int

    def render(self) -> str:
        message = ""
        message += "[ Claimable ]"
        message += f"\nESBFR: {self.esbfr_claimable / 10**18:.5f}"
        message += f"\nMP: {self.mp_claimable / 10**18:.5f}"
        message += f"\nUSDC: {self.usdc_claimable / 10**6:.5f}"

        return message


@pkg.on_clicked_button()
@pkg.command("track")
async def track(ctx: vq.NewMessage):
    account_address = USERS[str(ctx.msg.from_id)]["address"]

    esbfr_claimable, mp_claimable, usdc_claimable = await asyncio.gather(
        ARBITRUM_PROVIDER.eth.contract(
            address=addresses.ESBFR_REWARD_TRACKER,
            abi=abi.RewardTracker
        ).functions.claimable(account_address).call(),
        ARBITRUM_PROVIDER.eth.contract(
            address=addresses.MP_REWARD_TRACKER,
            abi=abi.RewardTracker
        ).functions.claimable(account_address).call(),
        ARBITRUM_PROVIDER.eth.contract(
            address=addresses.USDC_REWARD_TRACKER,
            abi=abi.RewardTracker
        ).functions.claimable(account_address).call(),
    )

    report = ClaimableRewardsReport(
        esbfr_claimable=esbfr_claimable,
        mp_claimable=mp_claimable,
        usdc_claimable=usdc_claimable
    )

    await ctx.answer(report.render())
