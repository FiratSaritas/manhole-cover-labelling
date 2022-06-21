import sys
from streamlit import cli as stcli
import streamlit

if __name__ == '__main__':
    # Prepare imagefolder when calling this file
    sys.argv = ["streamlit", "run", 'labelly.py']
    sys.exit(stcli.main())
