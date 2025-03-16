import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# Charger la clé API Groq depuis un fichier .env
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

# Titre de l'application
st.title("Évaluation de CV par IA")
st.write("""
Cette application utilise l'IA pour évaluer un CV par rapport à une offre d'emploi.
""")

# Fonction pour extraire le texte d'un PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Fonction pour évaluer le CV
def evaluate_cv(cv_text, job_description):
    prompt = f"""
Tu es un expert en recrutement et en analyse de CV. 
Ton rôle est d'évaluer un CV par rapport à une offre d'emploi, puis de générer un CV optimisé.

CV du candidat :
\"\"\"  
{cv_text}  
\"\"\"  

Offre d'emploi : 
\"\"\"  
{job_description}  
\"\"\"  

### Instructions pour l'évaluation :
1. Pour chaque critère, évalue si l'élément est présent (✅), partiellement présent (⚠️), ou absent (❌).
2. Explique clairement pourquoi tu as donné cette évaluation :
   - Si l'élément est présent (✅), précise ce qui est présent et comment cela correspond à l'offre.
   - Si l'élément est partiellement présent (⚠️), explique ce qui manque ou ce qui pourrait être amélioré.
   - Si l'élément est absent (❌), explique pourquoi il est important pour l'offre et ce qui pourrait être ajouté.
3. Pour les compétences techniques (Hard Skills), compare explicitement les compétences mentionnées dans le CV avec celles requises dans l'offre.
   - Si une compétence requise est absente, explique pourquoi elle est importante pour le poste.
4. Structure la sortie en trois parties :
   - [EXTRACTION] : Résumé structuré des informations du CV.
   - [ÉVALUATION] : Analyse point par point avec ✅, ⚠️, ou ❌, et une explication détaillée pour chaque critère.
   - [CV AMÉLIORÉ] : Proposition d'une version améliorée du CV.

Exemples d'évaluation :

Exemple 1 :
CV du candidat :
- Compétences : JavaScript, React, Node.js, MySQL
Offre d'emploi :
- Compétences requises : React, Node.js, Python, SQL

Évaluation :
- ✅ Langages de programmation : Présent (JavaScript, React, Node.js)
  - Le CV mentionne JavaScript, React et Node.js, ce qui correspond aux attentes de l'offre.
- ❌ Langages de programmation : Absent (Python, SQL)
  - Le CV ne mentionne pas Python et SQL, qui sont requis pour ce poste. Python est important pour le développement backend, et SQL est essentiel pour la gestion de bases de données.

Exemple 2 :
CV du candidat :
- Compétences : Python, TensorFlow, Git
Offre d'emploi :
- Compétences requises : Python, PyTorch, Docker

Évaluation :
- ✅ Langages de programmation : Présent (Python)
  - Le CV mentionne Python, ce qui correspond aux attentes de l'offre.
- ⚠️ Bibliothèques & Frameworks : Partiel (TensorFlow mentionné, mais PyTorch absent)
  - Le CV mentionne TensorFlow, mais PyTorch, qui est requis pour ce poste, est absent. PyTorch est important pour le développement de modèles de machine learning.
- ❌ Outils de développement : Absent (Docker)
  - Le CV ne mentionne pas Docker, qui est requis pour ce poste. Docker est essentiel pour le déploiement de conteneurs.

### Critères d'évaluation :

 1. Searchability (Visibilité & Mots-clés)
- Informations de contact : Vérifie la présence d’un e-mail, numéro de téléphone, profil LinkedIn, GitHub ou portfolio.
- Résumé (Summary/Profile) : Existe-t-il une section donnant une vue d’ensemble rapide du candidat et de ses objectifs ?
- Mots-clés métiers & techniques :Le CV inclut-il des termes spécifiques au poste ciblé (ex. Machine Learning, NLP, Deep Learning, XGBoost) ?
- Structure adaptée aux ATS (Applicant Tracking Systems) :
  - Utilisation de titres clairs et standards (ex. "Expérience professionnelle", "Compétences techniques").
  - Absence d’éléments pouvant poser problème pour les logiciels de recrutement (images, tableaux, colonnes).
- Lien vers des travaux/projets publics : Présence de liens vers des projets GitHub, publications, ou portfolio.

 2.Hard Skills (Compétences techniques)
- Compare les langages mentionnés dans le CV avec ceux requis dans l'offre.
  - Si un langage requis est absent, explique pourquoi il est important pour le poste.
- Bibliothèques & Frameworks : TensorFlow, PyTorch, Scikit-learn, etc. Bien indiqués ?
  - Compare les frameworks mentionnés dans le CV avec ceux requis dans l'offre.
  - Si un framework requis est absent, explique pourquoi il est important pour le poste.
- Outils de développement : Git, Docker, Kubernetes,Gitlab etc.
  - Compare les outils mentionnés dans le CV avec ceux requis dans l'offre.
  - Si un outil requis est absent, explique pourquoi il est important pour le poste.
- Bases de données : PostgreSQL, MongoDB, etc.
  - Compare les bases de données mentionnées dans le CV avec celles requises dans l'offre.
  - Si une base de données requise est absente, explique pourquoi elle est importante pour le poste.
- Déploiement & MLOps : Expérience avec AWS, GCP, Azure, ou CI/CD ?
  - Compare les compétences de déploiement mentionnées dans le CV avec celles requises dans l'offre.
  - Si une compétence requise est absente, explique pourquoi elle est importante pour le poste.
- Données et analyse : Dataiku, Tableau, Power BI, etc.
  - Compare les outils d'analyse de données mentionnés dans le CV avec ceux requis dans l'offre.
  - Si un outil requis est absent, explique pourquoi il est important pour le poste.
- Projets concrets :Les compétences techniques sont-elles démontrées à travers des réalisations spécifiques ?
  - Vérifie si les projets mentionnés dans le CV correspondent aux attentes de l'offre.

 3. Soft Skills (Compétences interpersonnelles)
- **Communication : Le CV est-il rédigé de manière claire et concise ? Présence d’un résumé efficace ?
- Travail en équipe : Mention de collaborations dans des projets de groupe ou en entreprise ?
- Gestion de projet : Expérience en gestion agile (Scrum, Kanban) ?
- Autonomie & auto-apprentissage : Indications sur la capacité à apprendre de nouveaux outils ou concepts ?
- Capacité d’adaptation : Transitions entre différents domaines ou technologies visibles ?

 4.Expérience professionnelle & Projets
- Détails des missions :Chaque expérience décrit-elle clairement les responsabilités et tâches effectuées ?
- Résultats mesurables : Impact du travail chiffré (ex. "Réduction du temps d’inférence de 30%", "Amélioration de l’accuracy de 10%") ?
- Expérience avec des données réelles : Manipulation de jeux de données volumineux, traitement de données textuelles ?
- Projets personnels :Contributions open source, Kaggle/Zindi, publications ?

 5. Formation & Certifications
- Diplômes :Master, PhD, ou certifications en data science, machine learning ?
- Certifications techniques : TensorFlow Developer, AWS Certified ML, Google Data Engineer ?
- Cours en ligne pertinents : Udacity, Coursera, DeepLearning.AI ?
- Thèses & publications : Articles publiés en lien avec le domaine ?

6. **Clarté & Lisibilité
- Bonne structuration : Sections bien séparées, titres en gras, listes à puces ?
- Hiérarchisation des informations : Les expériences et compétences les plus pertinentes sont-elles mises en avant ?
- Police et mise en page lisibles : Pas de surcharge d’informations, espace suffisant entre les éléments ?
- Longueur du CV adaptée :** Moins de 2 pages pour un junior, pas plus de 3 pour un senior ?

7. Personnalisation & Pertinence
- CV adapté au poste ciblé : Contenu pertinent pour l’emploi visé ?
- Résumé percutant :** Objectifs et forces du candidat mis en avant ?
- Adéquation entre expérience et job description :** Expériences alignées avec les attentes du poste ?

8. Impact & Résultats
- Utilisation de chiffres et résultats mesurables : Réduction de coûts, augmentation de performance, impact business mesuré ?
- Références à des réalisations significatives :Publications, brevets, modèles en production, leadership technique ?
- Distinctions & compétitions :Kaggle, Zindi, hackathons gagnés, récompenses professionnelles ?
 Format de sortie attendu :
- [EXTRACTION] Résumé structuré des informations du CV.
- [ÉVALUATION] Une analyse point par point avec ✅ (Présent), ⚠️ (Partiel) ou ❌ (Absent) pour chaque critère.
  - Pour chaque évaluation, explique clairement pourquoi tu as donné ✅, ⚠️, ou ❌.
  - Si un élément requis par l'offre est absent, explique pourquoi il est important et ce qui pourrait être ajouté.
- [CV AMÉLIORÉ] Proposition d'une version améliorée du CV.
"""

    client = Groq(api_key=groq_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Tu es un expert en recrutement."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content

# Interface utilisateur
with st.form("cv_evaluation_form"):
    st.subheader("1. Téléchargez votre CV")
    uploaded_file = st.file_uploader("Choisissez un fichier PDF", type="pdf", help="Seuls les fichiers PDF sont acceptés.")

    st.subheader("2. Description du poste")
    job_description = st.text_area("Collez la description du poste ici :", height=150, placeholder="Exemple : Nous recherchons un développeur Python avec 3 ans d'expérience...")

    # Bouton pour soumettre le formulaire
    submitted = st.form_submit_button("🚀 Évaluer le CV")

# Traitement après soumission du formulaire
if submitted:
    if not uploaded_file or not job_description:
        st.error("❌ Veuillez télécharger un fichier PDF et fournir une description de poste.")
    else:
        with st.spinner("🔍 Extraction du texte et analyse en cours..."):
            try:
                # Extraire le texte du PDF
                cv_text = extract_text_from_pdf(uploaded_file)
                
                # Afficher un aperçu du texte extrait
                with st.expander("Aperçu du texte extrait du CV"):
                    st.write(cv_text[:1000] + "...")  # Afficher les 1000 premiers caractères

                # Évaluer le CV
                evaluation = evaluate_cv(cv_text, job_description)
                
                # Afficher les résultats
                st.success("✅ Évaluation terminée !")
                st.markdown("---")
                st.subheader("📊 Résultat de l'évaluation")
                st.write(evaluation)
                
            except Exception as e:
                st.error(f"❌ Une erreur s'est produite : {e}")