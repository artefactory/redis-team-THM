import asyncio

from prompt_toolkit.input import create_input
from prompt_toolkit.keys import Keys


Engine = SearchEngine("https://docsearch.redisventures.com/api/v1/paper")

async def keypress_listener() -> None:
    done = asyncio.Event()
    input = create_input()

    def keys_ready():
        for key_press in input.read_keys():
            print(key_press)

            if key_press.key == Keys.ControlC:
                done.set()

    with input.raw_mode():
        with input.attach(keys_ready):
            await done.wait()


if __name__ == "__main__":
    asyncio.run(keypress_listener())