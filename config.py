import os
from typing import Optional
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """
    Configuración centralizada para la aplicación
    """
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_PROTOCOL: str = os.getenv("API_PROTOCOL", "http")
    
    @classmethod
    def get_api_base_url(cls, request: Optional[object] = None) -> str:
        """
        Obtiene la URL base de la API
        Si se proporciona un request, usa la URL del request
        Si no, usa las variables de configuración
        """
        if request:
            return f"{request.url.scheme}://{request.url.netloc}"
        else:
            return f"{cls.API_PROTOCOL}://{cls.API_HOST}:{cls.API_PORT}"
    
    @classmethod
    def get_users_endpoint(cls, request: Optional[object] = None) -> str:
        """Endpoint completo para usuarios"""
        return f"{cls.get_api_base_url(request)}/users/"
    
    @classmethod
    def get_images_endpoint(cls, request: Optional[object] = None) -> str:
        """Endpoint completo para imágenes"""
        return f"{cls.get_api_base_url(request)}/images"

# Instancia global de configuración
config = Config()