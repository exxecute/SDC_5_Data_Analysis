import os

DEFAULT_DIRECTORY: str = "./../report"
MAIN_DOC: str = "/README.md"

MAIN_POINTS_DIR: str = "/main_points"

BASIC_STAT_DIR: str = MAIN_POINTS_DIR + "/basic_stat"
BASIC_STAT_DOC: str = BASIC_STAT_DIR + MAIN_DOC

DATA_SHAPE_DIR: str = MAIN_POINTS_DIR + "/data_shape"
DATA_SHAPE_DOC: str = DATA_SHAPE_DIR + MAIN_DOC

DATA_TYPES_DIR: str = MAIN_POINTS_DIR + "/data_types"
DATA_TYPES_DOC: str = DATA_TYPES_DIR + MAIN_DOC

UNIQ_DATA_DIR: str = MAIN_POINTS_DIR + "/uniq_data"
UNIQ_DATA_DOC: str = UNIQ_DATA_DIR + MAIN_DOC

UNIQ_COUNT_DIR: str = MAIN_POINTS_DIR + "/uniq_count"
UNIQ_COUNT_DOC: str = UNIQ_COUNT_DIR + MAIN_DOC

SIMPLE_FILT_DIR: str = MAIN_POINTS_DIR + "/simple_filtering"
SIMPLE_FILT_DOC: str = SIMPLE_FILT_DIR + MAIN_DOC

PIVOT_TAB_DIR: str = "/pivot_tables"

PIVOT_TABLES_DIR: str = PIVOT_TAB_DIR + "/pivot_tables"
PIVOT_TABLES_DOC: str = PIVOT_TABLES_DIR + MAIN_DOC

FREQ_HEATMAP_DIR: str = PIVOT_TAB_DIR + "/frequency_heatmap"
FREQ_HEATMAP_DOC: str = FREQ_HEATMAP_DIR + MAIN_DOC

class ReportGenerator:
    def __init__(self):
        self.__createDirectory("")
        self.__createDirectory(MAIN_POINTS_DIR)
        self.__createDirectory(BASIC_STAT_DIR)
        self.__createDirectory(DATA_SHAPE_DIR)
        self.__createDirectory(DATA_TYPES_DIR)
        self.__createDirectory(UNIQ_DATA_DIR)
        self.__createDirectory(UNIQ_COUNT_DIR)
        self.__createDirectory(SIMPLE_FILT_DIR)
        self.__createDirectory(PIVOT_TAB_DIR)
        self.__createDirectory(PIVOT_TABLES_DIR)
        self.__createDirectory(FREQ_HEATMAP_DIR)

        self.__createFile(MAIN_DOC,         "Main")
        self.__writeToMain(               "- Main points. Introduction")
        self.__createFile(BASIC_STAT_DOC,   "Basic Statistic")
        self.__createFile(DATA_SHAPE_DOC,   "Data Shape")
        self.__createFile(DATA_TYPES_DOC,   "Data Types")
        self.__createFile(UNIQ_DATA_DOC,    "Count of Unique Values")
        self.__createFile(UNIQ_COUNT_DOC,   "Value Counts")
        self.__createFile(SIMPLE_FILT_DOC,  "Simple Filtering")
        self.__writeToMain(               "- Pivot Table")
        self.__createFile(PIVOT_TABLES_DOC, "Pivot Tables")
        self.__createFile(FREQ_HEATMAP_DOC, "Frequency Heatmap")

    def __createDirectory(self, directory: str):
        directory = DEFAULT_DIRECTORY + directory
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory '{directory}' created successfully.")
        else:
            print(f"Directory '{directory}' already exists.")

    def __createFile(self, file_path: str, name: str):
        file_path = DEFAULT_DIRECTORY + file_path
        with open(file_path, 'w') as file:
            print(f"File '{file_path}' created successfully.")
            file.write("# " + name + "\n\n")
        if file_path == (DEFAULT_DIRECTORY + MAIN_DOC): return
        else: 
            with open(file_path, 'a') as file: file.write("[<- Back](./../../README.md)\n")
        with open(DEFAULT_DIRECTORY + MAIN_DOC, "a") as file:
            file.write("   - [{name}]({file_path})\n".format(name=name, file_path=file_path))

    def __writeToMain(self, string: str):
        with open(DEFAULT_DIRECTORY + MAIN_DOC, "a") as file:
            file.write(string + "\n")

    def addBasicStatistic(self, statistic: str):
        with open(DEFAULT_DIRECTORY + BASIC_STAT_DOC, 'a') as file:
            file.write(statistic + '\n')

    def addDataShape(self, statistic: str, shape: str):
        with open(DEFAULT_DIRECTORY + DATA_SHAPE_DOC, 'a') as file:
            file.write("- number of rows and columns" + shape)
            file.write("\n```sh")
            file.write(statistic)
            file.write("\n```")

    def addDataTypes(self, statistic: str):
        with open(DEFAULT_DIRECTORY + DATA_TYPES_DOC, 'a') as file:
            file.write("\n```sh")
            file.write(statistic)
            file.write("\n```")

    def addUniqData(self, statistic: str):
        with open(DEFAULT_DIRECTORY + UNIQ_DATA_DOC, 'a') as file:
            file.write(statistic)

    def addUnicCounts(self, col: str, statistic: str):
        with open(DEFAULT_DIRECTORY + UNIQ_COUNT_DOC, 'a') as file:
            file.write(f"\n\n- Частоты категорий в столбце '{col}':")
            file.write("\n```sh")
            file.write(statistic)
            file.write("\n\n```")

    def addSimpleFiltering(self, name:str, statistic: str):
        with open(DEFAULT_DIRECTORY + SIMPLE_FILT_DOC, 'a') as file:
            file.write(f"\n{name}")
            file.write("\n```sh\n")
            file.write(statistic)
            file.write("\n\n```\n")

    def addPivotTable(self, name:str, statistic: str):
        with open(DEFAULT_DIRECTORY + PIVOT_TABLES_DOC, 'a') as file:
            file.write(f"\n{name}")
            file.write("\n```sh\n")
            file.write(statistic)
            file.write("\n\n```\n")

    def getFreqHeatmapPlace(self) -> str:
        PICTURE_NAME: str = "/heatmap.png"
        PICTURE_PATH: str = DEFAULT_DIRECTORY+ FREQ_HEATMAP_DIR + PICTURE_NAME
        with open(DEFAULT_DIRECTORY + FREQ_HEATMAP_DOC, 'a') as file:
            file.write(f"![heatmap](.{PICTURE_NAME})")
        return PICTURE_PATH