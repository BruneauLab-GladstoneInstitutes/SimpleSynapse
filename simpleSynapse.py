import os
import shutil
import hashlib
import synapseclient
import synapseutils
from synapseclient import Project, Folder, File, Link

class SimpleSynapse(object):
    """
    A class used to organize and sync a Synapse project. 
    
    Attributes
    ----------
    login : str
        Synapse username
    password : str
        Synapse password
    project : str
        Synapse project name
    
    Methods
    -------
    create_synapse_dict()
        Create a dictionary for Synapse folders and their ID's
        
    file_search(project_name, synapse_dict)
        Search through a Synapse project directory tree to collect new file metadata and 
        export the data to (a manifest tsv for a Synapse sync
        
    check_sub_folders(folder, synapse_dict)
        Check if a Synapse folder has sub folders
        
    make_synapse_dirs(dir_list)
        Create a project directory tree and syncs to Synapse
        
    sync_synapse_to_local()
        Sync Synapse to local
        
    sync_local_to_synapse()
        Syn local to synapse
        
    References
    -------
    https://python-docs.synapse.org/
    """
    
    def __init__(self, login, password, project):
        
        self.syn = synapseclient.Synapse()
        self.syn.login(login, password, forced=True)

        self.project = Project(project)
        self.project = self.syn.store(self.project)
    
    def syn_client(self):
        '''
        Construct a Python client object for the Synapse repository service
        
        :param: None
        return: Synapse client constructor
        '''
        return self.syn
    
    def syn_project(self):
        '''
        Construct a Python client for the Synapse project
        
        :param: None
        return: Synapse project constructor
        '''
        return self.project
    
    def sync_synapse_to_local(self):
        '''
        Sync Synapse to local
        
        :param: None
        return: None
        '''
        if not os.path.exists(self.project['name']): 
            os.makedirs(self.project['name'])
        synapseutils.sync.syncFromSynapse(self.syn, self.project['id'], path=self.project['name'], ifcollision="keep.local")
    
    def file_store(self, file_path, parent_path):
        file = File(file_path, parent=parent_path)
        file = self.syn.store(file)
    
    def check(self):
        synapse_folder_dict = {self.project.name :self.project.id}
        synapse_file_dict = {}
        for paths, subdirs, files in os.walk(self.project.name):
            if subdirs:
                for dirs in subdirs:
                    if dirs == '.ipynb_checkpoints':
                        shutil.rmtree(paths + '/' + dirs)
                    else:
                        dir_entityID = self.syn.findEntityId(dirs, parent=synapse_folder_dict[paths.split('/')[-1]])
                        if dir_entityID is not None:
                            synapse_folder_dict[dirs] = dir_entityID
                        else:
                            folder = Folder(dirs, parent=synapse_folder_dict[paths.split('/')[-1]])
                            folder = self.syn.store(folder)
                            synapse_folder_dict[folder.name] = folder.id
            if files:
                for data in files:
                    if data == 'SYNAPSE_METADATA_MANIFEST.tsv':
                        os.unlink(paths + '/' + data)
                    else:
                        file_entityID = self.syn.findEntityId(data, parent=synapse_folder_dict[paths.split('/')[-1]])
                        if file_entityID is not None:
                            file_entity = self.syn.get(file_entityID, downloadFile=False)
                            local_md5 = synapseclient.utils.md5_for_file(paths + '/' + data).hexdigest()
                            if file_entity.md5 != local_md5:
                                self.file_store(paths + '/' + data, synapse_folder_dict[paths.split('/')[-1]])
                        else:
                            self.file_store(paths + '/' + data, synapse_folder_dict[paths.split('/')[-1]])