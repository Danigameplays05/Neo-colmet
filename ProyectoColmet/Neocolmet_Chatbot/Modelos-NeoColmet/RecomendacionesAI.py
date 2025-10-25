import PyPDF2
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import spacy
import re
from typing import Dict, List, Tuple
import streamlit as st
import plotly.express as px
import google.generativeai as genai

# Inicializar el estado de la sesión
if 'GEMINI_API_KEY' not in st.session_state:
    st.session_state['GEMINI_API_KEY'] = ''

class ICFESAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("es_core_news_sm")
        
    def configure_gemini(self):
        """Configura el modelo de Gemini."""
        if st.session_state['GEMINI_API_KEY']:
            genai.configure(api_key=st.session_state['GEMINI_API_KEY'])
            return True
        return False
        
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extrae texto de un archivo PDF."""
        try:
            # Crear un lector de PDF
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            
            # Extraer texto de cada página
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            # Debug: Mostrar el texto extraído
            st.text("Texto extraído del PDF (para debug):")
            st.code(text)
            
            if not text.strip():
                st.error("No se pudo extraer texto del PDF. El archivo podría estar protegido o en un formato no compatible.")
                return ""
                
            return text
            
        except Exception as e:
            st.error(f"Error detallado al leer el PDF: {str(e)}")
            st.error("Tipo de error: " + str(type(e).__name__))
            return ""

    def parse_mprov_results(self, text: str) -> Dict[str, Dict]:
        """Parsea los resultados específicos del formato M-PROVE."""
        results = {
            'matematicas': {'puntaje': 0, 'nivel': ''},
            'lectura_critica': {'puntaje': 0, 'nivel': ''},
            'sociales': {'puntaje': 0, 'nivel': ''},
            'ciencias_naturales': {'puntaje': 0, 'nivel': ''},
            'ingles': {'puntaje': 0, 'nivel': ''}
        }
        
        # Buscar el puntaje global
        global_match = re.search(r'Puntaje Global\s*(\d+)/500', text, re.IGNORECASE)
        if global_match:
            global_score = int(global_match.group(1))
            st.markdown(f"### 📊 Puntaje Global: {global_score}/500")

        # Buscar los puntajes directamente
        puntajes = re.findall(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', text)
        if puntajes:
            # Tomar el primer conjunto de 5 números encontrados
            numeros = puntajes[0]
            results['matematicas']['puntaje'] = int(numeros[0])
            results['lectura_critica']['puntaje'] = int(numeros[1])
            results['sociales']['puntaje'] = int(numeros[2])
            results['ciencias_naturales']['puntaje'] = int(numeros[3])
            results['ingles']['puntaje'] = int(numeros[4])
            
            # Asignar niveles basados en los puntajes
            for subject in results:
                score = results[subject]['puntaje']
                results[subject]['nivel'] = 'CONSOLIDADO' if score >= 80 else 'DESARROLLO'

        encontrados = []
        no_encontrados = []
        
        # Mostrar resultados encontrados
        for subject, data in results.items():
            if data['puntaje'] > 0:
                nombre_materia = subject.replace('_', ' ').title()
                emoji = "🌟" if data['nivel'] == "CONSOLIDADO" else "📈"
                encontrados.append(f"{emoji} {nombre_materia}: {data['puntaje']} - {data['nivel']}")
            else:
                nombre_materia = subject.replace('_', ' ').title()
                no_encontrados.append(nombre_materia)

        # Mostrar resultados en forma organizada
        if encontrados:
            st.markdown("### 📝 Resultados por área:")
            for resultado in encontrados:
                st.success(resultado)
        
        if no_encontrados:
            st.warning("### ⚠️ No se pudieron procesar los siguientes puntajes:")
            for materia in no_encontrados:
                st.warning(f"❌ {materia}")
                
        return results
    
    def get_level(self, score: int) -> str:
        """Determina el nivel basado en el puntaje."""
        if score >= 80:
            return "CONSOLIDADO"
        elif score >= 60:
            return "DESARROLLO"
        else:
            return "INICIAL"

    def generate_practice_questions(self, subject: str, weaknesses: List[str]) -> List[str]:
        """Genera preguntas de práctica usando Gemini."""
        if not self.configure_gemini():
            return ["Por favor, configura tu API key de Gemini para generar preguntas de práctica."]
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"""Genera 3 preguntas de práctica tipo ICFES para {subject} enfocadas en las siguientes debilidades:
            {', '.join(weaknesses)}
            
            Las preguntas deben:
            1. Ser del estilo ICFES (opción múltiple)
            2. Incluir 4 opciones de respuesta (A, B, C, D)
            3. Indicar la respuesta correcta
            4. Incluir una breve explicación de por qué es la respuesta correcta
            
            Formato deseado para cada pregunta:
            
            Pregunta X:
            [Enunciado de la pregunta]
            
            A) [Opción A]
            B) [Opción B]
            C) [Opción C]
            D) [Opción D]
            
            Respuesta correcta: [Letra]
            
            Explicación:
            [Explicación detallada de por qué es la respuesta correcta]
            """
            
            response = model.generate_content(prompt)
            return [response.text]
        except Exception as e:
            return [f"Error al generar preguntas: {str(e)}"]

    def analyze_results(self, results: Dict[str, Dict]) -> List[str]:
        """Genera recomendaciones basadas en los resultados."""
        recommendations = []
        
        for subject, data in results.items():
            score = data['puntaje']
            nivel = data['nivel']
            
            if nivel == "INICIAL":
                recommendations.append(
                    f"📚 {subject.replace('_', ' ').title()}: Necesitas reforzar significativamente esta área. "
                    f"Puntaje actual: {score}. Recomendamos:"
                    f"\n   - Buscar tutoría especializada"
                    f"\n   - Practicar ejercicios básicos diariamente"
                    f"\n   - Revisar conceptos fundamentales"
                )
            elif nivel == "DESARROLLO":
                recommendations.append(
                    f"📈 {subject.replace('_', ' ').title()}: Vas por buen camino pero hay espacio para mejorar. "
                    f"Puntaje actual: {score}. Recomendamos:"
                    f"\n   - Practicar ejercicios de dificultad media"
                    f"\n   - Identificar temas específicos para mejorar"
                    f"\n   - Realizar simulacros periódicamente"
                )
            else:  # CONSOLIDADO
                recommendations.append(
                    f"🌟 {subject.replace('_', ' ').title()}: ¡Excelente nivel! "
                    f"Puntaje actual: {score}. Recomendamos:"
                    f"\n   - Mantener el ritmo de estudio"
                    f"\n   - Ayudar a otros estudiantes"
                    f"\n   - Explorar temas avanzados"
                )
        
        return recommendations

def main():
    st.set_page_config(page_title="Analizador de Resultados ICFES", page_icon="📊", layout="wide")
    
    st.title("📊 Analizador de Resultados ICFES M-PROVE")
    st.markdown("""
    Esta aplicación analiza los resultados de simulacros ICFES de M-PROVE y genera:
    - Análisis detallado por área
    - Recomendaciones personalizadas
    - Preguntas de práctica para reforzar áreas débiles
    """)
    
    # Configuración de Gemini API Key
    with st.sidebar:
        st.session_state['GEMINI_API_KEY'] = st.text_input(
            "Google Gemini API Key", 
            value=st.session_state['GEMINI_API_KEY'], 
            type="password",
            help="Necesaria para generar preguntas de práctica. Obtén una gratis en: https://makersuite.google.com/app/apikey"
        )
    
    uploaded_file = st.file_uploader("Sube tu archivo PDF con los resultados de M-PROVE", type="pdf")
    
    if uploaded_file is not None:
        analyzer = ICFESAnalyzer()
        
        # Extraer texto del PDF
        text = analyzer.extract_text_from_pdf(uploaded_file)
        
        if text:
            try:
                # Analizar resultados
                results = analyzer.parse_mprov_results(text)
                
                # Crear y mostrar gráfica
                areas = ['Matemáticas', 'Lectura Crítica', 'Sociales', 'Ciencias Naturales', 'Inglés']
                puntajes = [
                    results['matematicas']['puntaje'],
                    results['lectura_critica']['puntaje'],
                    results['sociales']['puntaje'],
                    results['ciencias_naturales']['puntaje'],
                    results['ingles']['puntaje']
                ]
                
                df = pd.DataFrame({'Área': areas, 'Puntaje': puntajes})
                
                fig = px.bar(df, x='Área', y='Puntaje')
                
                fig.update_layout(
                    title='Puntajes por Área',
                    yaxis_range=[0, 100],
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                fig.update_traces(
                    text=df['Puntaje'],
                    textposition='outside'
                )
                
                st.plotly_chart(fig)
                
                # Mostrar recomendaciones
                st.subheader("Recomendaciones Personalizadas")
                recommendations = analyzer.analyze_results(results)
                for rec in recommendations:
                    st.info(rec)
                
                # Generar preguntas de práctica
                st.subheader("Preguntas de Práctica Personalizadas")
                if st.session_state['GEMINI_API_KEY']:
                    for subject, data in results.items():
                        if data['nivel'] != 'CONSOLIDADO' and data['puntaje'] > 0:
                            st.write(f"### Preguntas para {subject.replace('_', ' ').title()}")
                            questions = analyzer.generate_practice_questions(
                                subject, 
                                ["Mejorar comprensión básica", "Practicar ejercicios fundamentales"]
                            )
                            for q in questions:
                                st.markdown(q)
                else:
                    st.warning("Configura tu API key de Google Gemini para generar preguntas de práctica personalizadas.")
                
            except Exception as e:
                st.error("Ocurrió un error al procesar el PDF. Por favor, asegúrate de que el archivo tenga el formato correcto.")

if __name__ == "__main__":
    main()
