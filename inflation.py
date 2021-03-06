#!/usr/bin/env python

import sys
from datetime import timedelta

import click

from golosscripts.decorators import common_options, helper
from golosscripts.golos_helper import STEEMIT_BLOCK_INTERVAL


@click.command()
@common_options
@helper
@click.option('--virtual-supply', default=0, type=float, help='override current virtual_supply')
@click.option('--long-term', default=False, is_flag=True, help='calculate long-term inflation')
@click.option('--years', default=50, type=int, help='number of years to calculate inflation for')
@click.pass_context
def main(ctx, virtual_supply, long_term, years):
    """
    Calculate current inflation or model long-term inflation.

    By default, only current daily inflation is calculated. Use --long-term flag to calculate inflation for years
    """
    daily_data = ctx.helper.calc_inflation(precise_rewards=True)
    print('virtual supply: {:,.0f}'.format(daily_data.virtual_supply))
    print('inflation rate: {:.2%}'.format(daily_data.current_inflation_rate))
    print('total daily: {:.0f}'.format(daily_data.total))
    print('workers: {:.0f}'.format(daily_data.worker))
    print('witness: {:.0f}'.format(daily_data.witness))
    print('vesting: {:.0f}'.format(daily_data.vesting))
    print('content: {:.0f}'.format(daily_data.content))
    print('top19 witnesses reward: {:.0f}'.format(daily_data.top19))
    print('single top19 witness: {:.0f}'.format(daily_data.top19 / 19))
    print('timeshare witnesses reward: {:.0f}'.format(daily_data.timeshare))

    if not long_term:
        sys.exit(0)

    props = ctx.helper.get_dynamic_global_properties()
    head_block_num = props['head_block_number']
    days = 365
    delta = timedelta(days=days)
    year = 0
    virtual_supply = None

    while year < years:
        stop_block_num = head_block_num + delta.total_seconds() / STEEMIT_BLOCK_INTERVAL
        data = ctx.helper.calc_inflation(
            start_block_num=head_block_num, stop_block_num=stop_block_num, virtual_supply=virtual_supply
        )
        virtual_supply = data.virtual_supply
        head_block_num = stop_block_num + 1
        year += 1

        daily_data = ctx.helper.calc_inflation(start_block_num=head_block_num, virtual_supply=virtual_supply)
        print(
            'New GOLOS daily on block {} ({:.0f} years): {:.0f}. Rate: {:.2%}. Virtual Supply: {:,.0f}'.format(
                int(head_block_num),
                year,
                daily_data.total,
                daily_data.current_inflation_rate,
                daily_data.virtual_supply,
            )
        )


if __name__ == '__main__':
    main()
