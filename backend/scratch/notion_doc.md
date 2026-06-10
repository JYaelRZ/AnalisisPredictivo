Variables y rangos

## Edad
Primero definir el rango de edad, según INEGI

![image.png](attachment_placeholder)

![image.png](attachment_placeholder)
https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/edr/EDR2024_RR_ene-dic.pdf

## Rangos de edad 

| Característica | Jóvenes (18-29) | Tempranos (30-44) | Medios (45-54) | Mayores Tempranos (55-64) | Mayores (65-75) |
| --- | --- | --- | --- | --- | --- |
| Rango Edad (años) | 18-29 | 30-44 | 45-54 | 55-64 | 65-75 |
| Prevalencia ECV (%) | 5-10% | 10-15% | 20-30% | 30-40% | 40-50% |
| Poder Discriminativo | Baja | Media | ALTO | MUY ALTO | MUY ALTO (pero sesgado) |
| Utilidad Clínica | Baja (prevención extrema) | Media | ALTO | MUY ALTO | Alta (pero sesgo sobreviv.) |
| Balance Clase | Muy desbalanceado (90-10) | Desbalanceado (85-15) | Balanceado (70-30) | Balanceado (65-35) | Desbalanceado (50-50) |
| Eventos Esperados | Muy pocos | Pocos | Moderados | Abundantes | Muy abundantes |
| Tamaño Muestra Ideal | 2000-3000 | 1000-2000 | 1000-2000 | 1000-1500 | 300-1000 |
| Duración Recolección | 2-3 años | 1-2 años | <1 año | <1 año | <1 año |
| Aplicación Principal | Detección susceptibles | Validación externa | Entrenar core ML | Entrenar core ML | Validación + Prevención 2ª |
| RECOMENDACIÓN | ❌ Subóptimo | ✓ Complementario | ✓✓ ÓPTIMO | ✓✓ ÓPTIMO | ✓ Con precaución |

Analisis_Rango_Edad_Optimo.csv

> ℹ️ 
 Yo propongo de 45 a 54 años o en su defecto tomar desde los 18 

## RANGOS PARA BIOMARCADORES

### Jóvenes (18–29 años)

| Grupo / Parámetro | Jóvenes Hombres 18–29 | Jóvenes Mujeres 18–29 | Correlación Fisiopatológica Predominante |
| --- | --- | --- | --- |
| Colesterol total (mg/dL) | Normal: <200; Alto riesgo: ≥240 o ≥200 con otros FR. | Igual. | Inicio de dislipidemia aterogénica y síndrome metabólico ligado a obesidad, baja HDL y TG altos; base para aterosclerosis precoz. |
| LDL‑C (mg/dL) | Normal: <100; Alto riesgo: ≥160, muy alto: ≥190. | Igual. | Elevación de LDL desde edades tempranas acelera estrías grasas y placas subclínicas en coronarias y carótidas. |
| HDL‑C (mg/dL) | Normal: ≥40; Alto riesgo: <40. | Normal: ≥50; Alto riesgo: <50. | Hipoalfalipoproteinemia (HDL bajo) es muy frecuente en hombres mexicanos y se asocia a alto riesgo coronario. |
| Triglicéridos (mg/dL) | Normal: <150; Alto riesgo: ≥200; muy alto: ≥500. | Igual. | Hipertrigliceridemia refleja dieta occidentalizada y resistencia a la insulina; se vincula a hígado graso y pancreatitis si es muy elevada. |
| Glucosa ayuno (mg/dL) | Normal: 70–99; Alto riesgo: 100–125 (prediabetes), ≥126 (diabetes, confirmar). | Igual. | Resistencia a la insulina silente y prediabetes, muy prevalentes en jóvenes mexicanos con sobrepeso. |
| HbA1c (%) | Normal: <5.7; Alto riesgo: 5.7–6.4 (prediabetes), ≥6.5 (diabetes). | Igual. | Elevación temprana de HbA1c marca transición a diabetes tipo 2 y aumenta riesgo cardiovascular a largo plazo. |
| Insulina ayuno (µU/mL)* | Normal aproximado: ~2–15; Alto riesgo: >15–20 (con glucosa y TG altos). | Ligeramente menor, mismos cortes clínicos. | Resistencia a la insulina y síndrome metabólico en individuos con IMC elevado y circunferencia de cintura aumentada. |
| Creatinina (mg/dL) | Normal: 0.8–1.3; Alto riesgo: valores crecientes fuera de rango con TFG baja. | Normal: 0.6–1.1; Alto riesgo: elevación sostenida. | Nefropatía temprana asociada a malformaciones, nefritis o nefropatía incipiente por obesidad/HTA no diagnosticada. |
| Sodio (mEq/L) | Normal: 136–145; Alto riesgo: <130 o >150. | Igual. | Hiponatremia/hipernatremia se relacionan con alteraciones de volumen, SIADH, deshidratación o causas iatrogénicas. |
| Potasio (mEq/L) | Normal: 3.5–5.0; Alto riesgo: <3.0 o >5.5 (≥6.0 emergencia). | Igual. | Hipo/hiperkalemia predisponen a arritmias ventriculares potencialmente fatales incluso en jóvenes. |
| PA sistólica / diastólica (mmHg) | Normal: <120/<80; Alto riesgo: ≥130 o ≥80 (hipertensión). | Igual. | HTA incipiente en jóvenes ligada a obesidad, consumo de sodio y sedentarismo; se asocia a daño de órgano blanco subclínico. |
| SpO₂ (%) | Normal: 95–100; Alto riesgo: <94, crítico <90. | Igual. | Hipoxemia indica patología respiratoria, cardiopatía congénita o tromboembolia pulmonar en contexto de síntomas agudos. |
| PCR‑hs (mg/L) | Normal: <1 bajo riesgo; 1–3 moderado; Alto riesgo: >3. | Igual. | Inflamación crónica de bajo grado relacionada con obesidad, tabaquismo y dieta, que potencia el riesgo aterosclerótico. |
| Troponina I (convencional) | Normal: <0.04 ng/mL (≈<40 ng/L) o por debajo de 99 pctl del ensayo; cualquier elevación sobre el corte es patológica. | Igual (con posibles cortes algo menores en mujeres). | Elevación sugiere lesión miocárdica aguda (IAM tipo 1 o 2, miocarditis, etc.) aun en ausencia de factores de riesgo clásicos. |
| Dímero D (µg/L FEU) | Normal: <500; Alto riesgo: ≥500 con clínica compatible. | Igual. | Elevación con síntomas sugiere tromboembolia venosa o TEP, especialmente en usuarios de anticonceptivos o fumadores. |
| BNP (pg/mL) | Normal: <100; Alto riesgo: ≥100 sugiere IC aguda/crónica. | Igual. | IC aguda es rara pero posible (miocarditis, cardiomiopatías, tóxicos); BNP alto obliga a descartar disfunción ventricular. |
| NT‑proBNP (pg/mL) | Regla práctica IC aguda: <300 descarta IC; Alto riesgo: ≥300 en contexto agudo. | Igual. | Elevación refleja sobrecarga de pared ventricular, pudiendo indicar miocardiopatía familiar o secundaria a HTA severa. |


