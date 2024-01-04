from FastAPI import APIRouter

class Controller(ABC):
    def initRouter(self):
        self.router = APIRouter()

    @abstractmethod
    def __init__(dao):
        pass