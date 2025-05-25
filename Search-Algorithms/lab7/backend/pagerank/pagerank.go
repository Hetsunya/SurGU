package pagerank

import (
	"log"
	"math"

	"mysearchengine/models"
)

// CalculatePageRank вычисляет PageRank для списка документов
func CalculatePageRank(documents []models.Document, d float64, maxIterations int) map[string]float64 {
	n := len(documents)
	ranks := make(map[string]float64)
	if n == 0 {
		return ranks
	}

	// Начальные значения PR
	for _, doc := range documents {
		ranks[doc.URL] = 1.0 / float64(n)
	}
	log.Printf("Initial PageRank values for %d documents:", n)
	for _, doc := range documents {
		log.Printf("Document: %s, Initial PageRank: %f", doc.Title, ranks[doc.URL])
	}

	// Итерации PageRank с проверкой сходимости
	for i := 0; i < maxIterations; i++ {
		newRanks := make(map[string]float64)
		maxChange := 0.0
		for _, doc := range documents {
			rankSum := 0.0
			// Ищем документы, ссылающиеся на текущий
			for _, otherDoc := range documents {
				for _, link := range otherDoc.URLLinks {
					if link == doc.URL {
						numLinks := len(otherDoc.URLLinks)
						if numLinks > 0 {
							rankSum += ranks[otherDoc.URL] / float64(numLinks)
						}
					}
				}
			}
			newRanks[doc.URL] = (1.0-d)/float64(n) + d*rankSum
			change := math.Abs(newRanks[doc.URL] - ranks[doc.URL])
			if change > maxChange {
				maxChange = change
			}
		}
		// Нормализация
		totalRank := 0.0
		for _, rank := range newRanks {
			totalRank += rank
		}
		for url := range newRanks {
			newRanks[url] = newRanks[url] / totalRank * float64(n)
		}
		ranks = newRanks
		log.Printf("PageRank values after iteration %d, max change: %f", i+1, maxChange)
		for _, doc := range documents {
			log.Printf("Document: %s, PageRank: %f", doc.Title, ranks[doc.URL])
		}
		// Проверка сходимости
		if maxChange < 0.000001 {
			log.Printf("PageRank converged after %d iterations", i+1)
			break
		}
	}

	return ranks
}
