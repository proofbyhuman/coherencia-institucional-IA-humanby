#!/usr/bin/env python3
"""
Coherencia Institucional — Backend Flask
Integra frontend estático + panel admin + generación de noticias actuales
"""

import os
import json
import random
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

# Almacenamiento en memoria para noticias
news_db = []

# Plantilla del frontend público
INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Coherencia Institucional — Inicio</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#EEF0EC;
    --card:#F7F8F5;
    --ink:#1A1D1B;
    --ink-soft:#5B5F58;
    --accent:#0F6E56;
    --line:rgba(26,29,27,.16);
    --pol:#2A4D6B;
    --cultura:#7A2A55;
    --eco:#6B5A1F;
    --geo:#4A2A6B;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:'Source Serif 4', Georgia, serif;-webkit-font-smoothing:antialiased;}
  .wrap{max-width:1080px;margin:0 auto;padding:0 28px 80px;}
  .masthead{padding:28px 0 22px;text-align:center;border-bottom:2px solid var(--ink);}
  .dateline{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.12em;color:var(--ink-soft);text-transform:uppercase;}
  .wordmark{font-size:48px;font-weight:700;margin:10px 0 6px;letter-spacing:-0.01em;}
  .tagline{font-style:italic;color:var(--ink-soft);font-size:15px;margin:0 0 18px;}
  .nav{display:flex;justify-content:center;gap:28px;font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;}
  .nav a{color:var(--ink);text-decoration:none;padding-bottom:4px;border-bottom:2px solid transparent;}
  .nav a:hover{border-bottom-color:var(--accent);}
  .hero{display:grid;grid-template-columns:1.3fr .9fr;gap:40px;padding:40px 0;border-bottom:1px solid var(--line);align-items:start;}
  .hero .tag{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#fff;background:var(--geo);padding:3px 9px;border-radius:2px;margin-bottom:14px;}
  .hero h2{font-size:38px;line-height:1.12;margin:0 0 14px;font-weight:700;}
  .hero .dek{font-size:17px;color:var(--ink-soft);line-height:1.55;margin:0 0 18px;}
  .byline{font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:var(--ink-soft);display:flex;flex-wrap:wrap;gap:6px;align-items:center;}
  .stamp{justify-self:end;border:2px solid var(--accent);color:var(--accent);font-family:'IBM Plex Mono',monospace;font-size:13px;letter-spacing:.14em;text-transform:uppercase;padding:14px 18px;transform:rotate(-7deg);text-align:center;line-height:1.5;}
  .stamp span{display:block;font-size:9.5px;letter-spacing:.1em;color:var(--ink-soft);text-transform:none;margin-top:4px;}
  .beat{padding:36px 0;border-bottom:1px solid var(--line);}
  .beat:last-of-type{border-bottom:none;}
  .beat-head{display:flex;align-items:center;gap:14px;margin-bottom:20px;}
  .beat-head .tag{font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;font-weight:500;}
  .beat-head .rule{flex:1;height:1px;background:var(--line);}
  .tag.politica{color:var(--pol);} .tag.cultura{color:var(--cultura);} .tag.economia{color:var(--eco);} .tag.geopolitica{color:var(--geo);}
  .cards{display:grid;grid-template-columns:repeat(2,1fr);gap:26px;}
  .card .thumb{height:120px;background:repeating-linear-gradient(45deg,var(--card),var(--card) 8px,#e4e6e0 8px,#e4e6e0 9px);border:1px solid var(--line);margin-bottom:12px;}
  .card h3{font-size:19px;line-height:1.3;margin:0 0 8px;}
  .card .dek{font-size:14px;color:var(--ink-soft);margin:0 0 10px;line-height:1.5;}
  .card .meta{font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:var(--ink-soft);display:flex;gap:6px;align-items:center;letter-spacing:.02em;}
  .card .meta .ok{color:var(--accent);}
  footer{padding:40px 0 0;}
  .foot-note{font-size:13px;color:var(--ink-soft);max-width:560px;line-height:1.6;margin:0 0 18px;}
  .sub{display:flex;gap:0;max-width:380px;}
  .sub input{flex:1;font-family:'IBM Plex Mono',monospace;font-size:12px;padding:10px 12px;border:1px solid var(--ink);border-right:none;background:var(--card);}
  .sub button{font-family:'IBM Plex Mono',monospace;font-size:12px;text-transform:uppercase;letter-spacing:.06em;padding:10px 16px;background:var(--ink);color:var(--paper);border:1px solid var(--ink);cursor:pointer;}
  @media (max-width:760px){
    .wordmark{font-size:38px;}
    .nav{gap:16px;flex-wrap:wrap;font-size:11px;}
    .hero{grid-template-columns:1fr;}
    .stamp{justify-self:start;}
    .cards{grid-template-columns:1fr;}
  }
</style>
</head>
<body>
<div class="wrap">
  <header class="masthead">
    <div class="dateline" id="dateline">Cargando fecha...</div>
    <h1 class="wordmark">Coherencia Institucional</h1>
    <p class="tagline">Periodismo de datos. Procesado por IA, gatekeeping humano.</p>
    <nav class="nav">
      <a href="#politica">Política</a><a href="#cultura">Cultura</a><a href="#economia">Economía</a><a href="#geopolitica">Geopolítica</a>
    </nav>
  </header>
  <section class="hero" id="hero-section">
    <div>
      <span class="tag" id="hero-tag">Geopolítica</span>
      <h2 id="hero-title">Cargando noticia principal...</h2>
      <p class="dek" id="hero-dek"></p>
      <div class="byline">
        <span>Agente 1: Fuentes cruzadas</span><span>·</span>
        <span>Agente 2: Redacción</span><span>·</span>
        <span>Agente 3: Distribución</span>
      </div>
    </div>
    <div class="stamp">Gatekeeper<span>Aprobado - Director Editorial</span></div>
  </section>
  <div id="news-container"></div>
  <footer>
    <p class="foot-note">Coherencia Institucional opera bajo un pipeline transparente. El Agente 1 audita hechos, el Agente 2 redacta, y el Director Editorial aplica el gatekeeping humano final para evitar sesgos y burbujas de filtro (Agente 3).</p>
    <div class="sub">
      <input type="email" placeholder="tu@email.com" />
      <button>Suscribirse</button>
    </div>
  </footer>
</div>
<script>
const categoryColors = { politica: '#2A4D6B', cultura: '#7A2A55', economia: '#6B5A1F', geopolitica: '#4A2A6B' };
const categoryNames = { politica: 'Política', cultura: 'Cultura', economia: 'Economía', geopolitica: 'Geopolítica' };

function formatDate(date) {
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleDateString('es-ES', options) + ' — Buenos Aires';
}

function formatTime(date) {
  return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
}

async function loadNews() {
  try {
    const res = await fetch('/api/news');
    const news = await res.json();
    const now = new Date();
    document.getElementById('dateline').textContent = formatDate(now);
    
    if (news.length === 0) {
      document.getElementById('hero-title').textContent = 'No hay noticias disponibles';
      return;
    }
    
    const hero = news[0];
    document.getElementById('hero-tag').textContent = categoryNames[hero.category];
    document.getElementById('hero-tag').style.background = categoryColors[hero.category];
    document.getElementById('hero-title').textContent = hero.title;
    document.getElementById('hero-dek').textContent = hero.summary;
    
    const categories = ['politica', 'cultura', 'economia', 'geopolitica'];
    const container = document.getElementById('news-container');
    let html = '';
    
    categories.forEach(cat => {
      const catNews = news.filter(n => n.category === cat && n !== news[0]);
      if (catNews.length > 0) {
        html += '<section class="beat" id="' + cat + '"><div class="beat-head"><span class="tag ' + cat + '" style="color:' + categoryColors[cat] + '">' + categoryNames[cat] + '</span><span class="rule"></span></div><div class="cards">';
        catNews.forEach(item => {
          html += '<article class="card"><div class="thumb"></div><h3>' + item.title + '</h3><p class="dek">' + item.summary + '</p><div class="meta"><span class="ok">✓ Verificado</span><span>·</span><span>Agente 3</span><span>·</span><span>' + formatTime(new Date(item.timestamp)) + '</span></div></article>';
        });
        html += '</div></section>';
      }
    });
    
    container.innerHTML = html;
  } catch (err) {
    console.error('Error loading news:', err);
  }
}

loadNews();
setInterval(loadNews, 60000);
</script>
</body>
</html>'''

# Plantilla del panel admin
ADMIN_TEMPLATE = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Coherencia Institucional — Panel Editorial</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#EEF0EC;
    --card:#FFFFFF;
    --ink:#1A1D1B;
    --ink-soft:#5B5F58;
    --accent:#0F6E56;
    --line:rgba(26,29,27,.14);
    --tec:#2A4D6B; --arte:#7A2A55; --eco:#6B5A1F; --geo:#4A2A6B;
    --ok:#1E7A4C; --pend:#B8860B; --alert:#B23A2E;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:'IBM Plex Mono',monospace;font-size:13px;}
  h1,h2,h3{font-family:'Source Serif 4',Georgia,serif;margin:0;}
  .app{display:grid;grid-template-columns:230px 1fr;min-height:100vh;}
  .side{background:var(--ink);color:var(--paper);padding:26px 20px;}
  .side .brand{font-family:'Source Serif 4',serif;font-size:18px;font-weight:700;margin-bottom:2px;line-height:1.2;}
  .side .sub{font-size:11px;color:#9A9D95;margin-bottom:30px;letter-spacing:.04em;margin-top:6px;}
  .side nav a{display:block;font-size:12.5px;letter-spacing:.03em;color:#C7C9C1;text-decoration:none;padding:10px 0 10px 12px;border-left:2px solid transparent;margin-bottom:2px;}
  .side nav a.active{color:var(--paper);border-left-color:var(--accent);background:rgba(255,255,255,.04);}
  .side nav a:hover{color:var(--paper);}
  .main{padding:32px 36px;}
  .top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;}
  .top h1{font-size:26px;}
  .date{color:var(--ink-soft);font-size:11.5px;}
  .filters{display:flex;gap:8px;margin:18px 0 26px;flex-wrap:wrap;}
  .chip{font-size:11px;padding:5px 12px;border:1px solid var(--line);border-radius:14px;background:var(--card);color:var(--ink-soft);cursor:pointer;}
  .chip.active{border-color:var(--ink);color:var(--ink);font-weight:500;}
  .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:30px;}
  .stat{background:var(--card);border:1px solid var(--line);padding:14px 16px;}
  .stat .label{font-size:10.5px;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;}
  .stat .num{font-family:'Source Serif 4',serif;font-size:26px;font-weight:600;}
  .stat.alert .num{color:var(--alert);}
  .stat.ok .num{color:var(--ok);}
  .list{display:flex;flex-direction:column;gap:1px;border:1px solid var(--line);background:var(--line);}
  .row{display:grid;grid-template-columns:4px 1fr 130px 200px;align-items:center;background:var(--card);}
  .bar.politica{background:var(--tec);} .bar.cultura{background:var(--arte);} .bar.economia{background:var(--eco);} .bar.geopolitica{background:var(--geo);}
  .row .info{padding:14px 18px;}
  .row .info .tag{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-soft);}
  .row .info h3{font-size:15.5px;margin:4px 0 5px;line-height:1.3;}
  .row .info .meta{font-size:10.5px;color:var(--ink-soft);}
  .status{font-size:11px;padding:5px 10px;border-radius:3px;justify-self:start;}
  .status.ok{background:#E4F1E9;color:var(--ok);}
  .status.pend{background:#FBF1DD;color:var(--pend);}
  .status.alert{background:#FAE6E3;color:var(--alert);}
  .actions{display:flex;gap:6px;padding-right:16px;justify-self:end;}
  .actions button{font-family:'IBM Plex Mono',monospace;font-size:11px;padding:6px 10px;border:1px solid var(--line);background:var(--card);cursor:pointer;}
  .actions button.approve{border-color:var(--ok);color:var(--ok);}
  .actions button.reject{border-color:var(--alert);color:var(--alert);}
  .detail{background:var(--card);border:1px solid var(--line);border-top:none;padding:16px 18px 18px 22px;font-size:11.5px;color:var(--ink-soft);display:grid;grid-template-columns:repeat(3,1fr);gap:18px;}
  .detail div b{display:block;color:var(--ink);font-size:11px;margin-bottom:4px;font-weight:500;}
  .generate-btn{background:var(--accent);color:var(--paper);border:none;padding:8px 16px;cursor:pointer;font-family:'IBM Plex Mono',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.06em;}
  .generate-btn:hover{opacity:0.9;}
  @media (max-width:820px){
    .app{grid-template-columns:1fr;}
    .side{display:flex;align-items:center;gap:18px;padding:14px 18px;}
    .side .sub{display:none;}
    .side nav{display:flex;gap:14px;}
    .side nav a{padding:0;border-left:none;border-bottom:2px solid transparent;}
    .side nav a.active{border-bottom-color:var(--accent);border-left:none;background:none;}
    .stats{grid-template-columns:repeat(2,1fr);}
    .row{grid-template-columns:4px 1fr;}
    .status,.actions{display:none;}
    .detail{grid-template-columns:1fr;}
  }
</style>
</head>
<body>
<div class="app">
  <aside class="side">
    <div class="brand">Coherencia<br>Institucional</div>
    <div class="sub">Panel del Director Editorial</div>
    <nav>
      <a href="#" class="active">Bandeja de revisión</a>
      <a href="/">Ver Sitio Público</a>
      <a href="#">Métricas de Audiencia</a>
      <a href="#">Filtros Antisesgo</a>
    </nav>
  </aside>
  <main class="main">
    <div class="top">
      <h1>Gatekeeping / Bandeja de revisión</h1>
      <span class="date" id="current-date"></span>
    </div>
    <div class="filters">
      <span class="chip active">Todas</span>
      <span class="chip">Política</span>
      <span class="chip">Cultura</span>
      <span class="chip">Economía</span>
      <span class="chip">Geopolítica</span>
      <button class="generate-btn" onclick="generateNews()" style="margin-left:auto;">🔄 Generar Noticias</button>
    </div>
    <div class="stats">
      <div class="stat"><div class="label">Borradores en cola</div><div class="num" id="stat-drafts">0</div></div>
      <div class="stat ok"><div class="label">Publicados hoy</div><div class="num" id="stat-published">0</div></div>
      <div class="stat"><div class="label">Tasa de aprobación</div><div class="num" id="stat-rate">0%</div></div>
      <div class="stat alert"><div class="label">Alertas de fact-check</div><div class="num" id="stat-alerts">0</div></div>
    </div>
    <div class="list" id="news-list"></div>
  </main>
</div>
<script>
const categoryColors = { politica: '#2A4D6B', cultura: '#7A2A55', economia: '#6B5A1F', geopolitica: '#4A2A6B' };
const categoryNames = { politica: 'Política', cultura: 'Cultura', economia: 'Economía', geopolitica: 'Geopolítica' };

function formatDate(date) {
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleDateString('es-ES', options) + ' · ' + date.toLocaleTimeString('es-ES', {hour:'2-digit',minute:'2-digit'});
}

function formatTime(date) {
  return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
}

async function loadNews() {
  try {
    const res = await fetch('/api/news');
    const news = await res.json();
    
    document.getElementById('current-date').textContent = formatDate(new Date());
    
    const drafts = news.filter(n => n.status === 'draft').length;
    const published = news.filter(n => n.status === 'approved').length;
    const alerts = news.filter(n => n.status === 'alert').length;
    const rate = news.length > 0 ? Math.round((published / news.length) * 100) : 0;
    
    document.getElementById('stat-drafts').textContent = drafts;
    document.getElementById('stat-published').textContent = published;
    document.getElementById('stat-rate').textContent = rate + '%';
    document.getElementById('stat-alerts').textContent = alerts;
    
    const list = document.getElementById('news-list');
    let html = '';
    
    news.forEach(function(item) {
      var statusClass = 'pend';
      var statusText = '⏳ Procesando NLP';
      if (item.status === 'approved') { statusClass = 'ok'; statusText = '✓ Verificado'; }
      if (item.status === 'alert') { statusClass = 'alert'; statusText = '⚠ Alerta de Desinformación'; }
      
      html += '<div class="row"><div class="bar ' + item.category + '"></div><div class="info"><span class="tag">' + categoryNames[item.category] + '</span><h3>' + item.title + '</h3><span class="meta">Agente 2 (Redactor) · borrador · ingresó ' + formatTime(new Date(item.timestamp)) + '</span></div><span class="status ' + statusClass + '">' + statusText + '</span><div class="actions"><button onclick="auditNews(\\'' + item.id + '\\')">Auditar</button><button class="approve" onclick="approveNews(\\'' + item.id + '\\')">Aprobar</button><button class="reject" onclick="rejectNews(\\'' + item.id + '\\')">Rechazar</button></div></div>';
      html += '<div class="detail"><div><b>Entidades extraídas (Agente 1)</b>' + (item.entities || '3 entidades clave, 2 cifras verificadas') + '</div><div><b>Fuentes cruzadas</b>' + (item.sources || '8 registros oficiales y de prensa') + '</div><div><b>Evaluación de sesgo</b>' + (item.bias || '88% de neutralidad — sin discrepancias semánticas') + '</div></div>';
    });
    
    list.innerHTML = html;
  } catch (err) {
    console.error('Error loading news:', err);
  }
}

async function generateNews() {
  try {
    await fetch('/api/generate-news', { method: 'POST' });
    loadNews();
  } catch (err) {
    console.error('Error generating news:', err);
  }
}

async function approveNews(id) {
  try {
    await fetch('/api/news/' + id + '/approve', { method: 'POST' });
    loadNews();
  } catch (err) {
    console.error('Error approving news:', err);
  }
}

async function rejectNews(id) {
  try {
    await fetch('/api/news/' + id + '/reject', { method: 'POST' });
    loadNews();
  } catch (err) {
    console.error('Error rejecting news:', err);
  }
}

async function auditNews(id) {
  alert('Auditando noticia... (funcionalidad demo)');
}

document.querySelectorAll('.chip').forEach(function(chip) {
  chip.addEventListener('click', function() {
    document.querySelectorAll('.chip').forEach(function(c) { c.classList.remove('active'); });
    chip.classList.add('active');
  });
});

loadNews();
setInterval(loadNews, 30000);
</script>
</body>
</html>'''


def get_current_date_spanish():
    """Retorna la fecha actual formateada en español"""
    months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
              'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    weekdays = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    now = datetime.now()
    weekday = weekdays[now.weekday()]
    month = months[now.month - 1]
    return f"{weekday} {now.day} de {month} de {now.year}"


def generate_news_item(category, topic_keywords):
    """Genera una noticia simulada basada en categoría"""
    titles = {
        'politica': [
            f"Nuevas medidas de {topic_keywords} generan debate en el congreso",
            f"Reforma de {topic_keywords} avanza hacia votación definitiva",
            f"Ministro anuncia cambios en política de {topic_keywords}",
            f"Oposición critica manejo gubernamental de {topic_keywords}",
        ],
        'cultura': [
            f"Museos adoptan tecnología para preservar {topic_keywords}",
            f"Festival de {topic_keywords} atrae visitantes internacionales",
            f"Debate sobre patrimonio cultural y {topic_keywords}",
            f"Nueva exposición explora intersección de arte y {topic_keywords}",
        ],
        'economia': [
            f"Mercados reaccionan ante anuncios sobre {topic_keywords}",
            f"Expertos proyectan impacto de {topic_keywords} en inflación",
            f"Inversiones en sector de {topic_keywords} crecen un 15%",
            f"Banco central evalúa medidas relacionadas con {topic_keywords}",
        ],
        'geopolitica': [
            f"Tensiones internacionales por recursos de {topic_keywords}",
            f"Alianzas estratégicas se reconfiguran alrededor de {topic_keywords}",
            f"Cumbre global aborda desafíos de {topic_keywords}",
            f"Análisis: cómo {topic_keywords} redefine balances de poder",
        ]
    }
    
    summaries = {
        'politica': [
            "Legisladores de diversos partidos presentan posturas encontradas mientras se acerca la fecha de votación.",
            "La propuesta incluye modificaciones sustanciales que podrían transformar el panorama institucional.",
            "Analistas señalan implicaciones a largo plazo para la gobernabilidad democrática.",
        ],
        'cultura': [
            "Instituciones tradicionales buscan equilibrar preservación con innovación digital.",
            "Especialistas destacan importancia de hacer accesible el patrimonio a nuevas generaciones.",
            "La iniciativa cuenta con apoyo de organizaciones internacionales dedicadas a la cultura.",
        ],
        'economia': [
            "Indicadores económicos muestran señales mixtas en medio de incertidumbre global.",
            "Empresarios solicitan claridad regulatoria para planificar inversiones a mediano plazo.",
            "Economistas advierten sobre posibles efectos en cadena para sectores relacionados.",
        ],
        'geopolitica': [
            "Observadores internacionales monitorean evolución de negociaciones multilaterales.",
            "Expertos analizan implicaciones estratégicas para regiones adyacentes.",
            "La situación refleja tendencias más amplias en relaciones internacionales contemporáneas.",
        ]
    }
    
    title = random.choice(titles[category])
    summary = random.choice(summaries[category])
    
    minutes_ago = random.randint(5, 180)
    timestamp = datetime.now() - timedelta(minutes=minutes_ago)
    
    statuses = ['approved', 'approved', 'approved', 'draft', 'draft']
    status = random.choice(statuses)
    
    return {
        'id': f"news-{datetime.now().timestamp()}-{random.randint(1000,9999)}",
        'category': category,
        'title': title,
        'summary': summary,
        'timestamp': timestamp.isoformat(),
        'status': status,
        'entities': f"{random.randint(2,5)} entidades clave, {random.randint(1,4)} cifras verificadas",
        'sources': f"{random.randint(5,20)} registros oficiales y de prensa",
        'bias': f"{random.randint(75,98)}% de neutralidad — sin discrepancias semánticas"
    }


def generate_fresh_news():
    """Genera noticias actuales basadas en temas genéricos"""
    topics = {
        'politica': ['transparencia institucional', 'reforma electoral', 'políticas públicas', 'gestión gubernamental'],
        'cultura': ['expresiones artísticas', 'patrimonio histórico', 'industrias creativas', 'diversidad cultural'],
        'economia': ['mercados emergentes', 'innovación tecnológica', 'comercio internacional', 'desarrollo sostenible'],
        'geopolitica': ['cooperación regional', 'seguridad energética', 'cadenas de suministro', 'diplomacia multilateral']
    }
    
    news_list = []
    for category, keywords_list in topics.items():
        num_articles = random.randint(2, 4)
        for _ in range(num_articles):
            keyword = random.choice(keywords_list)
            news_list.append(generate_news_item(category, keyword))
    
    news_list.sort(key=lambda x: x['timestamp'], reverse=True)
    return news_list


@app.route('/')
def index():
    """Sirve el frontend público"""
    return render_template_string(INDEX_TEMPLATE)


@app.route('/admin')
def admin():
    """Sirve el panel de administración"""
    return render_template_string(ADMIN_TEMPLATE)


@app.route('/admin.html')
def admin_html():
    """Redirige admin.html al endpoint /admin"""
    return admin()


@app.route('/index.html')
def index_html():
    """Redirige index.html al endpoint /"""
    return index()


@app.route('/api/news', methods=['GET'])
def get_news():
    """API para obtener noticias"""
    global news_db
    if not news_db:
        news_db = generate_fresh_news()
    return jsonify(news_db)


@app.route('/api/generate-news', methods=['POST'])
def api_generate_news():
    """API para generar nuevas noticias"""
    global news_db
    news_db = generate_fresh_news()
    return jsonify({'status': 'success', 'count': len(news_db)})


@app.route('/api/news/<news_id>/approve', methods=['POST'])
def approve_news(news_id):
    """Aprueba una noticia"""
    global news_db
    for news in news_db:
        if news['id'] == news_id:
            news['status'] = 'approved'
            return jsonify({'status': 'success'})
    return jsonify({'status': 'not_found'}), 404


@app.route('/api/news/<news_id>/reject', methods=['POST'])
def reject_news(news_id):
    """Rechaza una noticia"""
    global news_db
    for news in news_db:
        if news['id'] == news_id:
            news['status'] = 'rejected'
            return jsonify({'status': 'success'})
    return jsonify({'status': 'not_found'}), 404


if __name__ == '__main__':
    print("=" * 60)
    print("Coherencia Institucional — Servidor Flask")
    print("=" * 60)
    print(f"Fecha: {get_current_date_spanish()}")
    print("-" * 60)
    print("Endpoints disponibles:")
    print("  • Frontend público: http://localhost:5000/")
    print("  • Panel Admin:      http://localhost:5000/admin")
    print("  • API Noticias:     http://localhost:5000/api/news")
    print("-" * 60)
    print("Iniciando servidor...")
    print("=" * 60)
    
    news_db = generate_fresh_news()
    print(f"\n✓ {len(news_db)} noticias generadas automáticamente")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
