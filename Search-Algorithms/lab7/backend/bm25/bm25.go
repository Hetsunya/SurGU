package bm25

import (
	"database/sql"
	"log"
	"math"
	"strings"

	"mysearchengine/models"
)

// CalculateBM25 вычисляет BM25 для списка документов
func CalculateBM25(queryWords []string, documents []models.Document, k1, b float64, allDocs map[int]models.Document, frequencies map[int]map[string]int, db *sql.DB, avgDocLength float64) []models.Document {
	var scoredResults []models.Document
	for _, doc := range documents {
		score := 0.0
		docLength := float64(len(strings.Fields(doc.Content)))
		log.Printf("Document: %s, Length: %f", doc.Title, docLength)

		for _, word := range queryWords {
			tf := calculateTermFrequency(word, doc, frequencies[doc.ID])
			idf := calculateInverseDocumentFrequency(word, allDocs, db)
			idf = math.Max(idf, 2.0) // Минимальный порог IDF
			wordScore := idf * (tf * (k1 + 1)) / (tf + k1*(1-b+b*(docLength/avgDocLength)))
			log.Printf("Word: %s, TF: %f, IDF: %f, WordScore: %f", word, tf, idf, wordScore)
			score += wordScore
		}
		log.Printf("Final BM25 score for Document: %s, Score: %f", doc.Title, score)
		doc.Score = score
		scoredResults = append(scoredResults, doc)
	}

	return sortByScore(scoredResults)
}

// calculateTermFrequency использует частоту из index_table
func calculateTermFrequency(word string, doc models.Document, freqMap map[string]int) float64 {
	count := freqMap[word]
	totalWords := len(strings.Fields(doc.Content)) + len(strings.Fields(doc.Title))
	log.Printf("TF for word %s in document %s: count=%d, total words=%d", word, doc.Title, count, totalWords)
	if totalWords == 0 {
		return 0
	}
	return float64(count) / float64(totalWords)
}

// calculateInverseDocumentFrequency использует word_stats
func calculateInverseDocumentFrequency(word string, allDocs map[int]models.Document, db *sql.DB) float64 {
	var docCount, docsWithWord int
	err := db.QueryRow("SELECT COUNT(*) FROM documents").Scan(&docCount)
	if err != nil {
		log.Printf("Error querying document count: %v", err)
		return 0
	}
	err = db.QueryRow("SELECT doc_count FROM word_stats WHERE word = ?", word).Scan(&docsWithWord)
	if err == sql.ErrNoRows {
		log.Printf("Word %s not found in word_stats", word)
		return 0
	}
	if err != nil {
		log.Printf("Error querying word_stats: %v", err)
		return 0
	}
	idf := math.Log(float64(docCount) / float64(docsWithWord+1))
	log.Printf("IDF for word %s: %f (appears in %d of %d documents)", word, idf, docsWithWord, docCount)
	return idf
}

// sortByScore сортирует документы по убыванию Score
func sortByScore(docs []models.Document) []models.Document {
	for i := 0; i < len(docs)-1; i++ {
		for j := i + 1; j < len(docs); j++ {
			if docs[i].Score < docs[j].Score {
				docs[i], docs[j] = docs[j], docs[i]
			}
		}
	}
	return docs
}
