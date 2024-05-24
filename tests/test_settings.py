from app.config.settings import ApplicationSettings, Settings, get_settings

settings = Settings()


def test_load_settings():
    settings = get_settings()
    assert settings.app_env == "local"
    assert settings.db_user == settings.db_user
    assert settings.db_password == settings.db_password
    assert settings.db_host == settings.db_host
    assert settings.db_database == settings.db_database


def test_log_config():
    config = ApplicationSettings.log_config()
    assert "handlers" in config
    assert len(config["handlers"]) > 0
