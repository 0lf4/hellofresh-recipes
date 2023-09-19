class Recipe:

    def __init__(self, url, name, difficulty, time, created_at, pdf_origin='', pdf_local='', tags=[], allergen=[],
                 ingredients=[], nutrition=[], utensils=[], instructions=[]):
        self.url = url
        self.name = name
        self.pdf_origin = pdf_origin
        self.pdf_local = pdf_local
        self.difficulty = difficulty
        self.time = time
        self.tags = tags
        self.allergen = allergen
        self.ingredients = ingredients
        self.nutrition = nutrition
        self.utensils = utensils
        self.instructions = instructions
        self._created_at = created_at

    def to_json(self):
        return {
            "url": self.url,
            "name": self.name,
            "tags": self.tags,
            "allergen": self.allergen,
            "difficulty": self.difficulty,
            "time": self.time,
            "ingredients": self.ingredients,
            "nutrition": self.nutrition,
            "utensils": self.utensils,
            "pdf_origin": self.pdf_origin,
            "pdf_local": self.pdf_local,
            "instructions": self.instructions,
            "_created_at": self._created_at
        }
