export PATH="$HOME/.kubeadm-dind-cluster:$PATH"

kubectl label node kube-node-1 openwhisk-role=core
kubectl label node kube-node-2 openwhisk-role=invoker

# instaling openwhisk
helm init --wait
kubectl create clusterrolebinding tiller-cluster-admin --clusterrole=cluster-admin --serviceaccount=kube-system:default
helm install ./openwhisk --namespace=openwhisk --name=owdev -f values.yaml
kubectl get pods -n openwhisk -w

# install postgres database
helm install --name postgres stable/postgresql --set persistence.enabled=false --namespace=postgres
kubectl get pods -n postgres -w
