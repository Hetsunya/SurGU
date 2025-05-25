package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"

	_ "github.com/mattn/go-sqlite3"

	"mysearchengine/bm25"
	"mysearchengine/models"
	"mysearchengine/pagerank"
)

var db *sql.DB
var pageRanks map[string]float64
var avgDocLength float64
var config Config

// Config хранит параметры алгоритмов
type Config struct {
	BM25 struct {
		K1 float64
		B  float64
	}
	PageRank struct {
		D             float64
		MaxIterations int
	}
}

func init() {
	// Загрузка конфигурации
	config = Config{}
	config.BM25.K1 = 1.2
	config.BM25.B = 0.75
	config.PageRank.D = 0.85
	config.PageRank.MaxIterations = 35

	// Подключение к базе данных
	var err error
	db, err = sql.Open("sqlite3", "./search_engine.db")
	if err != nil {
		log.Fatal(err)
	}

	// Загрузка всех документов
	rows, err := db.Query("SELECT id, title, url, content, links FROM documents")
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	allDocs := make(map[int]models.Document)
	var allDocList []models.Document
	for rows.Next() {
		var doc models.Document
		var linksStr string
		if err := rows.Scan(&doc.ID, &doc.Title, &doc.URL, &doc.Content, &linksStr); err != nil {
			log.Fatal(err)
		}
		doc.URLLinks = strings.Split(linksStr, ",")
		allDocs[doc.ID] = doc
		allDocList = append(allDocList, doc)
	}

	// Кэширование средней длины документа
	totalLength := 0.0
	for _, doc := range allDocs {
		totalLength += float64(len(strings.Fields(doc.Content)))
	}
	if len(allDocs) > 0 {
		avgDocLength = totalLength / float64(len(allDocs))
	}
	log.Printf("Cached average document length: %f", avgDocLength)

	// Кэширование PageRank
	pageRanks = pagerank.CalculatePageRank(allDocList, config.PageRank.D, config.PageRank.MaxIterations)
	log.Printf("Cached PageRank for %d documents", len(pageRanks))
}

func setHeaders(w http.ResponseWriter) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
}

