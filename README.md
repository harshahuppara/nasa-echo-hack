# 🌌 NASA Echo: Solar System, Mars, Moon & Deep Space Interactive Explorer

An interactive, 3D educational web application powered by **Streamlit**, **Three.js**, **Google Gemini AI**, **NASA Open Data APIs**, and **Supabase**.

Explore planetary bodies, monuments of human spaceflight, authentic 3D models of rovers and orbiters, curated NASA mission archives, historical voiceovers, and live conversational AI chatbots embodying the spacecraft themselves.

---

## ✨ Features

- 🪐 **Interactive 3D Solar System & Deep Space Explorer**:
  - Full planetary orbits with Three.js rendering and dynamic lighting.
  - Seamless cinematic warp transition into **Deep Space** to inspect historic exploration missions (Dawn, New Horizons, Voyager 1, Voyager 2, Pioneer 10, Pioneer 11).
- 🔴 **Mars Surface & Monument Explorer**:
  - Interactive 3D Martian globe highlighting historic landing sites and exploration monuments.
  - Authentic 3D GLB models with OrbitControls for **Opportunity**, **Viking 1**, and **Ingenuity**.
  - Integrated **NASA Mission Photography & Media Studio** for all Martian spacecraft with high-resolution imagery and telemetry.
- 🌕 **Moon Explorer**:
  - Lunar landing sites (Apollo, Surveyor, Luna, Chandrayaan).
  - Authentic audio narratives, mission metadata, and high-definition photography.
- 🤖 **Gemini First-Person AI Chatbot**:
  - Conversational AI powered by Google Gemini, speaking directly in the first person as each spacecraft (*"I arrived at Meridiani Planum in 2004..."*).
  - Grounded with live telemetry from NASA Open Archives and Supabase.
  - Multi-tone audience selector (Junior Explorer vs. Senior Space Enthusiast).
- 🎙️ **Voiceover Mission Audio Narratives**:
  - Authentic historical and narrative audio stories for missions across the Solar System, Moon, Mars, and Deep Space.

---

## 🛠️ Tech Stack

- **Backend / Web Framework**: Python 3, [Streamlit](https://streamlit.io/)
- **Frontend / 3D Graphics**: HTML5, Modern CSS3, [Three.js](https://threejs.org/) (WebGL), OrbitControls, DRACOLoader
- **Artificial Intelligence**: [Google Gemini AI API](https://ai.google.dev/) (Flash / Pro)
- **Database & Telemetry**: [Supabase](https://supabase.com/) PostgreSQL
- **NASA Archives**: NASA Image and Video Library API (`images-api.nasa.gov`), NASA APOD API

---

## 🚀 Getting Started Locally

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/nasa-echo-hack.git
cd nasa-echo-hack
```

### 2. Set Up Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
NASA_API_KEY=your_nasa_api_key_here
```

### 5. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🌐 Deployment on Streamlit Community Cloud

1. Push this repository to your GitHub account.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **"New app"** and select your repository, branch (`main`), and main file path (`app.py`).
4. In **Advanced Settings ➔ Secrets**, configure your keys:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key"
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_KEY = "your_supabase_anon_key"
   NASA_API_KEY = "your_nasa_api_key"
   ```
5. Click **Deploy**!

---

## 📜 License
Distributed under the MIT License. Built for the NASA Space Apps / Echo Hack challenge.
