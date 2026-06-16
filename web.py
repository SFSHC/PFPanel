import os
import math
import signal
import shutil
import subprocess
import zipfile
import logging
import re
import threading
import time
import json
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta

import psutil
from flask import Flask, request, jsonify, render_template, redirect, session, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import chardet

app = Flask(__name__)
CORS(app)

# 从环境变量获取密钥，如果没有设置则使用默认值
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")
bcrypt = Bcrypt(app)

# 密码哈希文件
PASSWORD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.password_hash')

# 会话配置
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
SESSION_TIMEOUT_MINUTES = 30

# 配置文件和服务器路径
SERVER_BASE_DIR = "/root/pf/"
CONFIG_FILE_PATH = os.path.join(SERVER_BASE_DIR, "ServerConfig.txt")
UPLOAD_FOLDER = os.path.join(SERVER_BASE_DIR, "editor")
ALLOWED_EXTENSIONS = {'zip'}
MAX_FILE_SIZE = 1024 * 1024 * 50  # 50 MB

# 日志配置
handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# 网络使用情况跟踪
NETWORK_LOG_FILE = 'network_usage.log'
NETWORK_INITIAL_STATE_FILE = 'network_initial_state.json'
DAILY_USAGE_FILE = 'daily_usage.json'
last_network_stats = None
daily_recording_thread = None

