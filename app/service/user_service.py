class UserService:
    @staticmethod
    def format_user_name(full_name: str) -> str:
        return full_name.title()