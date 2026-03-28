from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import shutil
import os
import matplotlib.pyplot as plt
import numpy as np

class Util:
        
    def connectDriver(): 
            # Set up Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Uncomment to run in headless mode (no GUI)
            chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
            chrome_options.add_argument("--no-sandbox")  # Disable sandboxing (for CI environments)

            # Specify the path to your chromedriver (adjust the path if necessary)
            #service = Service('/Users/tommythomasson/Downloads/chromedriver-mac-arm64/chromedriver')
            service = Service(ChromeDriverManager().install())

            # Initialize the WebDriver with Chrome options
            driver = None
            try:
                driver = webdriver.Chrome(service=service, options=chrome_options)
            except:
                driver_cache_path = os.path.expanduser("~/.wdm/drivers/chromedriver")
                shutil.rmtree(driver_cache_path)
                
                print("Removing and Redownloading Chrome Driver")
                return Util.connectDriver()
            
            # need to wrap this in try except and delete current driver if broken, then rerun
            # rm -rf ~/.wdm/drivers/chromedriver
            
            return driver
    
    def print_dict(d, indent=0):
        """
        Recursively prints a dictionary with nested structures using indentation.
        """
        for key, value in d.items():
            # Print the key with indentation
            print("\t" * indent + f"'{key}': ", end="")
            
            # If the value is a dictionary, call the function recursively
            if isinstance(value, dict):
                print("{")
                Util.print_dict(value, indent + 1)
                print("\t" * indent + "},")
            else:
                # Print the value if it's not a dictionary
                print(f"'{value}',")
    
    def write_dict_to_file(d, file, indent=0):
        for key, value in d.items():
            file.write("\t" * indent + f"'{key}': ")
            if isinstance(value, dict):
                file.write("{\n")
                Util.write_dict_to_file(value, file, indent + 1)
                file.write("\t" * indent + "},\n")
            else:
                file.write(f"'{value}',\n")


    '''
    odds: [[stat_value, odd_value]]
    stats: [[date, stat]]
    '''
    def createPlot(odds: list, stats: list):
        dates, values = zip(*stats)
        values = [int(val) for val in values]
        stat_values, odd_values = zip(*odds)
        stat_values = [int(stat.strip('+')) for stat in stat_values]

        labels = [f'{stat_values[i]} {odd_values[i]}' for i in range(len(stat_values))]

        lines = []
        for val in stat_values:
            row = [val]*len(dates)
            lines.append(row)
        
        plt.bar(dates, values)
        for i in range(len(lines)):
            plt.plot(dates, lines[i], label=labels[i])
        plt.legend(loc='best')
        plt.ylabel("Stats")
        plt.xlabel("Date")
        plt.ylim(bottom=0)
        plt.xticks(rotation=75)

        plt.savefig('test_plot.png')

        print("total average hits", np.mean(values))
        nonzero = sum(1 for val in values if val != 0)
        print("percent 1+ hits: ", nonzero / len(values))
        print("-250 implies 71% probability")

        over2 = sum(1 for val in values if val >= 2)
        print("percent 2+ hits: ", over2 / len(values))
        print("+200 implies 33% probability")
        

