from sqlalchemy import Boolean, create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from tracker.utils import format_timedelta

# Define the Base
Base = declarative_base()

# Define the App class
class App(Base):
    __tablename__ = 'apps'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    ps_name = Column(String)  # Nombre del proceso en el sistema operativo
    tracking = Column(Boolean, default=False)  # Campo booleano añadido
    total_usage_time = Column(Integer, default=0)  # Tiempo total de uso en segundos


# Define the Log class
class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey('apps.id'), nullable=False)
    start_time = Column(DateTime, nullable=False, default=datetime.now)
    end_time = Column(DateTime)
    app = relationship('App', back_populates='logs')

App.logs = relationship('Log', order_by=Log.id, back_populates='app')

# Configuración de la base de datos
engine = create_engine('sqlite:///data/tracker.db')
Session = sessionmaker(bind=engine)

def setup_database():
    Base.metadata.create_all(engine)

def get_session():
    return Session()

def create_app(session, app_name, ps_name):
    app = session.query(App).filter_by(name=app_name).first()
    if not app:
        app = App(name=app_name, ps_name=ps_name)
        session.add(app)
        session.commit()
    return app

def create_log(session, app_id):
    log = Log(app_id=app_id, start_time=datetime.now().replace(microsecond=0))
    app_name = get_name_app(session, app_id)
    print(f"[START] {app_name} - {log.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    session.add(log)
    session.commit()
    return log

def close_log(session, app_id):
    print(f"Intentando cerrar log para app_id: {app_id}")
    log = session.query(Log).filter_by(app_id=app_id).order_by(Log.start_time.desc()).first()
    if log:
        print(f"Log encontrado: {log}")
        if log.end_time is None:
            log.end_time = datetime.now().replace(microsecond=0)
            app_name = get_name_app(session, app_id)
            print(f"[CLOSE] {app_name} - {log.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            session.commit()
            usage_time = int((log.end_time - log.start_time).total_seconds())
            update_app_usage_time(session, app_id, usage_time)
            return log
        else:
            print(f"El log ya tiene un end_time: {log.end_time}")
    else:
        print("No se encontró ningún log para cerrar.")
    return None

def update_app_usage_time(session, app_id, usage_time):
    app = session.query(App).filter_by(id=app_id).first()
    if app:
        app.total_usage_time += usage_time
        print(f"Tiempo de uso de {app.name}: {app.total_usage_time} segundos. Ultima sesion: {usage_time} segundos.")
        session.commit()
        return app
    return None

def get_app_id(session, ps):
    app = session.query(App).filter_by(ps_name=ps).first()
    if app:
        return app.id
    return None

def get_name_app(session, app_id):
    app = session.query(App).filter_by(id=app_id).first()
    if app:
        return app.name
    return None

def fetch_logs(session):
    logs = session.query(Log).all()
    return [(log.app.name, log.start_time, log.end_time, format_timedelta(int((log.end_time - log.start_time).total_seconds()))) for log in logs]

def fetch_apps(session):
    apps = session.query(App).all()
    return [(app.name, app.ps_name, format_timedelta(app.total_usage_time)) for app in apps]

def fetch_names(session):
    apps = session.query(App).all()
    return [app.name for app in apps]

def fetch_processes(session):
    apps = session.query(App).all()
    return [app.ps_name for app in apps]

def get_app_by_name(session, app_name):
    return session.query(App).filter_by(name=app_name).first()