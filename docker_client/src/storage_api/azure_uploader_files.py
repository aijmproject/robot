from azure.storage.file import FileService
from azure.storage.file import ContentSettings
import os 
class AzureUploaderFiles:
    def __init__(self):
        self.account_name = "robotstockage"
        self.account_key = "x3KcC1YsGE037tA7/HgC24VHG3OA11fzURgu+CGz+MXoZKDrY+6pJwor5Dd1KhBQpXMk1Mr9rpTqP8MJe6VNsw=="
        self.file_service = FileService(account_name=self.account_name, account_key=self.account_key)
        self.intrusion_videos = "intrusionvideos"

    def show_all_files(self):
        generator = self.file_service.list_directories_and_files(self.intrusion_videos)
        for file_or_dir in generator:
            print(file_or_dir.name)

    def upload(self, input_file):
        print("create azure repo")
        self.file_service.create_share(self.intrusion_videos)

        file_name = os.path.splitext(os.path.basename(input_file))[0]
        print("file_name : ", file_name)
        self.file_service.create_file_from_path(
            self.intrusion_videos,
            None,  # We want to create this blob in the root directory, so we specify None for the directory_name
            file_name,
            input_file,
            content_settings=ContentSettings(content_type='video/mp4'))

if __name__ == "__main__":
    app  = AzureUploaderFiles()
    #app.upload("test.mp4")
    app.show_all_files()
    

