#!/bin/sh

docker build -t hfweb ../client/front

docker run -d --name hfweb -p 3000:3000 hfweb
