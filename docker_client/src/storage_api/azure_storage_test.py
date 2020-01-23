from azure.storage.file import FileService
from azure.storage.file import ContentSettings

print("connect to fileservice")
file_service = FileService(account_name='robotstockage', account_key='x3KcC1YsGE037tA7/HgC24VHG3OA11fzURgu+CGz+MXoZKDrY+6pJwor5Dd1KhBQpXMk1Mr9rpTqP8MJe6VNsw==')
print("create myshare")
file_service.create_share('myshare')
print("create directory in myshare")
file_service.create_directory('myshare', 'sampledir')
print("list files from myshare")
generator = file_service.list_directories_and_files('myshare')
for file_or_dir in generator:
    print(file_or_dir.name)


file_service.create_file_from_path(
    'myshare',
    None,  # We want to create this blob in the root directory, so we specify None for the directory_name
    'myfile',
    'sunset.jpg',
    content_settings=ContentSettings(content_type='image/jpg'))

file_service.get_file_to_path('myshare', None, 'myfile', 'out-sunset.jpg')