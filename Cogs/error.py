import interactions
from interactions import *
from interactions import extension_listener as listener







class Error(interactions.Extension):
    def __init__(self, client):
        self.client = client
    
    @listener()
    async def 
