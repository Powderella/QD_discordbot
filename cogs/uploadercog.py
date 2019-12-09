from discord.ext import commands, tasks
import shutil
import filecmp
import dropbox
from settings import LOCAL_PATH_DBFILE, LOCAL_PATH_DBFOLDER, PATH_DROPBOX, DROPBOX_TOKEN, UPLOAD_LOOP_TIME

class UploaderCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dbx = dropbox.Dropbox(DROPBOX_TOKEN)
        self.dbx.users_get_current_account()
        self.uploadDBLoop.start()
    
    def cog_unload(self):
        self.uploadDBLoop.cancel()
    
    @tasks.loop(minutes=UPLOAD_LOOP_TIME)
    async def uploadDBLoop(self):
        shutil.make_archive(LOCAL_PATH_DBFOLDER, "zip", LOCAL_PATH_DBFOLDER)

        with open(LOCAL_PATH_DBFILE, "rb") as f:
            self.dbx.files_upload(f.read(), PATH_DROPBOX, mode=dropbox.files.WriteMode('overwrite'))
        print("DBFILE UPLOAD COMPLETE")

    @uploadDBLoop.before_loop
    async def beforeUploadDBLoop(self):
        await self.bot.wait_until_ready()
def setup(bot):
    bot.add_cog(UploaderCog(bot))