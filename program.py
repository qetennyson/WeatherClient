import requests
import bs4
import collections

WeatherReport = collections.namedtuple('WeatherReport',
                                       'cond, temp, scale, loc')


def main():
    print_the_header()

    z_code = input("What zipcode do you want the weather for (ex. 42101)? ")

    html = get_html_from_web(z_code)

    report = get_weather_from_html(html)

    # this is quite limited.  we have to check our
    # return value in all cases to print the correct thing
    print("The temp in this location is {}.".format(report[1]))

    # see?  nonsense!  Let's use named tuples.
    print('The temp in {} is {} and {} {}'.format(
        report[2],
        report[0],
        report[1],
        report[3]

    ))  # The power of named tuples.
    print('The temp in {} is {} {} and {}'.format(
        report.loc,
        report.temp,
        report.scale,
        report.cond
    ))

    # display forecastpip


def print_the_header():
    print("--------------------------")
    print("   LILOO'S WEATHER APP")
    print("--------------------------")
    print()


def get_html_from_web(zipcode):
    url = "https://www.wunderground.com/weather-forecast/{}".format(zipcode)
    response = requests.get(url)

    return response.text


def get_weather_from_html(html):
    # cityCSS = '.region-content-header h1'
    # weatherScaleCSS = '.wu-unit-temperature.wu-label'
    # weatherTempCSS = '.wu-unit-temperature.wu-value'
    # weatherConditionCss = '.condition-icon'

    soup = bs4.BeautifulSoup(html, 'html.parser')
    loc = soup.find(class_='region-content-header').find('h1').get_text()
    condition = soup.find(class_='condition-icon').get_text()
    temp = soup.find(class_='wu-unit-temperature').find(class_='wu-value').get_text()
    scale = soup.find(class_='wu-unit-temperature').find(class_='wu-label').get_text()

    loc = cleanup_text(loc)
    loc = find_citystate_from_location(loc)
    condition = cleanup_text(condition)
    temp = cleanup_text(temp)
    scale = cleanup_text(scale)

    # print(condition, temp, scale, loc)
    # return condition, temp, scale, loc

    # PERFECTION.
    report = WeatherReport(cond=condition, temp=temp, scale=scale, loc=loc)
    return report


def find_citystate_from_location(loc):
    parts = loc.split("\n")
    return parts[0].strip()


# Define a function using a text hint parameter (: str does not affect runtime)
def cleanup_text(text: str):
    if not text:
        return text

    text = text.strip()
    return text


if __name__ == '__main__':
    main()
