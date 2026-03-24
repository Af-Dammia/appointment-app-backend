from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="buxior.minimoc.engg@gmail.com",
    MAIL_PASSWORD="ihkw rvwp irpv tdvr",
    MAIL_FROM="buxior.minimoc.engg@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)