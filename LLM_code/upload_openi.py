from openmind_hub import set_platform, create_repo, upload_folder, snapshot_download
set_platform("openi")
model_name="***"
token = "***"
create_repo(repo_id=model_name, token=token)
upload_folder(repo_id=model_name, folder_path="models/UniVaR-lambda-5", token=token)