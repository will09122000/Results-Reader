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
    # Get stage screenshot
    img_path = r".\stages\{}.png".format(stage_num)
    img = cv2.imread(img_path)

    try:
        # Convert to black and white
        grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        grey, img_bin = cv2.threshold(grey, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        grey = cv2.bitwise_not(img_bin)
    except:
        print("Error: Cannot read file: " + str(stage_num) + ".png")
        exit()
    else:
        # Read text from image
        kernel = np.ones((2, 1), np.uint8)
        img = cv2.erode(grey, kernel, iterations=1)
        img = cv2.dilate(img, kernel, iterations=1)
        pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract.exe')
        out_below = pytesseract.image_to_string(img)

        # Remove blanks
        words = list(filter(None, out_below.split('\n')))

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
        if "ELETAL" in drivers[i] or "A | " in drivers[i]:
            drivers[i] = "Mr. Beletal"
        elif "WHLLO9I2" in drivers[i] or "OPT2" in drivers[i] or "OT2" in drivers[i] or "912" in drivers[i] or "WILLO" in drivers[i]:
            drivers[i] = "Will0912"
        elif "LIGHT" in drivers[i]:
            drivers[i] = "L1GHTN1NG14"
        elif "XSEMP" in drivers[i]:
            drivers[i] = "XSempiternal012"
        elif "VMUSHROOM" in drivers[i]:
            drivers[i] = "V.Mushroom"
        elif "CALL" in drivers[i]:
            drivers[i] = "Calli"
        elif "MIN" in drivers[i]:
            drivers[i] = "Suk Min Dik"
        elif "Rope" in drivers[i] or "DROP" in drivers[i]:
            drivers[i] = "Dropi"
        else:
            drivers[i] = drivers[i].title()

    # Fix vehicle names
    for i in range(len(vehicles)):
        vehicles[i] = vehicles[i].title()
        if "$" in vehicles[i]:
            vehicles[i] = vehicles[i].replace("$", "S")
        elif "Citroen" in vehicles[i]:
            vehicles[i] = vehicles[i].replace("Citroen", "Citroën")
        elif "Rs" in vehicles[i]:
            vehicles[i] = vehicles[i].replace("Rs", "RS")

    # Fix stage times
    for i in range(len(times)):
        if (len(times[i]) != 9):
            times[i] = times[i][0:-1]
    
    return drivers, vehicles, times

if __name__ == "__main__":
    main()
