from json import dump, loads


def json_qualifier(section):
    with open(f'./json/{section}.json') as f:
        json = loads(f.read())
    res = []
    tmp = {}
    i = 0
    products = json['products']
    needful_keys = ['id', 'name']
    for product in products:
        for key, value in product.items():
            i += 1
            if i > 2:
                return None
            if key in needful_keys:
                print(f'First iteration: {key}: {value}')
                for i in range(len(needful_keys)):
                    print(f'Second iteration: {key}: {value}')
                    tmp.update({key: value})
                    print(tmp)
                res.append(tmp)
    return res
    #return {key: value for key, value in products.items() if key in needful_keys}


if __name__ == '__main__':
    # print(json_qualifier('house'))
    json_qualifier('house')