### Adultos Tempranos (30–44 años)

| Biomarcador | Hombres 30–44 Normal | Hombres 30–44 Alto riesgo / Patológico | Mujeres 30–44 Normal | Mujeres 30–44 Alto riesgo / Patológico | Correlación Fisiopatológica Predominante |
| --- | --- | --- | --- | --- | --- |
| Colesterol total | <200 | ≥240 o ≥200 con FR. | <200 | ≥240 o ≥200 con FR. | Consolidación de dislipidemia mixta y aumento claro del riesgo coronario. |
| LDL‑C | <100 (menor si alto riesgo). | ≥160 alto; ≥130 en pacientes de alto riesgo. | Igual. | Igual. | Aceleración de aterosclerosis en presencia de HTA, DM2 y tabaquismo. |
| HDL‑C | ≥40; <40 alto riesgo. | <40. | ≥50; <50 alto riesgo. | <50. | Hipo-HDL + TG elevados = fenotipo aterogénico típico en México. |
| Triglicéridos | <150 | ≥200; ≥500 muy alto. | <150 | ≥200; ≥500 muy alto. | Hígado graso y síndrome metabólico establecidos. |
| Glucosa ayuno | 70–99 | 100–125 prediabetes; ≥126 DM2. | Igual. | Igual. | Debut típico de DM2 en presencia de obesidad central. |
| HbA1c | <5.7 | 5.7–6.4 prediabetes; ≥6.5 DM2. | Igual. | Igual. | Mayor riesgo de ECV y nefropatía en años siguientes. |
| PCR‑hs | <1 bajo; 1–3 moderado. | >3 alto riesgo. | Igual. | Igual. | Inflamación crónica asociada a obesidad, tabaco y DM2, potenciando el riesgo CV. |
| PA | <120/<80 | ≥130/80 (ACC/AHA) o ≥140/90 (ESC). | Igual. | Igual. | Debut de HTA sostenida: inicio de daño de órgano blanco (VI, riñón). |
| SpO₂ | 95–100 | <94 anormal. | Igual. | Igual. | Mayor visibilidad de SAOS y EPOC en fumadores/obesos. |
| Insulina | ~2–15 | >15–20 con otros criterios de SM. | Igual. | Igual. | Síndrome metabólico completo, riesgo alto de DM2 y ECV. |
| Creatinina | 0.8–1.3 | Elevada con TFG <90–60 → ERC inicial. | 0.6–1.1 | Igual. | Nefropatía hipertensiva/diabética subclínica. |
| Sodio | 136–145 | <130 o >150. | Igual. | Igual. | Trastornos de volumen y fármacos (diuréticos, ISRS, etc.). |
| Potasio | 3.5–5.0 | <3.0 o >5.5. | Igual. | Igual. | Riesgo arrítmico (diuréticos, IECA/ARA II, IR). |
| Troponina I | <0.04 ng/mL o <99 pctl. | ≥0.04 ng/mL o ≥99 pctl. | Igual. | Igual. | IAM precoz, miocarditis y daño tipo 2 en sepsis/FA rápida. |
| Dímero D | <500 | ≥500 con clínica compatible. | Igual. | Igual. | TEP/TVP relacionad@s con inmovilidad, cáncer, trombofilia. |
| BNP | <100 | ≥100 sospecha de IC. | Igual. | Igual. | Aparición de IC aguda por HTA o cardiopatía isquémica. |
| NT‑proBNP | <300 | ≥300 IC aguda probable. | Igual. | Igual. | Diferencia disnea cardiaca vs respiratoria en urgencias. |


