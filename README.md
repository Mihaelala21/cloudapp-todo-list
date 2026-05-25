\# ☁️ Cloud To-Do App



O aplicație modernă To-Do List dezvoltată pentru laboratorul de \*\*Aplicații Cloud Native\*\*.



\## 🚀 Tehnologii utilizate



| Categorie | Tehnologii |

|-----------|------------|

| \*\*Backend\*\* | Python, Flask |

| \*\*Frontend\*\* | HTML5, CSS3, JavaScript |

| \*\*Containerizare\*\* | Docker, containerd, Rancher Desktop |

| \*\*Orchestrare\*\* | Kubernetes, kubectl |

| \*\*CI/CD\*\* | Google Cloud Build, Cloud Run, Artifact Registry |

| \*\*Version Control\*\* | Git, GitHub |



\## 📋 Funcționalități



\- ✅ Adăugare sarcini noi

\- ✅ Marcare sarcini ca finalizate

\- ✅ Ștergere sarcini

\- ✅ Statistici în timp real (Total, Completate, Rămase)

\- ✅ Interfață modernă cu gradient mov

\- ✅ Endpoint de sănătate (`/health`)



\## 🏃 Cum rulează aplicația



\### Local cu Kubernetes (Rancher Desktop)



```bash

kubectl apply -f deployment.yaml

kubectl get pods

kubectl get svc

