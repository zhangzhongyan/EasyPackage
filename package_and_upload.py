import os
import shutil
import zipfile
import requests

def package_app(app_path):
    # 1. 确保 .app 文件存在
    if not os.path.exists(app_path) or not app_path.endswith('.app'):
        print(f"Error: {app_path} is not a valid .app file.")
        return
    
    # 2. 创建 Payload 文件夹
    payload_dir = 'Payload'
    if os.path.exists(payload_dir):
        shutil.rmtree(payload_dir)
    os.makedirs(payload_dir)
    
    # 3. 将 .app 文件复制到 Payload 文件夹
    shutil.copytree(app_path, os.path.join(payload_dir, os.path.basename(app_path)))
    
    # 4. 将 Payload 文件夹压缩为 Payload.zip
    zip_filename = 'Payload.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(payload_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, payload_dir))
    
    # 5. 将 Payload.zip 重命名为 Payload.ipa
    ipa_filename = 'Payload.ipa'
    if os.path.exists(ipa_filename):
        os.remove(ipa_filename)
    os.rename(zip_filename, ipa_filename)
    
    print(f"Successfully packaged {app_path} to {ipa_filename}")
    return ipa_filename

def upload_to_pgyer(ipa_path, api_key, user_key):
    upload_url = "https://www.pgyer.com/apiv2/app/upload"
    
    data = {
        '_api_key': api_key,
        'userKey': user_key,
    }
    
    files = {
        'file': open(ipa_path, 'rb')
    }
    
    print(f"Uploading {ipa_path} to Pgyer...")
    response = requests.post(upload_url, data=data, files=files)
    
    if response.status_code == 200:
        print("Upload successful!")
        print("Response:", response.json())
    else:
        print("Upload failed!")
        print("Response:", response.text)

if __name__ == "__main__":
    # 替换为你的 .app 文件路径
    app_file_path = '/Users/zhangzhongyan/Library/Developer/Xcode/DerivedData/Fargo-fbvqwegpsgdlafcydsvfrzlbahtd/Build/Products/Debug-iphoneos/Fargo.app'
    
    # 替换为你的蒲公英 API Key 和 User Key
    api_key = 'fc870539ca92797712cc0ac863fb30ac'
    user_key = '56ee6b6db5c5655c5902d6f9bdfae9be'
    
    # 执行打包操作
    ipa_file = package_app(app_file_path)
    
    if ipa_file:
        # 上传到蒲公英
        upload_to_pgyer(ipa_file, api_key, user_key)