### Adultos Medios (45–54 años)

| Biomarcador | Hombres 45–54 Normal | Hombres 45–54 Alto riesgo / Patológico | Mujeres 45–54 Normal | Mujeres 45–54 Alto riesgo / Patológico | Correlación Fisiopatológica Predominante |
| --- | --- | --- | --- | --- | --- |
| Colesterol total | <200 | ≥240 o ≥200 con FR. | <200 | ≥240 o ≥200 con FR. | Debut típico de HTA y dislipidemia mixta con aterosclerosis clínicamente relevante. |
| LDL‑C | Objetivo habitual <100; en alto riesgo <70. | ≥130 en alto riesgo; ≥100 en muy alto riesgo (prevención secundaria). | Igual; posmenopausia incrementa LDL. | Igual. | Elevado riesgo de SCA y EVC si coexisten LDL alto, HTA y DM2. |
| HDL‑C | ≥40; <40 patológico. | <40. | ≥50; <50 patológico. | <50. | Disminución de HDL y aumento de TG en mujeres posmenopáusicas aumenta riesgo. |
| Triglicéridos | <150 | ≥200; ≥500 muy alto. | <150 | ≥200; ≥500 muy alto. | Hígado graso, SM y riesgo pancreatitis. |
| Glucosa ayuno | 70–99 | 100–125 IFG; ≥126 DM. | Igual. | Igual. | DM2 manifiesta, con aumento de riesgo de nefropatía y ECV. |
| HbA1c | <5.7 | 5.7–6.4; ≥6.5 DM. | Igual. | Igual. | Control glucémico subóptimo acelera daño micro/macrovascular. |
| PCR‑hs | <1 bajo; 1–3 moderado. | >3 alto. | Igual. | Igual. | Marcador de inflamación vascular asociado a alto riesgo de IAM y EVC. |
| PA | <120/<80 | ≥130/80 (ACC/AHA) o ≥140/90 (ESC). | Igual. | Igual. | HTA crónica con hipertrofia VI y rigidez arterial. |
| SpO₂ | 95–100 | <94. | Igual. | Igual. | EPOC y SAOS más prevalentes, contribuyendo a hipertensión pulmonar. |
| Insulina | ~2–15 | >15–20 con otros criterios de SM. | Igual. | Igual. | SM consolidado y riesgo alto de DM2 y ECV establecida. |
| Creatinina | 0.8–1.3 | Elevada con TFG <60 → ERC grado ≥3. | 0.6–1.1 | Igual. | Nefropatía diabética/hipertensiva frecuente. |
| Sodio | 136–145 | <130 o >150. | Igual. | Igual. | Descompensaciones hidroelectrolíticas en contexto de IC/IRC. |
| Potasio | 3.5–5.0 | <3.0 o >5.5. | Igual. | Igual. | Hiperkalemia por IECA/ARA II y ERC aumenta riesgo arrítmico. |
| Troponina I | <0.04 ng/mL o <99 pctl. | ≥0.04 ng/mL o ≥99 pctl. | Igual. | Igual. | Edad clásica de IAM con elevación de ST y NSTEMI. |
| Dímero D | <500 | ≥500 con síntomas. | Igual. | Igual. | Mayor incidencia de TEP/TVP posquirúrgico e inmovilización. |
| BNP | <100 | ≥100 sugiere IC (mayor valor → peor pronóstico). | Igual. | Igual. | Aparición de IC (FE reducida o preservada) por HTA y cardiopatía isquémica. |
| NT‑proBNP | <300 | ≥300 IC aguda; umbrales 450–900 según edad para IC crónica. | Igual. | Igual. | Aumento refleja sobrecarga de cavidades y riesgo de descompensación. |


