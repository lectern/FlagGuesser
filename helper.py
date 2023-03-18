def get_flags():
    countries = open('countries.csv', 'r', encoding="utf-8").read().splitlines()

    with open("countries.py", "a", encoding="utf-8") as f:
        f.write("country_ids = {")
        for country in countries:
            country = country.split(",")
            # 
            f.write(f"\t\"{country[0]}\": \"{country[1]}\",\n")
        f.write("}")

if __name__ == "__main__":
    get_flags()