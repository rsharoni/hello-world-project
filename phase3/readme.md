# Phase 3 - Jenkins and github with helm

### **What this project does**
- Builds a Docker image from the application source  
- Runs a simple health test on the built container  
- Pushes the image to Docker Hub  
- Deploys the application to Kubernetes using Helm  
- Uses a PersistentVolume (pv.yaml) applied before deployment  
- Requires Docker Hub credentials + Kubernetes kubeconfig stored in Jenkins credentials  

---

# **Pipeline Flow (Step‑by‑Step)**

- **Checkout Code**  
  Pulls the latest code from the GitHub repository.

- **Build Docker Image**  
  Builds the application image using the Dockerfile in `phase1/`.

- **Test Container**  
  Runs the container briefly to ensure it starts and stays healthy.

- **Push to Docker Hub**  
  Logs in using Jenkins credentials and pushes the built image.

- **Apply Persistent Volume**  
  Applies `phase3/pv.yaml` to create the required PV in Kubernetes.

- **Deploy with Helm**  
  Runs `helm upgrade --install` using the chart in `phase3/` to deploy the app.
