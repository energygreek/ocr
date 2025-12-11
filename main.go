package main

import (
	"embed"
	"io/fs"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/otiai10/gosseract/v2"
)

//go:embed static/dist
var f embed.FS

func main() {

	r := gin.Default()
	st, err := fs.Sub(f, "static/dist")
	if err != nil {
		panic(err)
	}

	r.StaticFS("/static", http.FS(st))

	r.GET("/", func(c *gin.Context) {
		c.Redirect(http.StatusFound, "/static/index.html")
	})

	// Group API routes under /api
	api := r.Group("/api")
	{
		api.POST("/ocr", func(c *gin.Context) {
			file, err := c.FormFile("image")
			if err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}

			client := gosseract.NewClient()
			defer client.Close()
			err = client.SetLanguage("eng")
			if err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}
			err = client.SetPageSegMode(13)
			if err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}

			path := "./uploads/" + file.Filename
			// Save the uploaded file to disk
			if err := c.SaveUploadedFile(file, path); err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}
			err = client.SetImage(path)
			if err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}

			boxes, err := client.GetBoundingBoxes(gosseract.RIL_WORD)
			if err != nil {
				panic(err)
			}

			var results []map[string]string

			for _, value := range boxes {
				results = append(results, map[string]string{
					"left":   strconv.Itoa(value.Box.Min.X),
					"top":    strconv.Itoa(value.Box.Min.Y),
					"width":  strconv.Itoa(value.Box.Dx()),
					"height": strconv.Itoa(value.Box.Dy()),
					"text":   value.Word,
				})
			}

			c.JSON(http.StatusOK, results)
		})
	}

	r.Run(":8080")
}
