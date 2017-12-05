from settings_analyzer.models import StopWordList, Settings


def filter_parse(title, description, price, currency, city=''):
    for stop in StopWordList.objects.values_list('word', flat=True):
        if stop in title or stop in description or stop in city:
            return False

    if price and isinstance(price, str):
        price = int(price)

    if isinstance(price, int):
        if currency == '$':
            price_usd_from = Settings.get_solo().price_usd_from
            price_usd_to = Settings.get_solo().price_usd_to
            if price_usd_from and price < price_usd_from:
                return False
            if price_usd_to and price > price_usd_to:
                return False

        else:
            price_hrn_from = Settings.get_solo().price_hrn_from
            price_hrn_to = Settings.get_solo().price_hrn_to
            if price_hrn_from and price < price_hrn_from:
                return False
            if price_hrn_to and price > price_hrn_to:
                return False

    return True