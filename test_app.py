from streamlit.testing.v1 import AppTest
import warnings

warnings.filterwarnings('ignore')

try:
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()
    if at.exception:
        print("Exception found:")
        print(at.exception)
    else:
        print("No exception on first load")
except Exception as e:
    print(f"Error testing: {e}")
