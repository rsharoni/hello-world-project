# Kubernetes Hello World Orchestration

This application uses the docker image **rsharoni/hello-world:1.0.0**. You can find the image on DockerHub at: [https://hub.docker.com/r/rsharoni/hello-world](https://hub.docker.com/r/rsharoni/hello-world) (Note: This specific URL is external to the provided sources).

This project deploys a "Hello World" application using Kubernetes orchestration and scheduling.

## Quick Start
Deploy all components to your cluster:
```bash
kubectl apply -f pv.yaml -f pvc.yaml -f configmap.yaml -f deployment.yaml -f service.yaml -f hpa.yaml -f cronjob.yaml
```

## Accessing the App
The application is exposed via a **NodePort** service.
*   **Browser URL:** `http://localhost:30000`.
*   **Port Mapping:** Host 30000 -> Container 5000.
*   **Minikube Shortcut:** If using Minikube, you can open the app directly with:
```bash
minikube service <pod-service-name>
```
*(For this project, the service name defined in the sources is **hello-world-service**)*.

## Viewing Logs
To see logs from the running application pods:
```bash
kubectl logs -l app=hello-world
```
To view logs from the **CronJob** executed every minute:
```bash
kubectl get jobs
kubectl logs <job-pod-name>
```

## Persistent Storage Setup (PV & PVC)
The project uses a **1Gi Persistent Volume** (local-pv) mapped to the host path `/data`.

# ✅ **SHORT, CORRECT STEP‑BY‑STEP CHECKLIST**

### **1. Start Minikube**
```bash
minikube start
```

---

### **2. Mount your Windows folder into Minikube (in a SEPARATE terminal)**
```bash
minikube mount "C:\data":/data
```

⚠️ **Keep this terminal open**  
If you close it, the mount disappears.

Verify inside Minikube:
```bash
minikube ssh
ls /data
```
You MUST see your Windows files.

---

## Component Verification
Use these commands to verify each component and see the results in your terminal:

*   **Deployment:** 
    *   *Check Status:* `kubectl get deployment hello-world-deployment` to verify **3 replicas**.
    *   *See Results:* `kubectl get pods -l app=hello-world` to ensure all pods are in the **Running** state.
*   **ConfigMap:** 
    *   *Check Status:* `kubectl describe configmap hello-world-config`.
    *   *See Results:* `kubectl get configmap hello-world-config -o yaml` to view environment variables like `APP_MESSAGE` and `SERVER_PORT` (**5000**).
*   **Autoscaling (HPA):** 
    *   *Check Status:* `kubectl get hpa hello-world-hpa`.
    *   *See Results:* `kubectl describe hpa hello-world-hpa` to monitor the **50% CPU** target and current scaling between **1 and 5 replicas**.
*   **Storage (PV & PVC):** 
    *   *Check Status:* `kubectl get pv local-pv` and `kubectl get pvc local-pvc`.
    *   *See Results:* Confirm the status is **Bound** and verify persistence by running `kubectl exec <pod-name> -- ls /data`.
*   **Service:** 
    *   *Check Status:* `kubectl get service hello-world-service`.
    *   *See Results:* `kubectl describe service hello-world-service` to confirm the **NodePort 30000** is active and pointing to valid **Endpoints**.
*   **CronJob:** 
    *   *Check Status:* `kubectl get cronjob hello-world-cron` to see the **one-minute schedule** (`*/1 * * * *`).
    *   *See Results:* `kubectl get jobs` to see the execution history and `kubectl logs <job-pod-name>` to see the "CronJob executed" timestamp.
