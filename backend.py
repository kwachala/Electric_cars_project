import itertools
import ahpy
import pandas as pd


def get_car(name, df):
    battery_best = (df[df['name'] == name]['battery'].values[0])
    segment_best = (df[df['name'] == name]['segment'].values[0])
    seats_best = (df[df['name'] == name]['seats'].values[0])
    drive_best = (df[df['name'] == name]['drive'].values[0])
    price_best = (df[df['name'] == name]['price'].values[0])
    body_best = (df[df['name'] == name]['body'].values[0])
    zero_to_100_best = (df[df['name'] == name]['zero_to_100'].values[0])
    topspeed_best = (df[df['name'] == name]['topspeed'].values[0])
    range_best = (df[df['name'] == name]['range'].values[0])
    efficiency_best = (df[df['name'] == name]['efficiency'].values[0])
    fastcharge_best = (df[df['name'] == name]['fastcharge'].values[0])

    car = [name, battery_best, segment_best, seats_best, drive_best, price_best, body_best, zero_to_100_best,
           topspeed_best, range_best, efficiency_best, fastcharge_best]

    return car


def cut_dataframe(df, values):
    new_df = df.drop(df[df.body != values[0]].index)

    if values[-1] == 'Nie':
        new_df = new_df.drop(new_df[new_df.price < values[1][0]].index)
        new_df = new_df.drop(new_df[new_df.price > values[1][1]].index)
    elif values[-1] == 'Tak' and values[0] == 'Minivan':
        new_df = new_df.drop(new_df[new_df.price - 70000 / 4.72 < values[1][0]].index)
        new_df = new_df.drop(new_df[new_df.price - 70000 / 4.72 > values[1][1]].index)
    else:
        new_df = new_df.drop(new_df[new_df.price - 27000 / 4.72 < values[1][0]].index)
        new_df = new_df.drop(new_df[new_df.price - 27000 / 4.72 > values[1][1]].index)

    new_df = new_df.drop(new_df[new_df.range < values[2][0]].index)
    new_df = new_df.drop(new_df[new_df.range > values[2][1]].index)
    new_df = new_df.drop(new_df[new_df.seats != values[3]].index)
    new_df = new_df.drop(new_df[new_df.drive != values[4]].index)
    new_df = new_df.drop(new_df[new_df.topspeed < values[5][0]].index)
    new_df = new_df.drop(new_df[new_df.topspeed > values[5][1]].index)
    new_df = new_df.drop(new_df[new_df.zero_to_100 < values[6][0]].index)
    new_df = new_df.drop(new_df[new_df.zero_to_100 > values[6][1]].index)

    print(new_df)

    return new_df


def get_best(values):
    df = pd.read_json('base.json')

    df = cut_dataframe(df, values)

    cars = df['name'].tolist()

    if len(cars) == 1:
        best = get_car(cars[0], df)
        best.append(values[-1])

        return best

    elif len(cars) == 0:
        best = 'Nie ma takiego pojazdu'

        return best

    else:
        vehicle_pairs = list(itertools.combinations(cars, 2))

        criteria_comparisons = {('price', 'range'): values[7][0] / values[7][1],
                                ('price', 'topspeed'): values[7][0] / values[7][2],
                                ('price', '0-100'): values[7][0] / values[7][3],
                                ('range', 'topspeed'): values[7][1] / values[7][2],
                                ('range', '0-100'): values[7][1] / values[7][3],
                                ('topspeed', '0-100'): values[7][2] / values[7][3]}

        print(criteria_comparisons)

        price_comparisons = {}
        zero_to_100_comparisons = {}
        topspeed_comparisons = {}
        range_comparisons = {}

        for i in range(len(vehicle_pairs)):
            if values[-1] == 'Tak' and (df[df['name'] == vehicle_pairs[i][0]]['segment'].values[0]) == 'N':
                price_x = (df[df['name'] == vehicle_pairs[i][0]]['price'].values[0]) - 70000
            elif values[-1] == 'Tak':
                price_x = (df[df['name'] == vehicle_pairs[i][0]]['price'].values[0]) - 27000
            else:
                price_x = (df[df['name'] == vehicle_pairs[i][0]]['price'].values[0])

            if values[-1] == 'Tak' and (df[df['name'] == vehicle_pairs[i][0]]['segment'].values[0]) == 'N':
                price_y = (df[df['name'] == vehicle_pairs[i][0]]['price'].values[0]) - 70000
            elif values[-1] == 'Tak':
                price_y = (df[df['name'] == vehicle_pairs[i][0]]['price'].values[0]) - 27000
            else:
                price_y = (df[df['name'] == vehicle_pairs[i][0]]['price'].values[0])

            zero_to_100_x = (df[df['name'] == vehicle_pairs[i][0]]['zero_to_100'].values[0])
            zero_to_100_y = (df[df['name'] == vehicle_pairs[i][1]]['zero_to_100'].values[0])
            topspeed_x = (df[df['name'] == vehicle_pairs[i][0]]['topspeed'].values[0])
            topspeed_y = (df[df['name'] == vehicle_pairs[i][1]]['topspeed'].values[0])
            range_x = (df[df['name'] == vehicle_pairs[i][0]]['range'].values[0])
            range_y = (df[df['name'] == vehicle_pairs[i][1]]['range'].values[0])

            price_comparisons[vehicle_pairs[i]] = price_y / price_x
            zero_to_100_comparisons[vehicle_pairs[i]] = zero_to_100_y / zero_to_100_x
            topspeed_comparisons[vehicle_pairs[i]] = topspeed_x / topspeed_y
            range_comparisons[vehicle_pairs[i]] = range_x / range_y

            price = ahpy.Compare('price', price_comparisons, precision=3, random_index='dd')
            zero_to_100 = ahpy.Compare('zero_to_100', zero_to_100_comparisons, precision=3, random_index='dd')
            topspeed = ahpy.Compare('topspeed', topspeed_comparisons, precision=3, random_index='dd')
            range_score = ahpy.Compare('range', range_comparisons, precision=3, random_index='dd')
            criteria = ahpy.Compare('criteria', criteria_comparisons, precision=3, random_index='dd')

            criteria.add_children([price, zero_to_100, topspeed, range_score])

            best = get_car(list(criteria.target_weights.keys())[0], df)
            best.append(values[-1])

            return best
