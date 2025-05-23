# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'todo_secret_key_change_this_in_production'
    DEBUG = False
    TESTING = False

    # Docker 환경 체크
    IS_DOCKER = os.environ.get('IS_DOCKER', 'false').lower() == 'true'
    
    # MySQL 연결 설정 (SQLite 폴백 제거)
    if os.environ.get('SQLALCHEMY_DATABASE_URI'):
        # 환경변수에 직접 지정된 경우 우선 사용
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    elif IS_DOCKER:
        # Docker 내부에서는 컨테이너 이름으로 연결
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://livon:dks12345@mysql:3306/today_todo?charset=utf8mb4'
    else:
        # 로컬 개발환경에서는 Docker 호스트의 IP로 연결
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://livon:dks12345@192.168.123.104:3306/today_todo?charset=utf8mb4'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 3600  # 1시간마다 연결 재생성
    SQLALCHEMY_POOL_TIMEOUT = 60    # 타임아웃 증가
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    
    # 연결 풀 설정 (연결 설정 최적화)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'connect_args': {
            'connect_timeout': 30,      # 연결 타임아웃 증가
            'read_timeout': 30,         # 읽기 타임아웃 증가
            'write_timeout': 30,        # 쓰기 타임아웃 증가
            'charset': 'utf8mb4',
            'autocommit': True
        }
    }

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    # 테스트 환경에서도 MySQL 사용
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://livon:dks12345@192.168.123.104:3306/today_todo?charset=utf8mb4'

class ProductionConfig(Config):
    # 운영환경에서는 환경변수에서 가져오거나 Docker MySQL 사용
    if os.environ.get('SQLALCHEMY_DATABASE_URI'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://livon:dks12345@mysql:3306/today_todo?charset=utf8mb4'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}