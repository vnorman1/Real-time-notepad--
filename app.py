#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real-time Notepad Application
Egy valós idejű jegyzetblokk alkalmazás WebSocket-tel és automatikus mentéssel
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json
import os
import datetime
from threading import Lock
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'notepad-secret-key-2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Thread lock a biztonságos fájl műveletekhez
file_lock = Lock()

# Jegyzetek tárolása
NOTES_FILE = 'notes.json'
SAVED_NOTES_FILE = 'saved_notes.json'
notes_data = {
    'content': '',
    'last_modified': None,
    'sessions': {}
}
saved_notes = []

def load_notes():
    """Jegyzetek betöltése JSON fájlból"""
    global notes_data
    try:
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                notes_data = json.load(f)
    except Exception as e:
        print(f"Hiba a jegyzetek betöltésekor: {e}")
        notes_data = {'content': '', 'last_modified': None, 'sessions': {}}

def load_saved_notes():
    """Mentett jegyzetek betöltése JSON fájlból"""
    global saved_notes
    try:
        if os.path.exists(SAVED_NOTES_FILE):
            with open(SAVED_NOTES_FILE, 'r', encoding='utf-8') as f:
                saved_notes = json.load(f)
    except Exception as e:
        print(f"Hiba a mentett jegyzetek betöltésekor: {e}")
        saved_notes = []

