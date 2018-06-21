import time as t
import pandas as pd

class SaveDataCSV():
    def __init__(self, file_name="new_test_data.csv"):
        self.file_name = file_name
        self.date_format = "%H:%M:%S" #+millis
        #self.date_format="%Y/%m/%d %H:%M:%S"
        self.hist_data = {}
        
    def save_data(self, new_data_dict):
        curr_time = t.strftime(self.date_format, t.gmtime())
        millis = int(round(t.time() * 1000)%1000)
        self.hist_data[curr_time+f" +{millis}"] = new_data_dict
        #print(self.hist_data)
        
    def save_csv(self):
        if self.hist_data != {}:
            pd_hist_data = pd.DataFrame.from_dict(self.hist_data, orient='index')
            pd_hist_data.to_csv(path_or_buf=self.file_name, sep=',', index=True, index_label='Timestamp')
            print(f"Data saved in {self.file_name}")

    """
    def clear_all_data(self):
        self.hist_data = {}
    
    def clear_data(self, timestamp):
        try:
            del self.hist_data[timestamp]
        except KeyError as e:
            print(e)
    """

if __name__ == "__main__":
    print("\nThis is just a test to save some\nautofenetared data in the current folder\n")
    s = SaveDataCSV()
    for n in range(10):
        s.save_data({'a':1})
        t.sleep(0.1)
        s.save_data({'b':2})
        t.sleep(0.1)
    s.save_csv()