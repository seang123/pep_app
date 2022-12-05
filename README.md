# PEP app

Reading PEP id's and other Pseudo id's for HBS


## Zipping files

- Requires files to be located on the desktop in a folder called __ZMax_temporary__.
- Should have sub-folders labled 1-7
- The extraced files should be placed in their respective sub-folder (name refers to day)
  - If a day has recordings from more than one data-file, these should be placed in sub-folders within the day folder
  - If the files come from different Zmax's, name the sub-folders after the device id otherwise 'a', 'b', ... also works.
- The raw data files should be stored at the top-level in the ZMax_temporary folder.

```
Desktop
|-- ZMax_temporary
|   |-- 1
|   |   +-- *.edf 
|   |-- 2
|   |   |-- Zmax19
|   |   |-- Zmax20
|   |-- 3
|   |   |-- A
|   |   |-- B
|   |-- 4
|   |-- 5
|   |-- 5
|   |-- 6 
|   |-- 7
|   +-- hypno1.hyp
|   +-- hypno2.hyp
|   ...
```

## Empatica duration

- The downloaded empatica data files should be stored in a folder on the desktop called __Empatica_temporary__

#### Requirements

- Python >=3.8
- Access to the S:\\ drive
- For the zipping (7-Zip cli tool in the path)


# TODO

- [x] handle zip_files.py edge case for when extracted files are in nested directory (in the case
that two sets of data exist for a single date)
- [x] Add information from planner tool
- [x] fixed bug where multiple entries for same lab visit in PT caused failure to get Ra/slot/data
- [x] Add Activpal file rename button
- [ ] Add button to open empatica.com/connect website
- [ ] Add logging 
- [ ] Refactor each frame into its own class/module