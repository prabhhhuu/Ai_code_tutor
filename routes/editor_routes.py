from flask import Blueprint, render_template, request, session, redirect, jsonify
from services.prompt_service import build_prompt
from services.ai_service import ask_ai
from services.formatter_service import format_ai_output
from services.difficulty_service import calculate_difficulty
from database import get_db
import sqlite3

editor_bp = Blueprint("editor", __name__)

@editor_bp.route("/editor", methods=["GET", "POST"])
def editor():
    if "user" not in session:
        return redirect("/")

    result = ""
    code = ""
    language = "python"
    difficulty = None
    error = None

    if request.method == "POST":
        code = request.form.get("code", "")
        language = request.form.get("language", "python")
        mode = request.form.get("mode", "explain")
        model = request.form.get("model", "qwen")

        if code.strip():
            try:
                prompt = build_prompt(code, language, mode)
                raw = ask_ai(prompt, model)
                result = format_ai_output(raw)
                difficulty = calculate_difficulty(code)
                
                # Save to history
                save_to_history(session["user_id"], code, language, mode, result, difficulty)
            except ValueError as e:
                error = str(e)
            except Exception as e:
                error = f"❌ Error: {str(e)}. Please try again or contact support."

    return render_template(
        "editor.html",
        result=result,
        code=code,
        language=language,
        difficulty=difficulty,
        error=error
    )

@editor_bp.route("/history")
def history():
    if "user" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    db = get_db()
    cursor = db.cursor()
    
    # Fix Problem 2: Use sqlite3.Row to return dictionary-like objects
    cursor.row_factory = sqlite3.Row
    
    cursor.execute("""
        SELECT id, code, language, mode, result, difficulty, created_at 
        FROM code_history 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    """, (user_id,))
    
    # Convert Row objects to dictionaries for the template
    history_items = [dict(row) for row in cursor.fetchall()]
    db.close()
    
    return render_template("history.html", history=history_items)

@editor_bp.route("/history/delete/<int:history_id>", methods=["POST"])
def delete_history(history_id):
    """Delete a history item."""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session["user_id"]
    db = get_db()
    cursor = db.cursor()
    
    # Delete only if the history item belongs to the user
    cursor.execute("""
        DELETE FROM code_history 
        WHERE id = ? AND user_id = ?
    """, (history_id, user_id))
    
    db.commit()
    db.close()
    
    return jsonify({"success": True})

def save_to_history(user_id, code, language, mode, result, difficulty):
    """Save a code submission to the history table."""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        INSERT INTO code_history (user_id, code, language, mode, result, difficulty)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, code, language, mode, result, difficulty))
    
    db.commit()
    db.close()
