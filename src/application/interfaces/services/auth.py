from typing import Protocol


class IAuthService(Protocol):

    def encode_password(self, password: str):
        pass

    def verify_password(self, password: str, encoded_password: str):
        pass

    def encode_token(self, username: str):
        pass

    def decode_token(self, token: str):
        pass

    def encode_refresh_token(self, username: str):
        pass

    def refresh_token(self, refresh_token: str):
        pass
