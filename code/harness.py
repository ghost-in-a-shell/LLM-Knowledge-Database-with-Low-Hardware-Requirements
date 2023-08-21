import numpy as np
import variables
import utils
import fileloader_splitter
import embedding_saving
import llm_agent
use_existing_data = utils.use_existing_data()

if not use_existing_data:
    utils.clear_folder(variables.CHROMADB_PATH)
    utils.clear_folder(variables.FILEARRAY_PATH)

    split_filename=fileloader_splitter.fileloader_splitter(variables.SRCFILE_PATH)
    splits=np.load(split_filename, allow_pickle=True)

    embedding_saving.embedding_saving(splits)
else:
    split_filename=utils.get_npy(variables.FILEARRAY_PATH)
llm_agent.llm_agent_start(split_filename,variables.POE_BOT)
