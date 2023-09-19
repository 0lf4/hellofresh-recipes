docker build -t hfapi ../server


docker run -d --name hfapi -p 8000:8000 hfapi
