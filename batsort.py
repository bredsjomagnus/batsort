from distutils.log import error
from errno import EROFS
import pandas as pd
import os
import glob
from loggingconfig import *
import pprint
pp = pprint.PrettyPrinter(indent=4)
from functions import *
import shutil


str_date_time = get_date_str("%Y%m%d_%H_%M_%S")

this_path = os.getcwd()

def main():
    
    df = pd.read_csv('batfil.csv')

    unique_sorts = get_unique_sorts(df, 'Contains')
    
    bat_dict = get_sorts_in_dict(unique_sorts, df, 'Contains', 'File name')
    
    try:
        os.mkdir(this_path+"/batcategories")
    except FileExistsError:
        logging.info("Mappen /batcaterories behövdes inte skapas.")

    for folder_name in unique_sorts:
        path = os.path.join(this_path+"/batcategories", folder_name) 
        try:
            os.mkdir(path)
        except:
            pass
        
    wav_files= glob.glob('batsounds/*.wav')

    wav_files = [file_path[10:] for file_path in wav_files]
    
    logg_content:dict = {}
    error_content:dict = {}
    for key, values in bat_dict.items():
        for value in values:
            if value in wav_files:
                this_file_path = this_path+"/batsounds/"+value
                to_file_path = this_path+"/batcategories/"+key+"/"+value

                try:
                    shutil.copyfile(this_file_path, to_file_path)
                    logging.info("{} --> {}".format(value, key))

                    if key in logg_content:
                        logg_content[key].append(value)
                    else:
                        logg_content[key] = []
                        logg_content[key].append(value)
                    
                except Exception as e:
                    logging.warning("Kunde inte kopiera {} --> {}".format(value, key))
                    
                    if key in error_content:
                        error_content[key].append(value)
                    else:
                        error_content[key] = []
                        error_content[key].append(value)

    try:
        if len(logg_content) > 0:
            logg_content = prepare_dict_for_df(logg_content)
            logg_df = pd.DataFrame.from_dict(logg_content)
            logg_df.to_csv("batsortlogg_"+str_date_time+".csv", sep=";", index=0)
    except:
        logging.warning("Kunde inte skapa batsortlogg "+str_date_time+".csv")

    try:
        if len(error_content) > 0:
            error_content = prepare_dict_for_df(error_content)
            err_df = pd.DataFrame.from_dict(error_content)
            err_df.to_csv("baterror_logg_"+str_date_time+".csv", sep=";", index=0)
    except:
        logging.warning("Kunde inte skapa baterror_logg"+str_date_time+".csv")

if __name__ == '__main__':
    logging.info("Start sortsounds")
    main()