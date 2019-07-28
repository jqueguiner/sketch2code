# Docker for API

You can build and run the docker using the following process:

Cloning
```console
git clone https://github.com/jqueguiner/sketch2code sketch2code
```

Building Docker
```console
cd sketch2code && docker build -t sketch2code -f Dockerfile .
```

Running Docker
```console
echo "http://$(curl ifconfig.io):5000" && docker run -p 5000:5000 -d sketch2code
```

Calling the API
```console
curl -X POST "http://MY_SUPER_API_IP:5000/process" -H "accept: text/html" -H "Content-Type: application/json" -d '{"url":"https://i.ibb.co/T4nTjth/input.png"}' --output site.html
```
