import os
import math
import signal
import shutil
import subprocess
import zipfile
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import configparser  # 导入 configparser

import psutil
from flask import Flask, request, jsonify, render_template, redirect, session, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import chardet

app = Flask(__name__)
CORS(app)

# 加载配置文件
config = configparser.ConfigParser()
CONFIG_FILE = 'server_config.ini'
CONFIG_TEMPLATE_FILE = 'server_config.ini.template'

if not os.path.exists(CONFIG_FILE):
    # 如果配置文件不存在，从模板复制一份并提示用户配置
    shutil.copyfile(CONFIG_TEMPLATE_FILE, CONFIG_FILE)
    print(f"配置文件 '{CONFIG_FILE}' 不存在，已创建默认配置文件。请编辑 '{CONFIG_FILE}' 文件来配置服务器路径和密码。")
    exit()  # 或者可以选择继续运行，但使用模板中的默认值

config.read(CONFIG_FILE)

# 从配置文件读取配置项
CONFIG_FILE_PATH = config.get('Paths', 'config_file_path')
SERVER_EXECUTABLE = config.get('Paths', 'server_executable')
UPLOAD_FOLDER = config.get('Paths', 'upload_folder')
NETWORK_LOG_FILE = config.get('Paths', 'network_log_file')
DAILY_USAGE_FILE = config.get('Paths', 'daily_usage_file')

SECRET_PASSWORD = config.get('Security', 'secret_password') # 从配置文件读取默认密码
# 密码哈希 - **注意顺序，bcrypt = Bcrypt(app) 必须在前面**
bcrypt = Bcrypt(app)  #  <----  bcrypt 实例在这里创建
hashed_password = bcrypt.generate_password_hash(SECRET_PASSWORD).decode('utf-8') # 初始化时生成哈希密码

SERVER_PORT = config.getint('Server', 'server_port') # 读取端口号
LOG_LEVEL_STR = config.get('Server', 'log_level').upper() # 读取日志级别并转换为大写
LOG_FILE = config.get('Server', 'log_file') # 日志文件路径

ALLOWED_EXTENSIONS = {'zip'}
MAX_FILE_SIZE = 1024 * 1024 * 50  # 50 MB

# 日志配置 (从配置文件读取日志级别和文件名)
log_level_map = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}
log_level = log_level_map.get(LOG_LEVEL_STR, logging.INFO) # 默认 INFO

handler = RotatingFileHandler(LOG_FILE, maxBytes=10000, backupCount=5)
handler.setLevel(log_level)
app.logger.addHandler(handler)
app.logger.info(f"Web application started with log level: {LOG_LEVEL_STR}")

# 网络使用情况跟踪 (路径从配置读取)
last_network_stats = None


