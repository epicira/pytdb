import json
import PyIraCluster
from typing import Union
from PyIraCluster import TdbOpen, TdbSelect, TdbExec, TdbCount, TdbClose, TdbExecAsync


class TDB():
    def __init__(self, 
        cluster_id: str, 
        privacy_level: PyIraCluster.privacy = PyIraCluster.privacy.none, 
        public_key: str = "", 
        private_key: str = "",
        publish_changes: bool = True
        ):

        self.cluster_id = cluster_id
        self.privacy_level = privacy_level
        self.public_key = public_key
        self.private_key = private_key
        self.publish_changes = publish_changes

    def open(self, database_name: str, init_query: str = "", index_query: str = ""):
        self.database_name = database_name
        TdbOpen(
            self.cluster_id, self.database_name, self.privacy_level, 
            init_query, index_query,
            self.public_key, self.private_key)
        
        return self

    def select(self, query: str):
        response = json.loads(TdbSelect(self.cluster_id, self.database_name, query))
        return response
    
    def execute(self, query: str, publish_changes: Union[bool, None] = None):
        return TdbExec(self.cluster_id, self.database_name, query, 
            self.publish_changes if publish_changes is None else publish_changes
        )

    def execute_async(self, query: str, publish_changes: Union[bool, None] = None, execute_after: int = 0):
        """
        You cannot set callback for this function.
        execute_after accepts integer (in milliseconds)
        """
        return TdbExecAsync(
            self.cluster_id, self.database_name, query, 
            self.publish_changes if publish_changes is None else publish_changes,
            execute_after
        )

    def count(self, table_name: str, where_clause: str = ""):
        return TdbCount(self.cluster_id, self.database_name, table_name, where_clause)

    def destroy_local(self):
        return TdbClose(self.cluster_id, self.database_name)
