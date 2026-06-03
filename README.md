# HELLO WORLD PROJECT

## Phase 3 - Jenkins and github with helm

### **What this project does**
- Builds a Docker image from the application source  
- Runs a simple health test on the built container  
- Pushes the image to Docker Hub  
- Deploys the application to Kubernetes using Helm  
- Uses a PersistentVolume (pv.yaml) applied before deployment  
- Requires Docker Hub credentials + Kubernetes kubeconfig stored in Jenkins credentials  

---


## Prerequisites (manual steps before running the Jenkins pipeline)

1. **Start Minikube**
   ```bash
   minikube start
   ```
   - All deployments run in the **dev** namespace inside this Minikube cluster.

2. **Prepare the local folder and file to sync with the pod**
   - Create the folder:
     ```
     C:\data
     ```
   - Create the file:
     ```
     C:\data\text.txt
     ```
   - This folder will sync with `/data` inside Minikube and inside the pod.

3. **Start Minikube mount (required for two‑way sync)**
   ```bash
   minikube mount C:\data:/data
   ```
   - Keep this terminal **open**  
   - `/data` on Windows ↔ `/data` in Minikube ↔ `/data` in the pod  
   - Jenkins does **not** run this automatically.

4. **Ensure kubectl is using the Minikube context**
   ```bash
   kubectl config use-context minikube
   ```
   - Ensures Jenkins deploys into the **dev** namespace on Minikube.

5. **Verify Jenkins credentials exist**
   - Go to:  
     **Jenkins → Dashboard → Manage Jenkins → Credentials**
   - Required credentials:
     - **Docker Hub credentials**  
       - ID: `docker-hub-credentials`  
       - Contains your Docker Hub username + password  
     - **Kubernetes kubeconfig**  
       - ID: `kubeconfig-cred`  
       - Upload your local `~/.kube/config` file  
       - Used by Jenkins to deploy into the **dev** namespace

6. **(Optional) Clean only this project’s PV/PVC if needed**
   ```bash
   kubectl delete pvc hello-world-pvc -n dev
   kubectl delete pv local-pv
   ```
   - Only delete these if you need to reset the storage for the **dev** namespace.

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
  Runs `helm upgrade --install` using the chart in `./phase3/hello-world-chart` to deploy the app.
