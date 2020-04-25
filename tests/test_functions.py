import pytest

from golosscripts.functions import (
    fetch_ticker,
    get_price_btc_usd_exchanges,
    get_price_gold_rub_cbr,
    get_price_gold_usd_cbr,
    get_price_usd_rub_cbr,
)


def test_get_price_gold_rub_cbr():
    price = get_price_gold_rub_cbr()
    assert price > 0


def test_get_price_usd_rub_cbr():
    price = get_price_usd_rub_cbr()
    assert price > 50


def test_get_price_gold_usd_cbr():
    price = get_price_gold_usd_cbr()
    assert price > 0


@pytest.mark.asyncio
async def test_fetch_ticker():
    ticker = await fetch_ticker('binance', 'BTC/USDT')
    assert 'last' in ticker


@pytest.mark.asyncio
async def test_get_price_btc_usd_exchanges():
    price = await get_price_btc_usd_exchanges()
    assert price > 0
