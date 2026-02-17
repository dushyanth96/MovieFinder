import MovieCard from "../components/MovieCard";
import {useState} from 'react';
import { useEffect } from "react";
import {searchMovies , getPopularMovies} from '../services/api';
import '../css/Home.css'

export default function Home() {
    const [searchQuery, setSearchQuery] = useState('');
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    useEffect(()=>{
        // getPopularMovies().then(data=>setMovies(data));
        const loadPopularMovies = async() =>{
          try{
            const popularMovies = await getPopularMovies();
            setMovies(popularMovies);
          }
          catch(err){
            
            setError(err.message);
            console.log(err)
          }
          finally{
            setLoading(false);
          }
        }
        loadPopularMovies();
      
    },[])

       
    const handleSearch=(e)=>{
        e.preventDefault();
        // console.log(searchQuery);
        if(!searchQuery.trim()) return
        if(loading) return;
        setLoading(true);
        try{
          searchMovies(searchQuery).then(data=>setMovies(data));
        }
        catch(err){
          setError(err.message);
        }
        finally{
          setLoading(false);
        }
    }
  
    return (
    <div className="home">
        <form action="" onSubmit={handleSearch} className='search-form'>
            <input type="text" placeholder="Search for movies..." className="search-input" value={searchQuery} 
            onChange={(e)=>setSearchQuery(e.target.value)}/>
            <button type="submit" className="search-button">Search</button>
        </form>
        {error && <div className="error-message">{error}</div>}
        {loading ? (
          <div className="loading">Loading...</div>):
        <div className="movies-grid">
        {movies.map(movie =>(movie.title.toLowerCase().includes(searchQuery.toLowerCase()) && (<MovieCard key={movie.id} movie={movie} />)))}
      </div>}
      
    </div>
  );
}