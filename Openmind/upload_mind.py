from openmind_hub import upload_folder
    # token：对目标仓库具有可写权限的访问令牌，必选。
    # folder_path：要上传的本地文件夹的路径，必选。
    # repo_id：目标仓库，必选。
    # 若需对上传的文件类型进行过滤，可以使用allow_patterns和ignore_patterns参数，详见upload_folder。
upload_folder(
    token="***",
    folder_path="models/UniVaR-lambda-5",
    repo_id="jeffding/UniVaR-lambda-5-openmind",
)