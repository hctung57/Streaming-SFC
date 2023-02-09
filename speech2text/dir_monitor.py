import time
import os


# NOTE: 
# - Assume: no removing files.

class DirMonitor: 
    def __init__(self,dir_home,pre,post,handler=lambda x:print(x),delay=0.15) -> None:
        self._dir_home=dir_home
        self._pre=pre
        self._post=post 
        self._handler=handler
        self._delay=delay
        self._pre_file_list=[]
       
    def listen(self):
        ind=0
        pre_mtime=0
        while True: 
            file=f"{self._pre}{ind}.{self._post}"
            file_path=os.path.join(self._dir_home,file)
            exists=os.path.exists(file_path) # TODO: optimize
            
            if not exists or not os.path.getsize(file_path) > 0:
                continue
            	
            print(f"[START PROCESS]: {self._pre}{ind}.{self._post}")
            ind+=1
            print(f"[PENDING]: {self._pre}{ind}.{self._post}")
            self._handler(file_path)