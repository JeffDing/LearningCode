import os

def rename_file(folder_path, old_file_name, start_number):
    # 校验文件夹路径是否有效
    if not os.path.exists(folder_path):
        print(f"错误：文件夹路径 {folder_path} 不存在，请检查路径是否正确")
        return  # 使用 return 代替 exit()，避免程序直接退出

    # 按文件最后修改时间升序排序（最早修改的文件编号靠前）
    file_list = sorted(
        [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))],
        key=lambda x: os.path.getmtime(os.path.join(folder_path, x))
    )

    # 批量重命名逻辑
    for index, file_name in enumerate(file_list, start=start_number):
        # 获取文件后缀（含.），无后缀则为空
        file_suffix = os.path.splitext(file_name)[1]
        # 生成新文件名：
        new_file_name = f"{old_file_name}_{index}{file_suffix}"
        # 拼接原文件完整路径和新文件完整路径
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_file_name)
        # 执行重命名
        os.rename(old_path, new_path)
        print(f"已重命名：{file_name} → {new_file_name}")

    print("批量重命名完成！")

if __name__ == "__main__":
    # 使用示例
    folder_path = input("请输入文件夹路径: ").strip()
    old_file_name = input("请输入文件名前缀: ").strip()
    start_number = int(input("请输入起始编号: ").strip())

    rename_file(folder_path, old_file_name, start_number)