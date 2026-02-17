import '../css/MovieCard.css'
import {useMovieContext} from '../contexts/MovieContext';
export default function MovieCard({ movie }) {
    
    const { 
        addToFavorites, 
        removeFromFavorites, 
        favorites, 
        user, 
        setShowLoginModal 
    } = useMovieContext();

    const isFav = favorites.some((fav) => fav.id === movie.id);
    function handleFavorite(e) {
        e.preventDefault();
        if (!user) {
            setShowLoginModal(true);
            return;
        }
        if (isFav) {
            removeFromFavorites(movie.id);
        } else {
            addToFavorites(movie);
        }
    }

    
    return(
        <div className='movie-card'>
            <div className="movie-poster">
                <img src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} alt={movie.title} />
                <div className="movie-overlay">
                    <button className={`favorite-btn ${isFav ? 'active' : ''}`} onClick={handleFavorite}>{isFav ? '❤️' : '🤍'}</button>
                </div>
            </div>
            <div className="movie-info">
                <h3>{movie.title}</h3>
                <p>{movie.release_date?.split('-')[0]}</p>
            </div>
        </div>
    )
}