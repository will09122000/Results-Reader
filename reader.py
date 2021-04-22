import cv2
import pytesseract
import numpy as np
import pandas

def main():
    # Iterate through each stage
    for stage_num in range(1, 6):
        words, num_entries = read_image(stage_num)

        drivers, vehicles, times = format_data(words, num_entries)

        # Write to CSV
        df = pandas.DataFrame(data={
                                    "driver": drivers,
                                    "vehicle": vehicles,
                                    "stage": times
                                    })
        file_path = "./results/{}.csv".format(stage_num)
        df.to_csv(file_path, sep=',', index=False)

        print("Successfully created CSV file for stage " + str(stage_num))


def read_image(stage_num):
    try:
        # Get stage screenshot
        img_path = r".\screenshots\{}.png".format(stage_num)
        img = cv2.imread(img_path)
        img = cv2.resize(img, None, fx=5, fy=5)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        print("Error: Cannot read file: " + str(stage_num) + ".png")
        exit()
    else:
        # Read text from image
        kernel = np.ones((2, 1), np.uint8)
        pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract.exe')
        output = pytesseract.image_to_string(img, lang='eng')

        # Remove blanks
        words = list(filter(None, output.split('\n')))

        # Get number of entries
        num_entries = 0
        for word in words:
            if ":" in word and "." in word:
                num_entries += 1

        return words, num_entries


def format_data(words, num_entries):
    # Split word list
    drivers = words[1:num_entries+1]
    vehicles = words[num_entries+2:num_entries*2+2]
    times = words[num_entries*2+3:num_entries*3+3]

    # Fix driver names
    for i in range(len(drivers)):
        if " | " in drivers[i]:
            drivers[i] = "Mr. Beletal"
        elif "912" in drivers[i]:
            drivers[i] = "Will0912"
        elif "L1GHTNING14" in drivers[i] or "GHTN" in drivers[i]:
            drivers[i] = "L1GHTN1NG14"
        elif "XSEMP" in drivers[i]:
            drivers[i] = "XSempiternal012"
        elif "MUSH" in drivers[i]:
            drivers[i] = "V.Mushroom"
        elif "CALL" in drivers[i]:
            drivers[i] = "Calli"
        elif "MIN" in drivers[i]:
            drivers[i] = "Suk Min Dik"
        elif "DROP" in drivers[i]:
            drivers[i] = "Dropi"
        elif "DIEGO" in drivers[i]:
            drivers[i] = "Diego_Domo2"
        else:
            drivers[i] = drivers[i].title()

    # Fix vehicle names
    for i in range(len(vehicles)):
        vehicles[i] = vehicles[i].title()
        if "Citroen" in vehicles[i]:
            vehicles[i] = vehicles[i].replace("Citroen", "Citroën")
        elif "Rs" in vehicles[i]:
            vehicles[i] = vehicles[i].replace("Rs", "RS")

    # Fix stage times
    for i in range(len(times)):
        times[i] = times[i].replace("/", "")
        if (len(times[i]) > 9):
            times[i] = times[i][0:-1]
        elif (len(times[i]) < 9) or ":" not in times[i] or "." not in times[i]:
            print("INACCURACY: The stage time '" + times[i] + "' is incorrect at row "
                  + str(i+1) + " for the CSV file below")

    return drivers, vehicles, times

if __name__ == "__main__":
    main()