### Mayores Tempranos (55–64 años)

| Biomarcador | Hombres 55–64 Normal | Hombres 55–64 Alto riesgo / Patológico | Mujeres 55–64 Normal | Mujeres 55–64 Alto riesgo / Patológico | Correlación Fisiopatológica Predominante |
| --- | --- | --- | --- | --- | --- |
| Colesterol total | <200 (en prevención secundaria se busca aún menos LDL, pero el “normal” de laboratorio no cambia). | ≥240 o ≥200 con ECV previa. | <200 | Igual. | Aterosclerosis calcificada y enfermedad coronaria/cerebrovascular establecida. |
| LDL‑C | En muy alto riesgo: objetivo <55–70; en laboratorio “normal” sigue <100. | ≥70 en muy alto riesgo; ≥100 en alto riesgo. | Igual. | Igual. | Fuerte asociación con eventos CV mayores, especialmente si coexiste PCR elevada. |
| HDL‑C | ≥40 | <40 | ≥50 | <50 | HDL bajo añade riesgo residual importante. |
| Triglicéridos | <150 | ≥200; ≥500 muy alto. | <150 | ≥200; ≥500 muy alto. | Dislipidemia aterogénica y riesgo de pancreatitis. |
| Glucosa ayuno | 70–99 | 100–125 IFG; ≥126 DM. | Igual. | Igual. | DM2 de larga evolución con complicaciones micro/macrovasculares. |
| HbA1c | <5.7 | ≥6.5 DM; objetivos de control individuales (ej. <7%). | Igual. | Igual. | HbA1c alta se asocia a progresión de ERC, retinopatía y eventos CV. |
| PCR‑hs | <1 bajo; 1–3 moderado. | >3 alto. | Igual. | Igual. | Inflamación vascular crónica y riesgo de eventos recurrentes. |
| PA | <120/<80 | ≥130/80 o ≥140/90 según guía; muchos tienen HTA estadio 2. | Igual. | Igual. | HTA de larga evolución con rigidez arterial y HFpEF. |
| SpO₂ | 95–100 | <94. | Igual. | Igual. | EPOC, SAOS y cardiopatía avanzada con hipoxemia crónica. |
| Insulina | ~2–15 (pero menos útil sola en DM2 larga). | >15–20 con SM; en DM avanzada puede ser baja por fallo secretor. | Igual. | Igual. | Resistencia a insulina residual y mayor riesgo de hipoglucemias en tratados. |
| Creatinina | 0.8–1.3 (rango de laboratorio igual, pero TFG suele ser menor). | Elevada con TFG <60 → ERC significativa. | 0.6–1.1 | Igual. | ERC estadio 3–4 frecuente, incrementa riesgo CV y modifica interpretación de BNP/troponina. |
| Sodio | 136–145 | <130 o >150. | Igual. | Igual. | Trastornos hidroelectrolíticos en IC, cirrosis o ERC. |
| Potasio | 3.5–5.0 | <3.0 o >5.5. | Igual. | Igual. | Hiperkalemia frecuente por IECA/ARA II/espironolactona + ERC, con riesgo de arritmias. |
| Troponina I | <0.04 ng/mL (o <99 pctl específico, p. ej., ~14 ng/L hs). | ≥0.04 ng/mL o ≥99 pctl: crítico. | Igual. | Igual. | IAM, IC descompensada y daño tipo 2 muy prevalentes. |
| Dímero D | <500 en <50 años; en este grupo usaredad ×10: p.ej., 60 años → 600 µg/L FEU. | ≥edad ×10 µg/L con clínica compatible se considera patológico. | Igual. | Igual. | Alta probabilidad de TEP/TVP en contexto de cáncer, inmovilidad, FA, etc. |
| BNP | <100 | ≥100 sugiere IC aguda; ≥300–400 aún más específico. | Igual. | Igual. | IC aguda descompensada (HFrEF/HFpEF) muy frecuente. |
| NT‑proBNP | <300 descarta IC aguda; en 50–75 años se suelen usar cortes diagnósticos alrededor de 900 pg/mL para IC. | ≥300 en urgencias, y ≥900 en 50–75 años, apoyan fuertemente IC. | Igual. | Igual. | Elevación marcada indica sobrecarga crónica y mal pronóstico. |


### Fuentes




### Estilo de vida




### Diccionario ECG (1–12 derivaciones)