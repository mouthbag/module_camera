from abc import abstractmethod

class CAMERA():
    
    @classmethod
    @abstractmethod
    def get_image(self)->bytes:
        pass