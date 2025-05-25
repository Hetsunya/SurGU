package models

// Document представляет документ в поисковой системе
type Document struct {
	ID            int      `json:"ID"`
	Title         string   `json:"Title"`
	URL           string   `json:"URL"`
	Content       string   `json:"Content"`
	URLLinks      []string `json:"URLLinks"`
	Score         float64  `json:"Score"`
	BM25Score     float64  `json:"BM25Score"`
	PageRankScore float64  `json:"PageRankScore"`
	Snippet       string   `json:"Snippet"`
}
