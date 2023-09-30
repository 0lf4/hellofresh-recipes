import Recipe from './recipe';

interface Document {
    _id: string;
    name: string;
    _source: Recipe;
    showDetails?: boolean;
}

export default Document;
