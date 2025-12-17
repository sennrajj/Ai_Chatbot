from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from src.search import build_or_load_embeddings, search_query
import os
import uuid

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Load embeddings saat startup
print("[INFO] Loading embeddings and model...")
df_kb, model, embeddings = build_or_load_embeddings()
print("[INFO] Model and embeddings loaded successfully!")

def init_chat_system():
    """Initialize chat system with multiple chat support"""
    if 'chat_sessions' not in session:
        session['chat_sessions'] = {}
    if 'current_chat_id' not in session:
        session['current_chat_id'] = None
    if 'chat_counter' not in session:
        session['chat_counter'] = 0

@app.route('/')
def index():
    init_chat_system()
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        init_chat_system()
        data = request.get_json()
        user_input = data.get('query', '').strip()

        if not user_input:
            return jsonify({'answer': 'Silakan masukkan pertanyaan.', 'history': []})

        print(f"[APP] Processing query: '{user_input}'")
        
        # Cari jawaban berdasarkan embeddings
        results = search_query(user_input, df_kb, model, embeddings)
        
        print(f"[APP] Search results count: {len(results)}")
        
        if results and len(results) > 0:
            answer = results[0]['answer']
            score = results[0].get('score', 0)
            print(f"[APP] Best match score: {score}")
        else:
            answer = "Maaf, saya belum memiliki informasi untuk itu."
            print("[APP] No results found")

        # Jika tidak ada chat aktif, buat baru
        if session['current_chat_id'] is None:
            session['chat_counter'] += 1
            chat_id = str(session['chat_counter'])
            session['current_chat_id'] = chat_id
            session['chat_sessions'][chat_id] = {
                'id': chat_id,
                'title': user_input[:30] + ('...' if len(user_input) > 30 else ''),
                'messages': []
            }

        # Simpan pesan ke chat aktif
        current_chat = session['chat_sessions'][session['current_chat_id']]
        current_chat['messages'].append({'user': user_input, 'bot': answer})
        
        # Update judul chat dengan pesan pertama
        if len(current_chat['messages']) == 1:
            current_chat['title'] = user_input[:30] + ('...' if len(user_input) > 30 else '')
        
        session.modified = True

        return jsonify({
            'answer': answer, 
            'history': current_chat['messages'],
            'current_chat_id': session['current_chat_id']
        })
        
    except Exception as e:
        print(f"[APP ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'answer': 'Terjadi kesalahan internal. Silakan coba lagi.',
            'history': []
        }), 500

@app.route('/get_history', methods=['GET'])
def get_history():
    """Get all chat sessions for sidebar"""
    init_chat_system()
    chat_sessions = session.get('chat_sessions', {})
    
    # Convert to list for frontend
    chats_list = []
    for chat_id, chat_data in chat_sessions.items():
        chats_list.append({
            'id': chat_data['id'],
            'title': chat_data['title'],
            'preview': chat_data['messages'][0]['user'] if chat_data['messages'] else 'Percakapan baru',
            'message_count': len(chat_data['messages'])
        })
    
    # Sort by ID descending (newest first)
    chats_list.sort(key=lambda x: int(x['id']), reverse=True)
    
    return jsonify(chats_list)

@app.route('/new_chat', methods=['POST'])
def new_chat():
    """Start new chat without deleting existing ones"""
    init_chat_system()
    
    # Reset current chat, but keep all chat sessions
    session['current_chat_id'] = None
    
    session.modified = True
    return jsonify({
        'message': 'Chat baru dimulai.', 
        'current_chat_id': None
    })

@app.route('/load_chat/<chat_id>', methods=['GET'])
def load_chat(chat_id):
    """Load specific chat session"""
    init_chat_system()
    
    if chat_id in session['chat_sessions']:
        session['current_chat_id'] = chat_id
        chat_messages = session['chat_sessions'][chat_id]['messages']
        session.modified = True
        
        return jsonify({
            'history': chat_messages,
            'current_chat_id': chat_id
        })
    else:
        return jsonify({'error': 'Chat tidak ditemukan'}), 404

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear ALL chat histories"""
    session['chat_sessions'] = {}
    session['current_chat_id'] = None
    session['chat_counter'] = 0
    session.modified = True
    return jsonify({'message': 'Semua history telah dihapus.'})

if __name__ == '__main__':
    app.run(debug=True)