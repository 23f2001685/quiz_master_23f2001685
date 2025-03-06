class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class LocalDevConfig(Config):
    # Configuration
    SQLALCHEMY_DATABASE_URI = "sqlite:///quiz_master.db"
    DEBUG = True

    # Security Configurations
    SECRET_KEY = "h$5wj*!26=_10yh%ii21!^x2q=jgysn!!9+a&b(nznne0s427-"             # Hash user's creds in session
    SECURITY_PASSWORD_HASH = "bcrypt"                                             # Algo used to encrypt
    SECURITY_PASSWORD_SALT = "u(u$9-0&*!pusa#ddfltgk@or%et_!2j0#tz*m5&itx(y&+*)*" # Helps in hashing pass
    WTF_CSRF_ENABLED = False                                                      # Verification of origin of form
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"