def get_server_pid():
    pid_file = "/tmp/server.pid"
    try:
        with open(pid_file, "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return None

def is_server_running():
    pid = get_server_pid()
    if pid:
        return psutil.pid_exists(pid)
    return False

def get_network_stats():
    global last_network_stats
    current_stats = psutil.net_io_counters()
    now = datetime.now()

    total_sent = get_cumulative_network_usage('sent')
    total_received = get_cumulative_network_usage('received')

    if last_network_stats:
        time_diff = (now - last_network_stats['time']).total_seconds()
        sent_diff = current_stats.bytes_sent - last_network_stats['stats'].bytes_sent
        received_diff = current_stats.bytes_recv - last_network_stats['stats'].bytes_recv

        current_sent_speed = (sent_diff / time_diff) if time_diff > 0 else 0
        current_received_speed = (received_diff / time_diff) if time_diff > 0 else 0
    else:
        current_sent_speed = 0
        current_received_speed = 0

    last_network_stats = {'stats': current_stats, 'time': now}
    return {
        'total_sent': total_sent,
        'total_received': total_received,
        'current_sent_speed': current_sent_speed,
        'current_received_speed': current_received_speed
    }

def get_cumulative_network_usage(direction):
    try:
        with open(NETWORK_LOG_FILE, 'r') as f:
            for line in f:
                if direction in line:
                    return int(line.split('=')[1])
    except FileNotFoundError:
        return 0
    return 0

def update_cumulative_network_usage(sent, received):
    total_sent = get_cumulative_network_usage('sent') + sent
    total_received = get_cumulative_network_usage('received') + received
    with open(NETWORK_LOG_FILE, 'w') as f:
        f.write(f"sent={total_sent}\n")
        f.write(f"received={total_received}\n")

def record_daily_usage(sent, received):
    today = datetime.now().strftime('%Y-%m-%d')
    daily_data = load_daily_usage()
    if today in daily_data:
        daily_data[today]['sent'] += sent
        daily_data[today]['received'] += received
    else:
        daily_data[today] = {'sent': sent, 'received': received}
    save_daily_usage(daily_data)

def load_daily_usage():
    try:
        with open(DAILY_USAGE_FILE, 'r') as f:
            import json
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_daily_usage(data):
    with open(DAILY_USAGE_FILE, 'w') as f:
        import json
        json.dump(data, f)

def get_daily_usage_history():
    data = load_daily_usage()
    history = [{'date': date, 'sent': usage['sent'], 'received': usage['received']} for date, usage in data.items()]
    history.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    return history

def get_server_resource_usage():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    return {
        'cpu_usage': cpu_usage,
        'memory_percent': memory_percent,
        'running': is_server_running()
    }

# ---------------------  辅助函数  ---------------------
def read_config():
    config_items = {}
    try:
        with open(CONFIG_FILE_PATH, 'r') as file:
            for line in file:
                key, value = line.strip().partition('=')[::2]
                config_items[key.strip()] = value
    except FileNotFoundError:
        return {}
    return config_items

def write_config(config_items):
    with open(CONFIG_FILE_PATH, 'w') as file:
        for key, value in config_items.items():
            file.write(f"{key}={value}\n")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_folder_size(path):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_folder_size(entry.path)
    return total

def format_bytes(bytes, decimals=2):
    if bytes is None:
        return "0 Bytes"
    k = 1024
    dm = 0 if decimals < 0 else decimals
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = int(math.floor(math.log(bytes, k))) if bytes else 0
    return f"{float(bytes / math.pow(k, i)):.{dm}f} {sizes[i]}"


def extract_with_detected_encoding(zip_path, extract_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                try:
                    bytes_name = member.encode('cp437')
                    detected_encoding = chardet.detect(bytes_name)['encoding']
                    if detected_encoding:
                      if detected_encoding.lower() in ["gbk","gb2312"]:
                          decoded_member = bytes_name.decode(detected_encoding,"ignore").encode("utf-8").decode("utf-8","ignore")
                          zip_ref.extract(member, extract_path)
                          os.rename(os.path.join(extract_path,member),os.path.join(extract_path,decoded_member))
                      else:
                        decoded_member = bytes_name.decode(detected_encoding,"ignore")
                        zip_ref.extract(member, extract_path)
                        os.rename(os.path.join(extract_path,member),os.path.join(extract_path,decoded_member))

                    else:
                        zip_ref.extract(member, extract_path)
                except Exception as e:
                     print(f"检测编码出错:{e}")
                     zip_ref.extract(member, extract_path) #默认解压
    except zipfile.BadZipFile:
         return "BadZipFile"
    except Exception as e:
         print(f"解压出错:{e}")
         return "OtherError"
    return "success"

# ---------------------  路由  ---------------------
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect('/login')
    config_items = read_config()
    return render_template('config.html', config=config_items)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if bcrypt.check_password_hash(hashed_password, password):
            session['logged_in'] = True
            app.logger.info("Login successful") # 登录成功日志
            return redirect('/')
        else:
            app.logger.warning("Login failed due to incorrect password") # 登录失败日志
            return '密码错误', 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    app.logger.info("User logged out") # 登出日志
    return redirect('/login')

@app.route('/update-config', methods=['POST'])
def update_config():
    try:
        config_items = request.form.to_dict()
        write_config(config_items)
        app.logger.info("Configuration updated") # 配置更新日志
        return jsonify({'message': '配置已更新'}), 200
    except Exception as e:
        app.logger.error(f"Error updating config: {str(e)}") # 配置更新失败日志
        return jsonify({'error': str(e)}), 500

@app.route('/upload-map', methods=['POST'])
def upload_map():
    if 'file' not in request.files:
        app.logger.warning("No file part in upload request") # 无文件上传日志
        return jsonify({"error": "没有文件上传"}), 400
    file = request.files['file']
    if file.filename == '':
        app.logger.warning("No filename in upload request") # 无文件名日志
        return jsonify({"error": "没有选择文件"}), 400
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        file.save(file_path)
        sent_bytes = os.path.getsize(file_path)  # 获取上传文件大小
        update_cumulative_network_usage(sent_bytes, 0) # 更新累计上传
        record_daily_usage(sent_bytes, 0) # 记录到每日流量
        result = extract_with_detected_encoding(file_path,UPLOAD_FOLDER)
        if result == "success":
            app.logger.info(f"File {file.filename} uploaded and extracted successfully") # 上传解压成功日志
            return jsonify({"message": f"文件 {file.filename} 已上传并解压"}), 200
        elif result =="BadZipFile":
            os.remove(file_path) # 删除无效的 zip 文件
            app.logger.warning(f"Uploaded file {file.filename} is not a valid zip file") # 无效 zip 日志
            return jsonify({"error": "上传的文件不是有效的zip文件"}), 400
        else:
            os.remove(file_path) # 删除解压出错的文件
            app.logger.error(f"Error extracting {file.filename}") # 解压错误日志
            return jsonify({"error": "解压出错"}), 500
    except Exception as e:
        app.logger.error(f"File upload error: {str(e)}") # 文件上传错误日志
        return jsonify({"error": str(e)}), 500


@app.route('/check-file', methods=['POST'])
def check_file():
    data = request.get_json()
    filename = data.get('filename')
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return jsonify({'exists': True}), 200
    else:
        return jsonify({'exists': False}), 200

@app.route('/unzip-map', methods=['POST'])
def unzip_map():
    data = request.get_json()
    filename = data.get('filename')
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    result = extract_with_detected_encoding(file_path,UPLOAD_FOLDER)
    if result == "success":
      return jsonify({"message": f"文件 {filename} 解压完成"}), 200
    elif result =="BadZipFile":
      return jsonify({"error": "上传的文件不是有效的zip文件"}), 400
    else:
       return jsonify({"error": "解压出错"}), 500

@app.route('/files', methods=['GET'])
def list_files():
    try:
        files_list = os.listdir(UPLOAD_FOLDER)
        files_info = []
        for f in files_list:
            file_path = os.path.join(UPLOAD_FOLDER, f)
            if os.path.isdir(file_path):
                total_size = get_folder_size(file_path)
                formatted_size = format_bytes(total_size)
                files_info.append({
                    'name': f,
                    'size': formatted_size
                })
            else:
                file_size = os.path.getsize(file_path)
                files_info.append({
                    'name': f,
                    'size': format_bytes(file_size)
                })
        return jsonify(files_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/control-server", methods=["POST"])
def control_server():
    action = request.json.get("action", "")
    pid_file = "/tmp/server.pid"

    if action == "start":
        if is_server_running():
            return jsonify({"message": "服务器已在运行"}), 200

        process = subprocess.Popen([SERVER_EXECUTABLE])
        with open(pid_file, "w") as f:
            f.write(str(process.pid))
        app.logger.info("服务器已启动")
        return jsonify({"message": "服务器已启动"}), 200

    elif action == "stop":
        pid = get_server_pid()
        if pid:
            try:
                os.kill(pid, signal.SIGTERM)
                os.remove(pid_file)
                app.logger.info("服务器已停止")
                return jsonify({"message": "服务器已停止"}), 200
            except Exception as e:
                app.logger.error(f"停止服务器出错：{str(e)}")
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"message": "服务器未运行"}), 200

    else:
        return jsonify({"error": "未指定操作"}), 400

@app.route('/delete-file', methods=['POST'])
def delete_file():
    data = request.get_json()
    filename = data.get('filename')
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        file_size = os.path.getsize(file_path)  # 获取删除文件的大小
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
            app.logger.info(f"Directory {filename} deleted") # 删除目录日志
        else:
            os.remove(file_path)
            app.logger.info(f"File {filename} deleted") # 删除文件日志
        update_cumulative_network_usage(0, file_size) # 更新累计下载 (假设删除是下载行为)
        record_daily_usage(0, file_size) # 记录到每日流量
        return jsonify({"message": f"文件 {filename} 已被删除"}), 200
    except FileNotFoundError:
        app.logger.warning(f"File not found during deletion: {filename}") # 文件未找到日志
        return jsonify({"error": f"文件 {filename} 未找到"}), 404
    except Exception as e:
        app.logger.error(f"Error deleting file {filename}: {str(e)}") # 删除文件错误日志
        return jsonify({'error': str(e)}), 500

@app.route('/rename-file', methods=['POST'])
def rename_file():
    data = request.get_json()
    old_filename = data.get('oldFilename')
    new_filename = data.get('newFilename')
    if not old_filename or not new_filename:
        app.logger.warning("Rename request missing old or new filename") # 重命名请求缺少文件名日志
        return jsonify({'error': '新旧文件名不能为空'}), 400
    old_file_path = os.path.join(UPLOAD_FOLDER, old_filename)
    new_file_path = os.path.join(UPLOAD_FOLDER, new_filename)
    try:
        os.rename(old_file_path, new_file_path)
        app.logger.info(f"File renamed from {old_filename} to {new_filename}") # 文件重命名日志
        return jsonify({'message': f'文件 {old_filename} 重命名为 {new_filename}'}), 200
    except FileNotFoundError:
        app.logger.warning(f"File not found during rename: {old_filename}") # 重命名时文件未找到日志
        return jsonify({'error': f'文件 {old_filename} 不存在'}), 404
    except FileExistsError:
        app.logger.warning(f"File already exists with new name: {new_filename}") # 重命名时新文件名已存在日志
        return jsonify({'error': f'文件 {new_filename} 已存在'}), 409 # 409 Conflict
    except Exception as e:
        app.logger.error(f"Error renaming file {old_filename} to {new_filename}: {str(e)}") # 重命名文件错误日志
        return jsonify({'error': str(e)}), 500



@app.route('/server-status', methods=['GET'])
def server_status():
    return jsonify(get_server_resource_usage())

@app.route('/network-stats', methods=['GET'])
def network_stats():
    stats = get_network_stats()
    return jsonify(stats)

@app.route('/daily-usage', methods=['GET'])
def daily_usage():
    history = get_daily_usage_history()
    return jsonify(history)

# ---------------------  错误处理  ---------------------
@app.errorhandler(404)
def page_not_found(error):
    app.logger.warning(f"Page not found: {request.path}") # 404 页面日志
    return render_template('404.html'), 404

# ---------------------  启动  ---------------------
if __name__ == "__main__":
    app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key") # 仍然支持环境变量 SECRET_KEY
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=True) # 端口号从配置文件读取