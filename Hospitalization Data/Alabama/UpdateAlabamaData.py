from tika import parser # pip install tika
from datetime import datetime
output = "06-22-2020,"

#file_out = open("ALData.csv", "w")
day = 7
month = 4
print(str(datetime.today()))
current_month = int(str(datetime.today())[5:7])
#current_month = 4
current_day = int(str(datetime.today())[8::10])

output_text = ""

failed = ""



while day < current_day or month < current_month:
    try:
        if day < 10:
            raw = parser.from_file(
                'https://www.alabamapublichealth.gov/covid19/assets/cov-al-cases-0' + str(month) + "0" + str(day) + '20.pdf')
        else:
            raw = parser.from_file(
                'https://www.alabamapublichealth.gov/covid19/assets/cov-al-cases-0' + str(month) + str(day) + '20.pdf')

        number_found = False
        data = raw['content']
        while not number_found:
            index = data.index(',')
            if data[index + 4].isdigit():
                if data[index + 5] == ',':
                    number = data[index+4] + data[index+6:index+9]
                else:
                    number = data[index+4::]
                    number = number[0:number.index("\n")]
                number_found = True
                output_text += str(month) + "-" + str(day) + "-2020," + number + "\n"
                print(output_text)
            elif data[index + 5].isdigit():
                if data[index + 6] == ',':
                    number = data[index + 5] + data[index + 7:index + 10]
                else:
                    number = data[index + 5::]
                    number = number[0:number.index("\n")]
                if not "," in number:
                    number_found = True
                    output_text += str(month) + "-" + str(day) + "-2020," + number + "\n"
                    print(output_text)

            data = data[index+1::]

            if not "," in data and not number_found:
                number_found = True
                print(str(month) + "-" + str(day) + "-2020 Failed")
                failed += str(month) + "-" + str(day) + "-2020\n"

        day += 1
        if day > 31:
            month += 1
            day = 1
    except IOError as er:
        print(str(month) + "-" + str(day) + "doesnt have data")
        day += 1
        if day > 31:
            month += 1
            day = 1
#file_out.write(output_text)
#file_out.close()

print(failed)