def save_notes():
    """Jegyzetek mentése JSON fájlba"""
    global notes_data
    try:
        with file_lock:
            notes_data['last_modified'] = datetime.datetime.now().isoformat()
            with open(NOTES_FILE, 'w', encoding='utf-8') as f:
                json.dump(notes_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Hiba a jegyzetek mentésekor: {e}")

def save_saved_notes():
    """Mentett jegyzetek mentése JSON fájlba"""
    global saved_notes
    try:
        with file_lock:
            with open(SAVED_NOTES_FILE, 'w', encoding='utf-8') as f:
                json.dump(saved_notes, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Hiba a mentett jegyzetek mentésekor: {e}")

def cleanup_sessions():
    """Régi vagy inaktív session-ök tisztítása"""
    global notes_data
    import datetime as dt
    
    # Távolítsuk el a duplikált SID-eket
    seen_sids = set()
    sessions_to_remove = []
    current_time = dt.datetime.now()
    
    for session_id, session_info in list(notes_data['sessions'].items()):
        sid = session_info['sid']
        
        # Ellenőrizzük a duplikációt
        if sid in seen_sids:
            # Duplikált SID, távolítsuk el a régebbit
            sessions_to_remove.append(session_id)
        else:
            seen_sids.add(sid)
            
        # Ellenőrizzük az időalapú lejáratot (pl. 1 órás timeout)
        try:
            connected_time = dt.datetime.fromisoformat(session_info['connected_at'])
            if (current_time - connected_time).total_seconds() > 3600:  # 1 óra
                sessions_to_remove.append(session_id)
        except:
            # Ha nem tudunk parseolni, távolítsuk el
            sessions_to_remove.append(session_id)
    
    # Duplikált és lejárt session-ök eltávolítása
    for session_id in sessions_to_remove:
        if session_id in notes_data['sessions']:
            del notes_data['sessions'][session_id]
            print(f"Session eltávolítva: {session_id}")
    
    # Limitáljuk a session-ök számát (max 100)
    if len(notes_data['sessions']) > 100:
        # Távolítsuk el a legrégebbi session-öket
        sorted_sessions = sorted(notes_data['sessions'].items(), 
                               key=lambda x: x[1]['connected_at'])
        for session_id, _ in sorted_sessions[:-100]:
            del notes_data['sessions'][session_id]
            print(f"Régi session eltávolítva: {session_id}")

# Jegyzetek betöltése indításkor
load_notes()
load_saved_notes()

@app.route('/')
def index():
    """Főoldal megjelenítése"""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Új kliens csatlakozása"""
    # Ellenőrizzük, hogy ez a SID már létezik-e valamelyik session-ben
    existing_session = None
    for session_id, session_info in list(notes_data['sessions'].items()):
        if session_info['sid'] == request.sid:
            existing_session = session_id
            break
    
    if existing_session:
        # Ha már létezik, csak frissítjük
        notes_data['sessions'][existing_session]['connected_at'] = datetime.datetime.now().isoformat()
        session_id = existing_session
        print(f"Kliens újracsatlakozott: {session_id}")
    else:
        # Új session létrehozása
        session_id = str(uuid.uuid4())
        notes_data['sessions'][session_id] = {
            'connected_at': datetime.datetime.now().isoformat(),
            'sid': request.sid
        }
        print(f"Új kliens csatlakozott: {session_id}")
    
    # Aktuális tartalom küldése az új kliensnek
    emit('content_update', {
        'content': notes_data['content'],
        'last_modified': notes_data['last_modified'],
        'session_id': session_id
    })
    
    # Session-ök tisztítása és aktív felhasználók számának broadcast-ja
    cleanup_sessions()
    emit('user_count', {'count': len(notes_data['sessions'])}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    """Kliens lecsatlakozása"""
    # Session törlése
    session_to_remove = None
    for session_id, session_info in list(notes_data['sessions'].items()):
        if session_info['sid'] == request.sid:
            session_to_remove = session_id
            break
    
    if session_to_remove:
        del notes_data['sessions'][session_to_remove]
        print(f"Kliens lecsatlakozott: {session_to_remove}")
    
    # Session-ök tisztítása és aktív felhasználók számának broadcast-ja
    cleanup_sessions()
    emit('user_count', {'count': len(notes_data['sessions'])}, broadcast=True)

@socketio.on('content_change')
def handle_content_change(data):
    """Tartalom változás kezelése"""
    global notes_data
    
    try:
        # Tartalom frissítése
        notes_data['content'] = data['content']
        
        # Változás broadcast minden kliensnek (kivéve a küldőt)
        emit('content_update', {
            'content': data['content'],
            'last_modified': datetime.datetime.now().isoformat()
        }, broadcast=True, include_self=False)
        
        # Automatikus mentés
        save_notes()
        
    except Exception as e:
        print(f"Hiba a tartalom változás kezelésekor: {e}")
        emit('error', {'message': 'Hiba történt a mentés során'})

@socketio.on('manual_save')
def handle_manual_save():
    """Manuális mentés kezelése"""
    try:
        save_notes()
        emit('save_success', {
            'message': 'Jegyzetek sikeresen mentve!',
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Hiba a manuális mentéskor: {e}")
        emit('error', {'message': 'Hiba történt a mentés során'})

@socketio.on('get_stats')
def handle_get_stats():
    """Statisztikák lekérése"""
    try:
        content_length = len(notes_data['content'])
        word_count = len(notes_data['content'].split()) if notes_data['content'] else 0
        line_count = notes_data['content'].count('\n') + 1 if notes_data['content'] else 0
        
        emit('stats_update', {
            'characters': content_length,
            'words': word_count,
            'lines': line_count,
            'last_modified': notes_data['last_modified'],
            'active_users': len(notes_data['sessions'])
        })
    except Exception as e:
        print(f"Hiba a statisztikák lekérésekor: {e}")

@socketio.on('save_note_as')
def handle_save_note_as(data):
    """Jegyzetek mentése megadott névvel"""
    global saved_notes
    try:
        title = data.get('title', '').strip()
        content = data.get('content', '')
        
        if not title:
            emit('error', {'message': 'A cím megadása kötelező!'})
            return
        
        # Ellenőrizzük, hogy létezik-e már ilyen címmel jegyzet
        existing_index = next((i for i, note in enumerate(saved_notes) if note['title'] == title), None)
        
        # Új ID generálása egyedi timestamp alapján
        new_id = int(datetime.datetime.now().timestamp() * 1000)
        
        note_data = {
            'id': saved_notes[existing_index]['id'] if existing_index is not None else new_id,
            'title': title,
            'content': content,
            'created_at': saved_notes[existing_index]['created_at'] if existing_index is not None else datetime.datetime.now().isoformat(),
            'modified_at': datetime.datetime.now().isoformat(),
            'word_count': len(content.split()) if content else 0,
            'char_count': len(content)
        }
        
        if existing_index is not None:
            # Frissítjük a meglévő jegyzetet
            saved_notes[existing_index] = note_data
            message = f'Jegyzet frissítve: {title}'
        else:
            # Új jegyzet hozzáadása
            saved_notes.append(note_data)
            message = f'Jegyzet mentve: {title}'
        
        save_saved_notes()
        emit('save_success', {'message': message})
        emit('saved_notes_update', {'notes': saved_notes}, broadcast=True)
        
    except Exception as e:
        print(f"Hiba a jegyzet mentésekor: {e}")
        emit('error', {'message': 'Hiba történt a jegyzet mentése során'})

@socketio.on('get_saved_notes')
def handle_get_saved_notes():
    """Mentett jegyzetek listájának lekérése"""
    try:
        emit('saved_notes_update', {'notes': saved_notes})
    except Exception as e:
        print(f"Hiba a mentett jegyzetek lekérésekor: {e}")
        emit('error', {'message': 'Hiba történt a jegyzetek lekérése során'})

@socketio.on('load_saved_note')
def handle_load_saved_note(data):
    """Mentett jegyzet betöltése"""
    global notes_data
    try:
        note_id = data.get('id')
        note = next((n for n in saved_notes if n['id'] == note_id), None)
        
        if not note:
            emit('error', {'message': 'A jegyzet nem található!'})
            return
        
        # Aktuális tartalom frissítése
        notes_data['content'] = note['content']
        save_notes()
        
        # Tartalom broadcast minden kliensnek
        emit('content_update', {
            'content': note['content'],
            'last_modified': datetime.datetime.now().isoformat()
        }, broadcast=True)
        
        emit('save_success', {'message': f'Jegyzet betöltve: {note["title"]}'})
        
    except Exception as e:
        print(f"Hiba a jegyzet betöltésekor: {e}")
        emit('error', {'message': 'Hiba történt a jegyzet betöltése során'})

@socketio.on('delete_saved_note')
def handle_delete_saved_note(data):
    """Mentett jegyzet törlése"""
    global saved_notes
    try:
        note_id = data.get('id')
        note_index = next((i for i, n in enumerate(saved_notes) if n['id'] == note_id), None)
        
        if note_index is None:
            emit('error', {'message': 'A jegyzet nem található!'})
            return
        deleted_note = saved_notes.pop(note_index)
        save_saved_notes()
        
        emit('save_success', {'message': f'Jegyzet törölve: {deleted_note["title"]}'})
        emit('saved_notes_update', {'notes': saved_notes}, broadcast=True)
        
    except Exception as e:
        print(f"Hiba a jegyzet törlésekor: {e}")
        emit('error', {'message': 'Hiba történt a jegyzet törlése során'})

@socketio.on('search_saved_notes')
def handle_search_saved_notes(data):
    """Mentett jegyzetek keresése"""
    try:
        query = data.get('query', '').lower().strip()
        
        if not query:
            emit('saved_notes_update', {'notes': saved_notes})
            return
        
        # Keresés a címben és tartalomban
        filtered_notes = []
        for note in saved_notes:
            if (query in note['title'].lower() or 
                query in note['content'].lower()):
                filtered_notes.append(note)
        
        emit('saved_notes_update', {'notes': filtered_notes})
        
    except Exception as e:
        print(f"Hiba a keresés során: {e}")
        emit('error', {'message': 'Hiba történt a keresés során'})

if __name__ == '__main__':
    print("🚀 Real-time Notepad indítása...")
    print("📝 Elérhető: http://localhost:{port}")
    print("💾 Jegyzetek automatikusan mentve: notes.json")
    print("🌐 WebSocket támogatás engedélyezve")
    
    # Kezdeti session tisztítás
    cleanup_sessions()
    
    try:
        socketio.run(app, host='0.0.0.0', port=5001, debug=True, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n👋 Alkalmazás leállítva")
    except Exception as e:
        print(f"❌ Hiba az alkalmazás indításakor: {e}")