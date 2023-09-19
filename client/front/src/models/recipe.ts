type RecipeConstructorOptions = {
    url: string;
    name: string;
    difficulty: string;
    time: string;
    created_at: string;
    pdf_origin?: string;
    pdf_local?: string;
    tags?: string[];
    allergen?: string[];
    ingredients?: string[];
    nutrition?: string[];
    utensils?: string[];
    instructions?: string[];
};

class Recipe {
    url: string;
    name: string;
    difficulty: string;
    time: string;
    created_at: string;
    pdf_origin: string;
    pdf_local: string;
    tags: string[];
    allergen: string[];
    ingredients: string[];
    nutrition: string[];
    utensils: string[];
    instructions: string[];

    constructor(options: RecipeConstructorOptions) {
        this.url = options.url;
        this.name = options.name;
        this.difficulty = options.difficulty;
        this.time = options.time;
        this.created_at = options.created_at;
        this.pdf_origin = options.pdf_origin || '';
        this.pdf_local = options.pdf_local || '';
        this.tags = options.tags || [];
        this.allergen = options.allergen || [];
        this.ingredients = options.ingredients || [];
        this.nutrition = options.nutrition || [];
        this.utensils = options.utensils || [];
        this.instructions = options.instructions || [];
    }

    toJSON(): object {
        return {
            url: this.url,
            name: this.name,
            tags: this.tags,
            allergen: this.allergen,
            difficulty: this.difficulty,
            time: this.time,
            ingredients: this.ingredients,
            nutrition: this.nutrition,
            utensils: this.utensils,
            pdf_origin: this.pdf_origin,
            pdf_local: this.pdf_local,
            instructions: this.instructions,
            created_at: this.created_at
        };
    }
}

export default Recipe;
