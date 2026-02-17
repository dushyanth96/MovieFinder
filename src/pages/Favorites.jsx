import '../css/Favorites.css'
import { useMovieContext } from '../contexts/MovieContext';
import MovieCard from '../components/MovieCard';
export default function Favorites() {
  const { favorites } = useMovieContext();
  if (favorites.length === 0) {
    return (
      <div className="favorites-empty">
        <h2>You don't have any favorites yet</h2>
        <p>Start adding movies to your favorites list!</p>
      </div>
    );
  }
  return (
    <div className="favorites-container">
      <h2>Your Favorite Movies</h2>
      <div className="favorites-grid">
        {favorites.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    </div>
  );
}