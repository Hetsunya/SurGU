import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const Search = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [suggestions, setSuggestions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [page, setPage] = useState(1);
    const resultsPerPage = 10;

    const handleSearch = async () => {
        if (!query.trim()) {
            setError('Пожалуйста, введите запрос');
            setResults([]);
            return;
        }

        setLoading(true);
        setError('');
        setSuggestions([]);

        try {
            const response = await axios.get(`http://localhost:8080/search?query=${encodeURIComponent(query)}`);
            // Проверяем, что response.data является массивом
            if (Array.isArray(response.data)) {
                setResults(response.data);
            } else {
                console.error('Response data is not an array:', response.data);
                setResults([]);
                setError('Некорректный ответ сервера');
            }
            setPage(1);
        } catch (err) {
            console.error('Search error:', err);
            setResults([]);
            setError('Ошибка при получении результатов поиска: ' + (err.response?.data || err.message));
        }
        setLoading(false);
    };

    const handleInputChange = async (e) => {
        const value = e.target.value;
        setQuery(value);
        if (value.length > 2) {
            try {
                const response = await axios.get(`http://localhost:8080/suggest?prefix=${encodeURIComponent(value)}`);
                if (Array.isArray(response.data)) {
                    setSuggestions(response.data);
                } else {
                    console.error('Suggestions response is not an array:', response.data);
                    setSuggestions([]);
                }
            } catch (err) {
                console.error('Error fetching suggestions:', err);
                setSuggestions([]);
            }
        } else {
            setSuggestions([]);
        }
    };

    const paginatedResults = results.slice((page-1)*resultsPerPage, page*resultsPerPage);

    return (
        <div className="search-container">
            <h1>ПоискоВики</h1>
            <div className="search-input">
                <input
                    type="text"
                    value={query}
                    onChange={handleInputChange}
                    placeholder="Введите запрос, например, рок музыка"
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
                <button onClick={handleSearch} disabled={loading}>
                    {loading ? 'Поиск...' : 'Искать'}
                </button>
            </div>
            {suggestions.length > 0 && (
                <ul className="suggestions">
                    {suggestions.map((suggestion, index) => (
                        <li key={index} onClick={() => { setQuery(suggestion); setSuggestions([]); handleSearch(); }}>
                            {suggestion}
                        </li>
                    ))}
                </ul>
            )}
            {error && <p className="error">{error}</p>}
            {paginatedResults.length > 0 ? (
                <>
                    <ul className="results-list">
                        {paginatedResults.map((result) => (
                            <li key={result.ID} className="result-item">
                                <a href={result.URL} target="_blank" rel="noopener noreferrer">
                                    {result.Title.replace(/\n/g, '').trim()}
                                </a>
                                <p className="snippet">
                                    {result.Snippet.split('<b>').map((part, index) => {
                                        if (part.includes('</b>')) {
                                            const [bold, rest] = part.split('</b>');
                                            return <span key={index}><b>{bold}</b>{rest}</span>;
                                        }
                                        return <span key={index}>{part}</span>;
                                    })}
                                </p>
                                <div className="scores">
                                    <p><strong>Общий рейтинг:</strong> {result.Score.toFixed(4)}</p>
                                    <p><strong>BM25:</strong> {(result.BM25Score || 0).toFixed(4)}</p>
                                    <p><strong>PageRank:</strong> {(result.PageRankScore || 0).toFixed(4)}</p>
                                </div>
                            </li>
                        ))}
                    </ul>
                    <div className="pagination">
                        <button onClick={() => setPage(page-1)} disabled={page === 1}>Назад</button>
                        <span>Страница {page}</span>
                        <button onClick={() => setPage(page+1)} disabled={page*resultsPerPage >= results.length}>Вперёд</button>
                    </div>
                </>
            ) : (
                <p className="no-results">Нет результатов для вашего запроса.</p>
            )}
        </div>
    );
};

export default Search;