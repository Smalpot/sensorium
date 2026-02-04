"""
Punto de entrada principal para el sistema SENSORIUM.
"""

from config.database import db
from views.login_view import LoginView
from views.main_view import MainView


def ejecutar_aplicacion() -> None:
    """Inicia el flujo de autenticación y abre la ventana principal."""
    login = LoginView()
    usuario = login.ejecutar()

    if usuario:
        main_view = MainView(usuario)
        main_view.ejecutar()

    db.desconectar()


if __name__ == "__main__":
    ejecutar_aplicacion()
