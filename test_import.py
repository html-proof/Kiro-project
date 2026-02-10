import sys
import traceback

try:
    import app.services.recommendation_service as rs
    print("Module imported")
    print("Module contents:", dir(rs))
    print("Has function:", hasattr(rs, 'get_user_recommendations'))
    
    if hasattr(rs, 'get_user_recommendations'):
        print("SUCCESS: Function exists")
    else:
        print("ERROR: Function does not exist")
except Exception as e:
    print(f"ERROR importing: {e}")
    traceback.print_exc()
