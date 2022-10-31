from utils import *
import _g


ticker_data = [
    {
        "ticker": "AAPL",
        "price": 100.50,
        "change": -10
    },
    {
        "ticker": "TSLA",
        "price": 124.50,
        "change": -50.4
    },
]

async def run():
    i = 0

    async def next_ticker():
        nonlocal i
        data = ticker_data[i]
        ticker_text, ticker_overflow = generate_word_offsets(data["ticker"], 1, 1, small_font=True)
        price_text, price_overflow = generate_word_offsets(f"${str(round(data["price"],2))}", 1, 5)
        change_text, change_overflow = generate_word_offsets(f"{str(data["change"])}%", 1, 11, small_font=True)

        queue_scroll(ticker_text, id="ticker", repeat=False)
        queue_scroll(price_text, id="price", repeat=False)
        queue_scroll(change_text, id="change", repeat=False)

        i += 1
        if i == len(ticker_data):
            i = 0

    _g.scroll_complete_callback = next_ticker

    await next_ticker()