@echo off

REM === Levantar backend Flask ===
start "" cmd /c "cd backend && python app.py"

REM === Levantar frontend Streamlit ===
start "" cmd /c "cd frontend && streamlit run app_streamlit.py --server.port 8501"
