import { createContext,useState,useContext, useEffect } from "react";

const MovieContext = createContext();

export const useMovieContext = ()=> useContext(MovieContext);

export const MovieProvider = ({children})=>{
    // 🔥 NEW: Auth state (for login system)
    const [user, setUser] = useState(() => {
        const storedUser = localStorage.getItem("user");
        return storedUser ? JSON.parse(storedUser) : null;
    });

    useEffect(() => {
    if (user) {
        localStorage.setItem("user", JSON.stringify(user));
    } else {
        localStorage.removeItem("user");
    }
}, [user]);
useEffect(() => {
    const fetchFavorites = async () => {
        if (!user) {
            setFavorites([]);
            return;
        }

        try {
            const res = await fetch(
                `http://127.0.0.1:5000/api/favorites/${user.id}`
            );
            const data = await res.json();

            // Convert backend format → frontend movie format
            const formattedFavorites = data.map((fav) => ({
                id: fav.movie_id,
                title: fav.title,
                poster_path: fav.poster_path,
            }));

            setFavorites(formattedFavorites);
        } catch (error) {
            console.error("Error fetching favorites:", error);
        }
    };

    fetchFavorites();
}, [user]);

    // 🔥 NEW: Login modal control state
    const [showLoginModal, setShowLoginModal] = useState(false);
    const [favorites, setFavorites] = useState(() => {
        const storedFavorites = localStorage.getItem("favorites");
        return storedFavorites ? JSON.parse(storedFavorites) : [];
    });

    useEffect(() => {
        localStorage.setItem("favorites", JSON.stringify(favorites));
    }, [favorites]);

   

    const addToFavorites = async (movie) => {
    if (!user) return;

    try {
        await fetch("http://127.0.0.1:5000/api/favorites/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                user_id: user.id,
                movie_id: movie.id,
                title: movie.title,
                poster_path: movie.poster_path,
            }),
        });

        // Update local UI state (instant feedback)
        setFavorites((prevFavorites) => {
            if (!prevFavorites.some((fav) => fav.id === movie.id)) {
                return [...prevFavorites, movie];
            }
            return prevFavorites;
        });

    } catch (error) {
        console.error("Error adding favorite:", error);
    }
};


    const removeFromFavorites = async (movieId) => {
    if (!user) return;

    try {
        await fetch("http://127.0.0.1:5000/api/favorites/remove", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                user_id: user.id,
                movie_id: movieId,
            }),
        });

        // Update local UI state
        setFavorites((prevFavorites) =>
            prevFavorites.filter((fav) => fav.id !== movieId)
        );

    } catch (error) {
        console.error("Error removing favorite:", error);
    }
};


    const isFavorite = (movieId) => {
        return favorites.some((fav) => fav.id === movieId);
    };
    const contextValue = {
        user,
        setUser,
        showLoginModal,
        setShowLoginModal,
        favorites,
        addToFavorites,
        removeFromFavorites,
        isFavorite
    };

    return <MovieContext.Provider value={contextValue}>
        {children}
    </MovieContext.Provider>

}