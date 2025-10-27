Build da imagem:
docker build -t israel/travel-app:latest .


Push para registry (local ou Docker Hub):
docker push israel/travel-app:latest

Deploy no Kubernetes:
kubectl create ns travel
kubectl apply -f k8s/

Acesso via VPN (WireGuard/Tailscale):
→ https://travel.local

