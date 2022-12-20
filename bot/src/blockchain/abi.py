import pathlib


def _read_abi(filename: str) -> str:
    path = pathlib.Path("abi", f"{filename}.json")
    return path.read_text(encoding="UTF-8")


ERC20 = _read_abi("ERC20")
RewardTracker = _read_abi("RewardTracker")
