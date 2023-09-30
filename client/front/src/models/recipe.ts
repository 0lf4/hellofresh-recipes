interface Recipe {
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
}

export default Recipe;
