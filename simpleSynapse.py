# Imports
import os
import shutil
import pandas as pd
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
        self.syn.login(login, password)

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
    
    def create_synapse_dict(self):
        '''
        Create a dictionary for synapse folders and their ID's

        :param project_id: str, main synapse project ID
        return synapse_dict: dict, keys are synapse folder names and values are synapse id's
        '''
        synapse_dict={}
        for folder in self.syn.getChildren(self.project['id'],includeTypes=['folder']):
            synapse_dict[folder['name']]=folder['id']
            self.check_sub_folders(folder, synapse_dict)
        return synapse_dict
    
    def useless_file_removal(self, project_name):
        for path, subdirs, files in os.walk(project_name):
            if '.ipynb_checkpoints' in path.split('/'):
                shutil.rmtree(path)
            if 'SYNAPSE_METADATA_MANIFEST.tsv' in files:
                os.unlink(path+'/SYNAPSE_METADATA_MANIFEST.tsv')
    
    def file_search(self, project_name, synapse_dict):
        '''
        Search through a Synapse project directory tree to collect new file metadata and 
        export the data to a manifest tsv for a Synapse sync

        :param project_name: str, main synapse project name
        :param synapse_dict: dict, keys are synapse folder names and values are synapse id's
        return: None
        '''
        synapse_update = {'path': [], 'parent':[]}
        self.useless_file_removal(project_name)
        for path, subdirs, files in os.walk(project_name):
            if path != project_name:
                for name in files:
                    synapse_update['path'].append(os.path.join(path, name))
                    synapse_update['parent'].append(synapse_dict[path.split('/')[-1]])
        synapse_update_df = pd.DataFrame.from_dict(synapse_update)
        synapse_update_df.to_csv('manifest.tsv', sep='\t', index=False)
        
    def check_sub_folders(self, folder, synapse_dict):
        '''
        Check if a Synapse folder has sub folders

        :param folder: synapse generator object
        :param synapse_dict: dict, keys are synapse folder names and values are synapse id's
        return synapse_dict: dict, updated input synapse_dict
        '''
        # Recursion only checks the primary dirs not all in the parent folder
        sub_folder = [file for file in self.syn.getChildren(folder['id'], includeTypes=['folder'])]
        if sub_folder:
            for folder_dict in sub_folder:
                synapse_dict[folder_dict['name']] = folder_dict['id']
                self.check_sub_folders(folder_dict, synapse_dict)
        else:
            return synapse_dict
    
    def make_synapse_dirs(self, dir_list):
        '''
        Create a project directory tree and syncs to Synapse
        
        :param dir_list: str, list of user defined directory names
        '''
        for dir_names in dir_list:
            path = self.project['name'] + '/' + dir_names
            if not os.path.exists(path):
                os.makedirs(path)
        synapseutils.sync.syncFromSynapse(self.syn, self.project['id'], path=self.project['name'])
        
    
    def synapse_removal(self, removal_list):
        '''
        Remove an object from Synase
        
        :param: str list, list of user defined file or directory names
        '''
        for file_name in removal_list:
            self.syn.delete(file_name)

    def sync_synapse_to_local(self):
        '''
        Sync Synapse to local
        
        :param: None
        return: None
        '''
        if not os.path.exists(self.project['name']): 
            os.makedirs(self.project['name'])
        synapseutils.sync.syncFromSynapse(self.syn, self.project['id'], path=self.project['name'])
        
        
    def sync_local_to_synapse(self):
        '''
        Syn local to synapse
        
        :param: None
        return: None
        '''
        synapse_dict = self.create_synapse_dict()
        self.file_search(self.project['name'], synapse_dict)
        synapseutils.sync.syncToSynapse(self.syn, 'manifest.tsv')
