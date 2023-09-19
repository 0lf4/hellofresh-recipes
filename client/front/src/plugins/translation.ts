// translations.ts

export type Language = 'en' | 'fr' | 'es' | 'it' | 'de';

export interface Translations {
    [phrase: string]: {
        [lang in Language]?: string;
    };
}

export const database: Translations = {
    'Nuts': {
        'en': 'Nuts',
        'fr': 'Fruits à coque',
        'es': 'Frutos secos',
        'it': 'Frutta a guscio',
        'de': 'Nusssorten or Schalenfrüchte'
    },
    'Almonds': {
        'en': 'Almonds',
        'fr': 'Amandes',
        'es': 'Almendras',
        'it': 'Mandorle',
        'de': 'Mandeln'
    },
    'Milk': {
        'en': 'Milk',
        'fr': 'Lait',
        'es': 'Leche',
        'it': 'Latte',
        'de': 'Milch'
    },
    'Mustard': {
        'en': 'Mustard',
        'fr': 'Moutarde',
        'es': 'Mostaza',
        'it': 'Senape',
        'de': 'Senf'
    },
    'Egg': {
        'en': 'Egg',
        'fr': 'Œuf',
        'es': 'Huevo',
        'it': 'Uovo',
        'de': 'Ei'
    },
    'Soya': {
        'en': 'Soya',
        'fr': 'Soja',
        'es': 'Soja',
        'it': 'Soia',
        'de': 'Soja'
    },
    'Gluten': {
        'en': 'Gluten',
        'fr': 'Gluten',
        'es': 'Gluten',
        'it': 'Glutine',
        'de': 'Gluten'
    },
    'Wheat': {
        'en': 'Wheat',
        'fr': 'Blé',
        'es': 'Trigo',
        'it': 'Grano',
        'de': 'Weizen'
    },
    'Sesame seeds': {
        'en': 'Sesame seeds',
        'fr': 'Graines de sésame',
        'es': ' Semillas de sésamo',
        'it': 'Semi di sesamo',
        'de': 'Sesamsamen'
    },
    'Sulfur dioxide and sulfites': {
        'en': 'Sulfur dioxide and sulfites',
        'fr': 'Anhydride sulfureux et sulfites',
        'es': 'Dióxido de azufre y sulfitos',
        'it': 'Anidride solforosa e solfiti',
        'de': 'Schwefeldioxid und Sulfite'
    },
    'Fish': {
        'en': 'Fish',
        'fr': 'Poisson',
        'es': 'Pescado',
        'it': 'Pesce',
        'de': 'Fisch'
    },
    'Peanuts': {
        'en': 'Peanuts',
        'fr': 'Arachides',
        'es': 'Cacahuetes o maní',
        'it': 'Arachidi',
        'de': 'Erdnüsse'
    },
    'Rye': {
        'en': 'Rye',
        'fr': 'Seigle',
        'es': 'Centeno',
        'it': 'Segale',
        'de': 'Roggen'
    },
    'Celery': {
        'en': 'Celery',
        'fr': 'Céleri',
        'es': 'Apio',
        'it': 'Sedano',
        'de': 'Sellerie'
    },
    'Pecans': {
        'en': 'Pecans',
        'fr': 'Noix de pécan',
        'es': 'Pacanas',
        'it': 'Noci di pecan',
        'de': 'Pekannüsse'
    },
    'Hazelnuts': {
        'en': 'Hazelnuts',
        'fr': 'Noisettes',
        'es': 'Avellanas',
        'it': 'Nocciole',
        'de': 'Haselnüsse'
    },
    'Walnuts': {
        'en': 'Walnuts',
        'fr': 'Noix',
        'es': 'Nueces',
        'it': 'Noci',
        'de': 'Walnüsse'
    },
    'Cashews': {
        'en': 'Cashews',
        'fr': 'Noix de cajou',
        'es': 'Anacardos ',
        'it': 'Anacardi',
        'de': 'Cashewnüsse'
    },
    'Without pork': {
        'en': 'Without pork',
        'fr': 'Sans porc',
        'es': 'Sin cerdo',
        'it': 'Senza maiale',
        'de': 'Ohne Schweinefleisch'
    },
    'Vegetarian': {
        'en': 'Vegetarian',
        'fr': 'Végétarien',
        'es': 'Vegetariano',
        'it': 'Vegetariano',
        'de': 'Vegetarier'
    },
    'Crustaceans': {
        'en': 'Crustaceans',
        'fr': 'Crustacés',
        'es': 'Crustáceos',
        'it': 'Crostacei',
        'de': 'Krebstiere'
    },
    'Rapido': {
        'en': 'Rapido',
        'fr': 'Rapido',
        'es': 'Rápido',
        'it': 'Rapido',
        'de': 'Schnell'
    },
    'Family': {
        'en': 'Family',
        'fr': 'Famille',
        'es': 'Familia',
        'it': 'Famiglia',
        'de': 'Familie'
    },
    'Spicy': {
        'en': 'Spicy',
        'fr': 'Épicé',
        'es': 'Picante',
        'it': 'Piccante',
        'de': 'Würzig'
    },
    'Barley': {
        'en': 'Barley',
        'fr': 'Orge',
        'es': 'Cebada',
        'it': 'Orzo',
        'de': 'Gerste'
    },
    'Oats': {
        'en': 'Oats',
        'fr': 'Avoine',
        'es': 'Avena',
        'it': 'Avena',
        'de': 'Hafer'
    }
    // ... Add as many phrases as you need
};
