import os
import pandas as pd
import zipfile
from collections import OrderedDict

USER = os.getlogin()
PATH = f"C:\\Users\\{USER}\\Desktop\\Empatica_temporary"

def compute_duration():
    files = os.listdir(PATH)
    file_to_read = 'EDA' # 'HR'

    total_time = 0 # in seconds

    for file in files:
        zip_file = os.path.join(PATH, file)
        with zipfile.ZipFile(zip_file) as z:
            with z.open(f"{file_to_read}.csv") as f:
                df = pd.read_csv(f)
                sample_rate = df.iloc[0].values[0]
                rows = df.shape[0] - 1
                file_time = rows / sample_rate
                total_time += rows / sample_rate

    #print(f"Time in seconds: {total_time}")
    #print(f"Time in minutes: {total_time / 60}")
    #print(f"Time in hours: {total_time / 3600}")
    #print(f"Time in days: {total_time / 86400}")
    return f'{(total_time / 3600):.2f}'

def rename_files(em_id, lab_visit):
    files = list(os.scandir(PATH))

    ## Sort based on the download/modify time
    #files.sort(key=lambda x: os.path.getmtime(x))
    #for ii, file in enumerate(files, start=1):
    #    os.rename(file.path, f'{PATH}/sub-{em_id}_pre_{lab_visit}_wrb_emp_{ii:02}.zip')

    ## Sort based on the timestamp in the filename
    try:
        files_ = {}
        for f in files:
            files_[f.name.split('_')[0]] = f

        files_ = OrderedDict(sorted(files_.items()))

        ii = 1
        for key, file in files_.items():
            os.rename(file.path, f'{PATH}/sub-{em_id}_pre_{lab_visit}_wrb_emp_{ii:02}.zip')
            ii += 1
    except FileExistsError as e:
        print(e)
        files.sort(key=lambda x: os.path.getmtime(x))
        for ii, file in enumerate(files, start=1):
            os.rename(file.path, f'{PATH}/sub-{em_id}_pre_{lab_visit}_wrb_emp_{ii:02}.zip')


if __name__ == '__main__':
    rename_files('abc', '420')