def get_server_pid():
    pid_file = "/tmp/server.pid"
    try:
        with open(pid_file, "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return None

def detect_server_executable():
    """自动检测服务器可执行文件"""
    if not os.path.exists(SERVER_BASE_DIR):
        return None
    
    try:
        files = os.listdir(SERVER_BASE_DIR)
        pattern = re.compile(r'^Polyfield_v\d+\.\d+\.\d+_Linux\.x86_64$')
        matches = [f for f in files if pattern.match(f)]
        
        if matches:
            return os.path.join(SERVER_BASE_DIR, matches[0])
    except Exception as e:
        app.logger.error(f"检测服务器可执行文件出错: {str(e)}")
    
    return None

def get_server_executable():
    """获取服务器可执行文件路径，优先从配置读取，否则自动检测"""
    config = read_config()
    executable = config.get('SERVER_EXECUTABLE')
    
    if executable and os.path.exists(executable):
        return executable
    
    detected = detect_server_executable()
    if detected:
        return detected
    
    return None

def initialize_network_state():
    """初始化网络状态，记录初始值"""
    try:
        if not os.path.exists(NETWORK_INITIAL_STATE_FILE):
            initial_stats = psutil.net_io_counters()
            with open(NETWORK_INITIAL_STATE_FILE, 'w') as f:
                json.dump({
                    'bytes_sent': initial_stats.bytes_sent,
                    'bytes_recv': initial_stats.bytes_recv,
                    'timestamp': datetime.now().isoformat()
                }, f)
            app.logger.info("网络初始状态已记录")
    except Exception as e:
        app.logger.error(f"初始化网络状态出错: {str(e)}")

def get_network_initial_state():
    """获取网络初始状态"""
    try:
        if os.path.exists(NETWORK_INITIAL_STATE_FILE):
            with open(NETWORK_INITIAL_STATE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        app.logger.error(f"读取网络初始状态出错: {str(e)}")
    return None

def sanitize_filename(filename):
    """验证和清理文件名，防止路径遍历攻击"""
    if not filename:
        return None
    
    # 移除路径分隔符和特殊字符
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', filename)
    
    # 检查是否包含路径遍历尝试
    if '..' in filename or filename.startswith('/') or filename.startswith('\\'):
        return None
    
    # 限制文件名长度
    if len(filename) > 255:
        return None
    
    # 确保文件名不为空
    if not filename.strip():
        return None
    
    return filename

def validate_file_size(file_size):
    """验证文件大小"""
    return file_size <= MAX_FILE_SIZE

def record_daily_usage_background():
    """后台线程：定期记录每日流量"""
    last_recorded_stats = psutil.net_io_counters()
    
    while True:
        try:
            time.sleep(300)  # 每5分钟记录一次
            
            current_stats = psutil.net_io_counters()
            sent_diff = current_stats.bytes_sent - last_recorded_stats.bytes_sent
            received_diff = current_stats.bytes_recv - last_recorded_stats.bytes_recv
            
            if sent_diff > 0 or received_diff > 0:
                record_daily_usage(sent_diff, received_diff)
            
            last_recorded_stats = current_stats
        except Exception as e:
            app.logger.error(f"后台记录每日流量出错: {str(e)}")
            last_recorded_stats = psutil.net_io_counters()  # 重置

def is_server_running():
    pid = get_server_pid()
    if pid:
        return psutil.pid_exists(pid)
    return False

def get_network_stats():
    global last_network_stats
    current_stats = psutil.net_io_counters()
    now = datetime.now()

    initial_state = get_network_initial_state()
    
    if initial_state:
        total_sent = current_stats.bytes_sent - initial_state['bytes_sent'] + get_cumulative_network_usage('sent')
        total_received = current_stats.bytes_recv - initial_state['bytes_recv'] + get_cumulative_network_usage('received')
    else:
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
        'total_sent': total_sent if total_sent > 0 else 0,
        'total_received': total_received if total_received > 0 else 0,
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
    config = {}
    try:
        with open(CONFIG_FILE_PATH, 'r') as file:
            for line in file:
                key, value = line.strip().partition('=')[::2]
                config[key.strip()] = value
    except FileNotFoundError:
        return {}
    return config

def write_config(config):
    with open(CONFIG_FILE_PATH, 'w') as file:
        for key, value in config.items():
            file.write(f"{key}={value}\n")

def get_password_hash():
    """读取密码哈希"""
    try:
        if os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, 'r') as f:
                return f.read().strip()
    except Exception as e:
        app.logger.error(f"读取密码哈希出错: {str(e)}")
    return None

def save_password_hash(password):
    """保存密码哈希"""
    try:
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        with open(PASSWORD_FILE, 'w') as f:
            f.write(hashed)
        # 设置文件权限为仅所有者可读写
        os.chmod(PASSWORD_FILE, 0o600)
        return True
    except Exception as e:
        app.logger.error(f"保存密码哈希出错: {str(e)}")
        return False

def is_password_set():
    """检查密码是否已设置"""
    return os.path.exists(PASSWORD_FILE) and os.path.getsize(PASSWORD_FILE) > 0

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


def check_session_timeout():
    """检查会话是否超时"""
    if 'logged_in' in session:
        last_activity = session.get('last_activity')
        if last_activity:
            last_activity_time = datetime.fromisoformat(last_activity)
            if datetime.now() - last_activity_time > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                session.clear()
                return False
        session['last_activity'] = datetime.now().isoformat()
    return True

def require_login(f):
    """要求登录的装饰器"""
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or not check_session_timeout():
            return redirect('/login')
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

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
    if not session.get('logged_in') or not check_session_timeout():
        return redirect('/login')
    config_items = read_config()
    return render_template('config.html', config=config_items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果密码未设置，重定向到设置密码页面
    if not is_password_set():
        return redirect('/setup')
    
    if request.method == 'POST':
        password = request.form.get('password')
        stored_hash = get_password_hash()
        
        if stored_hash and bcrypt.check_password_hash(stored_hash, password):
            session['logged_in'] = True
            session['last_activity'] = datetime.now().isoformat()
            return redirect('/')
        else:
            return render_template('login.html', error='密码错误')
    
    return render_template('login.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    # 如果密码已设置，重定向到登录页面
    if is_password_set():
        return redirect('/login')
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or len(password) < 6:
            return render_template('setup.html', error='密码长度至少6位')
        
        if password != confirm_password:
            return render_template('setup.html', error='两次密码不一致')
        
        if save_password_hash(password):
            session['logged_in'] = True
            session['last_activity'] = datetime.now().isoformat()
            return redirect('/')
        else:
            return render_template('setup.html', error='保存密码失败')
    
    return render_template('setup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/update-config', methods=['POST'])
def update_config():
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    try:
        config = request.form.to_dict()
        write_config(config)
        return jsonify({'message': '配置已更新'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload-map', methods=['POST'])
def upload_map():
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    if 'file' not in request.files:
        return jsonify({"error": "没有文件上传"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "没有选择文件"}), 400
    
    safe_filename = sanitize_filename(file.filename)
    if not safe_filename:
        return jsonify({"error": "文件名包含非法字符"}), 400
    
    if not allowed_file(safe_filename):
        return jsonify({"error": "只允许上传 zip 文件"}), 400
    
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    file.save(file_path)
    
    file_size = os.path.getsize(file_path)
    if not validate_file_size(file_size):
        os.remove(file_path)
        return jsonify({"error": f"文件大小超过限制 ({format_bytes(MAX_FILE_SIZE)})"}), 400
    
    sent_bytes = file_size
    update_cumulative_network_usage(sent_bytes, 0)
    record_daily_usage(sent_bytes, 0)
    result = extract_with_detected_encoding(file_path,UPLOAD_FOLDER)
    if result == "success":
      return jsonify({"message": f"文件 {safe_filename} 已上传并解压"}), 200
    elif result =="BadZipFile":
      return jsonify({"error": "上传的文件不是有效的zip文件"}), 400
    else:
       return jsonify({"error": "解压出错"}), 500

@app.route('/check-file', methods=['POST'])
def check_file():
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    data = request.get_json()
    filename = data.get('filename')
    
    safe_filename = sanitize_filename(filename)
    if not safe_filename:
        return jsonify({'error': '文件名包含非法字符'}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    if os.path.exists(file_path):
        return jsonify({'exists': True}), 200
    else:
        return jsonify({'exists': False}), 200

@app.route('/unzip-map', methods=['POST'])
def unzip_map():
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    data = request.get_json()
    filename = data.get('filename')
    
    safe_filename = sanitize_filename(filename)
    if not safe_filename:
        return jsonify({'error': '文件名包含非法字符'}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    result = extract_with_detected_encoding(file_path,UPLOAD_FOLDER)
    if result == "success":
      return jsonify({"message": f"文件 {safe_filename} 解压完成"}), 200
    elif result =="BadZipFile":
      return jsonify({"error": "上传的文件不是有效的zip文件"}), 400
    else:
       return jsonify({"error": "解压出错"}), 500

@app.route('/files', methods=['GET'])
def list_files():
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
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
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    action = request.json.get("action", "")
    pid_file = "/tmp/server.pid"

    if action == "start":
        if is_server_running():
            return jsonify({"message": "服务器已在运行"}), 200

        server_executable = get_server_executable()
        if not server_executable:
            return jsonify({"error": "无法找到服务器可执行文件，请检查配置或文件路径"}), 500

        try:
            process = subprocess.Popen([server_executable])
            with open(pid_file, "w") as f:
                f.write(str(process.pid))
            app.logger.info("服务器已启动")
            return jsonify({"message": "服务器已启动"}), 200
        except Exception as e:
            app.logger.error(f"启动服务器出错：{str(e)}")
            return jsonify({"error": f"启动服务器失败: {str(e)}"}), 500

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
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    data = request.get_json()
    filename = data.get('filename')
    
    safe_filename = sanitize_filename(filename)
    if not safe_filename:
        return jsonify({'error': '文件名包含非法字符'}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    try:
        file_size = os.path.getsize(file_path)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)
        update_cumulative_network_usage(0, file_size)
        record_daily_usage(0, file_size)
        return jsonify({"message": f"文件 {safe_filename} 已被删除"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/rename-file', methods=['POST'])
def rename_file():
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    data = request.get_json()
    old_filename = data.get('oldFilename')
    new_filename = data.get('newFilename')
    
    if not old_filename or not new_filename:
      return jsonify({'error': '新旧文件名不能为空'}), 400
    
    safe_old_filename = sanitize_filename(old_filename)
    safe_new_filename = sanitize_filename(new_filename)
    
    if not safe_old_filename or not safe_new_filename:
        return jsonify({'error': '文件名包含非法字符'}), 400
    
    if safe_old_filename == safe_new_filename:
        return jsonify({'error': '新旧文件名相同'}), 400
    
    old_file_path = os.path.join(UPLOAD_FOLDER, safe_old_filename)
    new_file_path = os.path.join(UPLOAD_FOLDER, safe_new_filename)
    
    try:
      os.rename(old_file_path, new_file_path)
      return jsonify({'message': f'文件 {safe_old_filename} 重命名为 {safe_new_filename}'}), 200
    except FileNotFoundError:
        return jsonify({'error': f'文件 {safe_old_filename} 不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/server-status', methods=['GET'])
def server_status():
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    return jsonify(get_server_resource_usage())

@app.route('/network-stats', methods=['GET'])
def network_stats():
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    stats = get_network_stats()
    return jsonify(stats)

@app.route('/daily-usage', methods=['GET'])
def daily_usage():
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    history = get_daily_usage_history()
    return jsonify(history)

@app.route('/server-executable', methods=['GET'])
def get_server_executable_info():
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    executable = get_server_executable()
    detected = detect_server_executable()
    return jsonify({
        'current': executable,
        'detected': detected,
        'available': detected is not None
    })

@app.route('/set-server-executable', methods=['POST'])
def set_server_executable():
    if not session.get('logged_in') or not check_session_timeout():
        return jsonify({'error': '未登录或会话已过期'}), 401
    data = request.get_json()
    executable_path = data.get('executable_path')
    
    if not executable_path:
        return jsonify({'error': '可执行文件路径不能为空'}), 400
    
    if not os.path.exists(executable_path):
        return jsonify({'error': '文件不存在'}), 400
    
    if not os.access(executable_path, os.X_OK):
        return jsonify({'error': '文件没有执行权限'}), 400
    
    try:
        config = read_config()
        config['SERVER_EXECUTABLE'] = executable_path
        write_config(config)
        return jsonify({'message': '服务器可执行文件路径已更新'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------------------  错误处理  ---------------------
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# ---------------------  启动  ---------------------
if __name__ == "__main__":
    initialize_network_state()
    
    daily_recording_thread = threading.Thread(target=record_daily_usage_background, daemon=True)
    daily_recording_thread.start()
    
    app.run(host="0.0.0.0", port=9999, debug=True)