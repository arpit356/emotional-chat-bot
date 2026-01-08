from backend.app.db import database
from backend.app.services.learning import extract_preferences_from_memories, consolidate_memories
import sys, os
root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(root, 'backend'))

if __name__ == '__main__':
    database.init_db()
    database.ensure_user_exists('u1')
    print('Before consolidation:', database.get_memories('u1'))
    consolidate_memories('u1')
    print('Preferences extracted:', extract_preferences_from_memories('u1'))
    print('After:', database.get_memories('u1'))
