def city_letters(city_name: str) -> str:
    ls = list()
    for _ in city_name:
        ls[_] = city_name[_]

    for char in ls:
        print(f"'{char}:'")
        for char in city_name:
            print("*")

city_letters("Chicago")
city_letters("Bangkok")
city_letters("Lav Vegas")