func searchHandler(w http.ResponseWriter, r *http.Request) {
	setHeaders(w)

	query := r.URL.Query().Get("query")
	if query == "" {
		log.Printf("Empty query received")
		http.Error(w, "Query parameter is missing", http.StatusBadRequest)
		return
	}

	queryWords := strings.Fields(strings.ToLower(query))
	log.Printf("Search query: %s", query)

	// Получаем все документы
	rows, err := db.Query("SELECT id, title, url, content, links FROM documents")
	if err != nil {
		log.Printf("Database query error: %v", err)
		http.Error(w, fmt.Sprintf("Database query error: %v", err), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	allDocs := make(map[int]models.Document)
	for rows.Next() {
		var doc models.Document
		var linksStr string
		if err := rows.Scan(&doc.ID, &doc.Title, &doc.URL, &doc.Content, &linksStr); err != nil {
			log.Printf("Error scanning row: %v", err)
			http.Error(w, fmt.Sprintf("Error scanning row: %v", err), http.StatusInternalServerError)
			return
		}
		doc.URLLinks = strings.Split(linksStr, ",")
		allDocs[doc.ID] = doc
	}

	// Поиск релевантных документов через индекс
	results := make(map[int]models.Document)
	frequencies := make(map[int]map[string]int)
	for _, word := range queryWords {
		log.Printf("Searching for word: %s", word)
		rows, err := db.Query(`
            SELECT documents.id, documents.title, documents.url, documents.content, documents.links, index_table.frequency
            FROM documents
            JOIN index_table ON documents.id = index_table.doc_id
            WHERE index_table.word = ?
        `, word)
		if err != nil {
			log.Printf("Database query error for word %s: %v", word, err)
			http.Error(w, fmt.Sprintf("Database query error: %v", err), http.StatusInternalServerError)
			return
		}
		defer rows.Close()

		found := false
		for rows.Next() {
			found = true
			var doc models.Document
			var linksStr string
			var freq int
			if err := rows.Scan(&doc.ID, &doc.Title, &doc.URL, &doc.Content, &linksStr, &freq); err != nil {
				log.Printf("Error scanning row for word %s: %v", word, err)
				http.Error(w, fmt.Sprintf("Error scanning row: %v", err), http.StatusInternalServerError)
				return
			}
			doc.URLLinks = strings.Split(linksStr, ",")
			results[doc.ID] = doc
			if frequencies[doc.ID] == nil {
				frequencies[doc.ID] = make(map[string]int)
			}
			frequencies[doc.ID][word] = freq
		}
		if !found {
			log.Printf("Word not found in index: %s", word)
		}
	}

	// Преобразуем результаты в список
	var resultList []models.Document
	for _, doc := range results {
		resultList = append(resultList, doc)
	}
	log.Printf("Found documents before ranking: %d", len(resultList))

	// Расчёт BM25
	resultList = bm25.CalculateBM25(queryWords, resultList, config.BM25.K1, config.BM25.B, allDocs, frequencies, db, avgDocLength)

	// Комбинируем BM25 и PageRank
	maxPageRank := 0.0
	for _, pr := range pageRanks {
		if pr > maxPageRank {
			maxPageRank = pr
		}
	}
	var finalResultList []models.Document
	for i := range resultList {
		resultList[i].BM25Score = resultList[i].Score
		if maxPageRank > 0 {
			resultList[i].PageRankScore = (pageRanks[resultList[i].URL] / maxPageRank) * 1.0
			resultList[i].Score = 0.5*resultList[i].BM25Score + ((1 - 0.5) * resultList[i].PageRankScore)
			// resultList[i].Score = resultList[i].BM25Score * resultList[i].PageRankScore
			// resultList[i].Score = resultList[i].PageRankScore * (0.95 + 0.1*resultList[i].BM25Score)
		} else {
			resultList[i].PageRankScore = 0
			resultList[i].Score = resultList[i].BM25Score
		}
		// Порог BM25Score
		if resultList[i].BM25Score > 0.001 {
			// Генерация сниппета
			snippet := generateSnippet(resultList[i].Content, queryWords)
			resultList[i].Snippet = snippet
			// Безопасное обрезание сниппета для логирования
			logSnippet := snippet
			if len(snippet) > 50 {
				logSnippet = snippet[:50] + "..."
			}
			log.Printf("Document: %s, BM25Score: %f, PageRankScore: %f, Final Score: %f, Snippet: %s",
				resultList[i].Title, resultList[i].BM25Score, resultList[i].PageRankScore, resultList[i].Score, logSnippet)
			finalResultList = append(finalResultList, resultList[i])
		}
	}

	// Отправляем результат
	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(finalResultList); err != nil {
		log.Printf("Error encoding JSON response: %v", err)
		http.Error(w, "Error encoding response", http.StatusInternalServerError)
		return
	}
}

func suggestHandler(w http.ResponseWriter, r *http.Request) {
	setHeaders(w)
	prefix := r.URL.Query().Get("prefix")
	if prefix == "" {
		log.Printf("Empty prefix received")
		http.Error(w, "Prefix parameter is missing", http.StatusBadRequest)
		return
	}

	rows, err := db.Query("SELECT word FROM word_stats WHERE word LIKE ? LIMIT 10", prefix+"%")
	if err != nil {
		log.Printf("Database query error for prefix %s: %v", prefix, err)
		http.Error(w, fmt.Sprintf("Database query error: %v", err), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var suggestions []string
	for rows.Next() {
		var word string
		if err := rows.Scan(&word); err != nil {
			log.Printf("Error scanning row for prefix %s: %v", prefix, err)
			http.Error(w, fmt.Sprintf("Error scanning row: %v", err), http.StatusInternalServerError)
			return
		}
		suggestions = append(suggestions, word)
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(suggestions); err != nil {
		log.Printf("Error encoding JSON response for suggestions: %v", err)
		http.Error(w, "Error encoding response", http.StatusInternalServerError)
		return
	}
}

func generateSnippet(content string, queryWords []string) string {
	contentLower := strings.ToLower(content)
	sentences := strings.Split(contentLower, ".")
	bestSnippet := ""
	maxMatches := 0
	for _, sentence := range sentences {
		sentenceLower := strings.ToLower(sentence)
		matches := 0
		for _, word := range queryWords {
			if strings.Contains(sentenceLower, word) {
				matches++
			}
		}
		if matches > maxMatches && len(sentence) > 20 {
			maxMatches = matches
			snippet := sentence
			for _, word := range queryWords {
				wordLower := strings.ToLower(word)
				snippet = strings.ReplaceAll(snippet, wordLower, "<b>"+wordLower+"</b>")
			}
			bestSnippet = snippet
		}
	}
	if bestSnippet == "" {
		if len(content) > 100 {
			return content[:100] + "..."
		}
		return content
	}
	return bestSnippet
}

func main() {
	http.HandleFunc("/search", searchHandler)
	http.HandleFunc("/suggest", suggestHandler)
	fmt.Println("Server started on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
