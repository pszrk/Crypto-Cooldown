import external_api as api
from datetime import datetime



def get_data(coin):
    return api.get_ohlc(coin)
    # response is list of lists with format: [timestamp, o, h, l, c]


def latest_price(data):
    if data is None: 
        return
    current = data[-1][4]
    print(current)
    return current


def ath(data):
    if data is None: 
        return
    max_price = max(data, key=lambda x: x[2])
    date = datetime.utcfromtimestamp(max_price[0] / 1000).strftime('%d-%m-%Y')
    print( f"ATH {[max_price[2]]} {date}")
    return [max_price[2], max_price[0]] # returns price, timestamp


def min_after_ath(data, ath_timestamp):
    after_ath = [ (timestamp, low)
                 for timestamp, open, high, low, close in data
                 if timestamp > ath_timestamp]
    if after_ath:
        min_price = min(after_ath, key=lambda x: x[1])
        date = datetime.utcfromtimestamp(min_price[0] / 1000).strftime('%d-%m-%Y')
        print( f"min after ATH {[min_price[1]]} {date}")
        return [min_price[1], min_price[0]] # returns price, timestamp


def peak_21(ath_timestamp):
    # convert to seconds
    value = True if datetime.utcfromtimestamp(ath_timestamp/1000).year == 2021 else False
    print(f"crypto era ath: {value}")
    return value


def decline_from_ath(current, ath):
    amount = ath - current
    percentage = (amount/ath)*100
    print(f"decline from ath is {amount} or {percentage} %")
    return percentage


def gain_to_ath(current, ath):
    amount = ath - current
    percentage = (amount / current) *100
    print(f"would have to gain {percentage} % to reach ath")
    return percentage


def tracked_since(data):
    first_timestamp = datetime.utcfromtimestamp(data[0][0] / 1000).strftime('%d-%m-%Y')
    print(f"tracked since {first_timestamp}")
    return first_timestamp


def tracked_in_21(data):
    result = datetime.utcfromtimestamp(data[0][0]/1000).year <= 2021
    print(f"tracked in 2021?: {result}")
    return result


def null(coin):
    return{
        "name": coin,
        "price": None,
        "ath": None,
        "ath_date": None,
        "low_after_ath": None,
        "low_after_ath_date": None,
        "decline_from_ath": None,
        "ath_was_in_2021": None,
        "gain_to_ath": None,
        "tracked_from": None,
        "around_in_21": None,
    }


def calculate_stats(coin):
    print(coin)
    data = get_data(coin)
    if not data: 
        return null(coin)
    price = latest_price(data)
    ath_data = ath(data)
    min_after_ath_data = min_after_ath(data, ath_data[1])
    ath_21 = peak_21(ath_data[1])
    ath_selloff = decline_from_ath(price, ath_data[0])
    to_ath = gain_to_ath(price, ath_data[0])
    tracked_from = tracked_since(data)
    tracked_21 = tracked_in_21(data)
    return{
        "name": coin,
        "price": price,
        "ath": ath_data[0],
        "ath_date": datetime.utcfromtimestamp(ath_data[1] / 1000).strftime('%d-%m-%Y'),
        "low_after_ath": min_after_ath_data[0],
        "low_after_ath_date": datetime.utcfromtimestamp(min_after_ath_data[1] / 1000).strftime('%d-%m-%Y'),
        "decline_from_ath": ath_selloff,
        "ath_was_in_2021": ath_21,
        "gain_to_ath": to_ath,
        "tracked_from": tracked_from,
        "around_in_21": tracked_21
    }


if __name__ == "__main__":
    print(calculate_stats("bitcoin"))
