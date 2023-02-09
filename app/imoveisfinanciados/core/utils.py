def extract_city_data(city, dependents=False):
    data = dict()
    if dependents:
        data['subsidy_max'] = city.d_subsidy_max and city.d_subsidy_max or city.subsidy_max
        data['subsidy_min'] = city.d_subsidy_min and city.d_subsidy_min or city.subsidy_min
        data['multsub'] = city.d_multsub and city.d_multsub or city.multsub
    else:
        data['subsidy_max'] = city.subsidy_max
        data['subsidy_min'] = city.subsidy_min
        data['multsub'] = city.multsub

    return data