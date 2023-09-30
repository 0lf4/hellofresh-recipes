docker build -t hfapi ../server


docker run -d --name hfapi -e DB_URL=https://192.168.43.137:9200 -e APP_PDF_SAVE_PATH=/app/ressources/seed-me.pdf -p 8000:8000 hfapi
