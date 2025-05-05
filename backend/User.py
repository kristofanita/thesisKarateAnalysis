

class User():
    def __init__(self, name, email, birth_date, height, weight, id, latest_score=None,
                 latest_score_time=None, best_score=None, best_score_time=None):
        self.name = name
        self.email = email
        self.birth_date = birth_date
        self.height = height
        self.weight = weight
        self.user_id = id
        self.latest_score = latest_score
        self.latest_score_time = latest_score_time
        self.best_score = best_score
        self.best_score_time = best_score_time
    
    def get_name(self):
        return self.name
    
    def get_user_id(self):
        return self.user_id
    
    def print_user(self):
        print("User", self.name, "successfully logged in")

    def print_user_data(self):
        return(
            f"Name: {self.name}\n"
            f"user_id: {self.user_id}\n"
            f"Email: {self.email}\n"
            f"Birth date: {self.birth_date}\n"
            f"Height: {self.height}\n"
            f"Weight: {self.weight}\n"
            f"Latest max score ({self.latest_score_time}): {self.latest_score}\n"
            f"Best score ({self.best_score_time}): {self.best_score}"
        )
