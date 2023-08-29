import numpy as np
import variables
import utils
import fileloader_splitter
import embedding_saving
import llm_agent
use_existing_data = utils.use_existing_data()

def startover():
    utils.clear_folder(variables.CHROMADB_PATH)
    utils.clear_folder(variables.FILEARRAY_PATH)

    split_filename=fileloader_splitter.fileloader_splitter(variables.SRCFILE_PATH)
    splits=np.load(split_filename, allow_pickle=True)

    embedding_saving.embedding_saving(splits)
    return split_filename

if not use_existing_data:
    update_data=utils.use_update_mode()
    if update_data:
        extra,missing=utils.compare_filelist(variables.SRCFILE_PATH,variables.COOKIE_PATH)
        if len(missing)==0:
            splits_add,l_add,split_filename=fileloader_splitter.updatesplits(extra,missing)
            embedding_saving.update_db(splits_add,l_add)
        else:
            split_filename=startover()
    else:
        split_filename=startover()
else:
    split_filename=utils.get_npy(variables.FILEARRAY_PATH)
llma=llm_agent.llm_agent(split_filename,variables.POE_BOT)
llma.run()
