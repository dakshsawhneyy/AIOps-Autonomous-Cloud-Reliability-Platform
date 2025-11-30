#################################
# Prometheus and Grafana
#################################
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://charts.helm.sh/stable
helm repo update
kubectl create namespace monitoring
helm install kind-prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --set prometheus.service.nodePort=30000 --set prometheus.service.type=NodePort --set grafana.service.nodePort=31000 --set grafana.service.type=NodePort --set alertmanager.service.nodePort=32000 --set alertmanager.service.type=NodePort --set prometheus-node-exporter.service.nodePort=32001 --set prometheus-node-exporter.service.type=NodePort
kubectl get svc -n monitoring
kubectl get namespace

# Expose these services
kubectl port-forward svc/kind-prometheus-kube-prome-prometheus -n monitoring 9090:9090 --address=0.0.0.0 &
kubectl port-forward svc/kind-prometheus-grafana -n monitoring 31000:80 --address=0.0.0.0 &

# Grafana Password
kubectl get secret --namespace monitoring kind-prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

#################################
# Strimzi and Kafka
#################################
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest?namespace=kafka

# create a simple Kafka cluster:
kubectl apply -f https://raw.githubusercontent.com/strimzi/strimzi-kafka-operator/main/examples/kafka/kafka-persistent.yaml -n kafka

#################################
# 
#################################