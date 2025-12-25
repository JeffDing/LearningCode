import os

def rename_file(folder_path,old_file_name):
    # 核心配置：替换为你的目标文件夹路径
    target_folder = folder_path

    # 校验文件夹路径是否有效
    if not os.path.exists(target_folder):
        print(f"错误：文件夹路径 {target_folder} 不存在，请检查路径是否正确")
        exit()

    # 按文件最后修改时间升序排序（最早修改的文件编号靠前）
    file_list = sorted(
        [f for f in os.listdir(target_folder) if os.path.isfile(os.path.join(target_folder, f))],
        key=lambda x: os.path.getmtime(os.path.join(target_folder, x))
    )

    # 批量重命名逻辑
    for index, file_name in enumerate(file_list, start=1):
        # 获取文件后缀（含.），无后缀则为空
        file_suffix = os.path.splitext(file_name)[1]
        # 生成新文件名：
        new_file_name = f"{old_file_name}_{index}{file_suffix}"
        # 拼接原文件完整路径和新文件完整路径
        old_path = os.path.join(target_folder, file_name)
        new_path = os.path.join(target_folder, new_file_name)
        # 执行重命名
        os.rename(old_path, new_path)
        print(f"已重命名：{file_name} → {new_file_name}")

    print("批量重命名完成！")

if __name__ == "__main__":
    # 使用示例
    folder_path = input("请输入文件夹名字:").strip()
    old_file_name = input("请文件夹前缀: ").strip()
    rename_file(folder_path,old_file_name)