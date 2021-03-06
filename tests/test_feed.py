import asyncio

import pytest
from golos.utils import fmt_time_from_now
from golosbase.exceptions import UnhandledRPCError

from golosscripts.feed import FeedUpdater, market_data


@pytest.fixture(scope='module')
def feed(nodes, node_bts):
    # Key is just random, don't bother
    config = {
        'witness': 'lex',
        'node': nodes,
        'node_gph': node_bts,
        'keys': '5JypMRUoJpsTZcYw2y9PX58WeHa937eJE3FzhA1cQe9zsHTHCWd',
    }
    return FeedUpdater(**config)


def test_init(nodes, node_bts):

    config = {
        'witness': 'foo',
        'node': nodes,
        'node_gph': node_bts,
        'keys': '5JypMRUoJpsTZcYw2y9PX58WeHa937eJE3FzhA1cQe9zsHTHCWd',
        'source': 'xynta',
    }
    with pytest.raises(ValueError, match='unknown price source'):
        FeedUpdater(**config)

    config = {
        'witness': 'foo',
        'node': nodes,
        'node_gph': node_bts,
        'keys': '5JypMRUoJpsTZcYw2y9PX58WeHa937eJE3FzhA1cQe9zsHTHCWd',
        'metric': 'xynta',
    }
    with pytest.raises(ValueError, match='unknown metric'):
        FeedUpdater(**config)

    config = {
        'witness': 'foo',
        'node': nodes,
        'node_gph': node_bts,
        'keys': '5JypMRUoJpsTZcYw2y9PX58WeHa937eJE3FzhA1cQe9zsHTHCWd',
    }
    FeedUpdater(**config)


def test_calc_weighted_average_price():
    prices = [
        market_data(1, 10.0, 'm1'),
        market_data(2, 10.0, 'm2'),
    ]
    price = FeedUpdater.calc_weighted_average_price(prices)
    assert price == 1.5


def test_is_last_price_too_old():
    timestamp = fmt_time_from_now(-60)
    witness_data = {'last_sbd_exchange_update': timestamp}

    assert FeedUpdater.is_last_price_too_old(witness_data, 30) is True
    assert FeedUpdater.is_last_price_too_old(witness_data, 90) is False


@pytest.mark.asyncio
async def test_calc_price_gph_golos(feed):
    price = await feed.calc_price_gph_golos()
    assert 0 < price < 100


@pytest.mark.asyncio
async def test_calc_price_gbg_golos_bitshares(feed):
    price = await feed.calc_price_gbg_golos_bitshares()
    assert 0 < price < 100


@pytest.mark.skip(reason='kuna delisted golos')
@pytest.mark.asyncio
async def test_calc_price_kuna(feed):
    price = await feed.calc_price_kuna()
    assert 0 < price < 100


@pytest.mark.asyncio
async def test_publish_price(feed):
    with pytest.raises(UnhandledRPCError, match='Missing Active Authority'):
        await feed.publish_price(force=True)


@pytest.mark.asyncio
async def test_run_forever(feed, monkeypatch):
    async def mock():
        pass

    monkeypatch.setattr(feed, 'publish_price', mock)

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(feed.run_forever(), timeout=1)
