
import os
import zipfile
import subprocess
import click


"""

    This script zips the ZMax files 
    To use it the .hyp files should be extracted in their corresponding integer denominated folders
    The .hyp files should also be located in the working folder
    IF the .hyp files came from more than 1 ZMax, they should be seperated into folders with a name 'zmax[zmax-id]'


    1. For each folder 1-7
        1.1. Enter each folder
            1.1.1. Zip the files in the folder
            1.1.2. Push zipfile up 1 dir
    2. Zip the hyp files 
    3. Handle edge case where data comes from >1 zmax
        3.1 Store each zmax's hyp files in a folder called 'zmax{zmax-id}'
        3.2 Zip together any folders with such matching folders
        
TODO:
    method to get current ZM id and lab_visit
        
sub-HB1ZM6075546_pre-1_wrb_zmx_1.zip  - zipfile template name
sub-HB1ZM6075546_pre-1_wrb_zmx_raw.zip - zipfile for raw data .hyp files
"""


class EmptyFolder(Exception):
    pass


def zip_folder_contents(path: str, zm_id: str, lab_visit):
    """ Zip contents of folders
    Parameters:
        path :: str
            path of folder whose content should be zipped
        zm_id :: str
            the ZMax id
        lab_visit :: str | int
            lab_visit
    """
    if len(os.listdir(path)) < 1:
        raise EmptyFolder(f'No files in folder: {path}')
    folder_name = os.path.split(path)[-1]
    zf = zipfile.ZipFile(f"sub-{zm_id}_pre-{lab_visit}_wrb_zmx_{folder_name}.zip", "w")

    for dirname, subdirs, files in os.walk(path):
        for f in files:
            if '.edf' in f:
                zf.write(os.path.join(dirname, f), arcname = f)


def zip_folder_contents2(path: str, zm_id, lab_visit):
    """ Faster version of above
        Uses 7Zip command line utility to zip files
    """
    folder_name = os.path.split(path)[-1]

    if len(os.listdir(path)) < 1:
        raise EmptyFolder(f'No files in folder: {path}')

    # Create cmd to run
    cmd = ["7z", "a", f"sub-{zm_id}_pre-{lab_visit}_wrb_zmax_{folder_name}.zip"]
    for dirname, subdirs, files in os.walk(path):
        for f in files:
            if '.edf' in f:
                cmd.append(str(os.path.join(dirname,  f)))

    print(cmd)
    # Run the 7-Zip cmd line utilty
    out = subprocess.run(cmd)
    print(out.returncode)
    #out.check_returncode()
    #out = subprocess.Popen(cmd)  # Spawn a new processes and continue

    if not out.returncode == 0:
        # If the previous attempt failed
        cmd = ["7z", "a", f"sub-{zm_id}_pre-{lab_visit}_wrb_zmax_{folder_name}.zip"]
        def find_edf(path):
            """ Recursively find any folders which contain a .hyp file """
            locations = []
            if os.path.isfile(path):
                return []
            if len([f for f in os.listdir(path) if f.endswith('.edf')]) > 0:
                locations.append(path)
            for d in os.listdir(path):
                new_path = os.path.join(path, d)
                if os.path.isdir(new_path):
                    locations += find_edf(new_path)
            return locations

        locations = find_edf(path)
        for l in locations:
            cmd.append(str(l))

        out = subprocess.run(cmd)
    return out.returncode

def zip_hypno_files(path, zm_id: str, lab_visit):
    """ Searchers recursively for the .hyp files and zips them into their own archive

    If there are .hyp files from multiple ZMax devices those should each be in their own subfolder
    and those subfolders will be zipped together
    """

    # Find out if the .hyp files exist in the cwd folder
    files = os.listdir(path)
    exist_at_cwd = False
    files_to_zip = []
    for f in files:
        if '.hyp' in f:
            files_to_zip.append(f)
            exist_at_cwd = True

    def find_hyp(path):
        """ Recursively find any folders which contain a .hyp file """
        locations = []
        if os.path.isfile(path):
            return []
        if len([f for f in os.listdir(path) if f.endswith('.hyp')]) > 0:
            locations.append(path)
        for d in os.listdir(path):
            new_path = os.path.join(path, d)
            if os.path.isdir(new_path):
                locations += find_hyp(new_path)
        return locations


    if not exist_at_cwd:
        # Find the folders in which the .hyp files exist
        locations = find_hyp(path)
        print(f".hyp files found in subfolders: {locations}")
        cmd = ['7z', 'a', f"sub-{zm_id}_pre-{lab_visit}_wrb_zmx_raw.zip", *locations]
    else:
        # Files exist separately in the root folder
        print(f'.hyp files found in root working directory: {path}')
        cmd = ['7z', 'a', f"sub-{zm_id}_pre-{lab_visit}_wrb_zmx_raw.zip", *files_to_zip]

    out = subprocess.run(cmd)
    out.check_returncode()
    return out.returncode

@click.command()
@click.option('--zm_id', prompt = 'ZMax ID', help='ZMax id.')
@click.option('--lab_visit', prompt='visit',
              help='Visit id')
def main(zm_id, lab_visit):

    path = os.getcwd()

    files_folders = os.listdir(cwd)
    folders_to_zip = list(map(str,[1,2,3,4,5,6,7]))

    for f in files_folders:
        if f in folders_to_zip:
            try:
                zip_folder_contents2(os.path.join(cwd, f), zm_id, lab_visit)
            except EmptyFolder as e:
                print(repr(e))
            except subprocess.CalledProcessError as e:
                print(repr(e))
    zip_hypno_files(path, zm_id, lab_visit)

    return


if __name__ == '__main__':
    cwd = os.getcwd()
    print('Current dir:', cwd)
    main()
