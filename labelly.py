import streamlit as st
import pandas as pd
import os
import sys
from PIL import Image
import yaml
from program.utility import load_image, load_image_df, create_test_csv

# Set default configurations of page
st.set_page_config(page_title="Labelly",
                   page_icon="🧊",
                   layout="centered")


# Set session variables
if 'configs' not in st.session_state:
    # Loads configuration in session state
    with open('config.yaml') as yaml_file:
        st.session_state.configs = yaml.load(yaml_file, yaml.FullLoader)

    if st.session_state.configs['_properties']['test_case']['is_test_case']:
        print(50*'=', '\nThis is a Test Case - File Properties will be overwritten\n', 50*'=')
        st.session_state.configs['csv_path'] = st.session_state.configs['_properties']['test_case']['test_csv_path']
        st.session_state.configs['image_folder'] = st.session_state.configs['_properties']['test_case']['test_image_folder']
        # Init test Dataframe
        create_test_csv(csv_path=st.session_state.configs['csv_path'],
                        image_path=st.session_state.configs['image_folder'])
    else:
        if not os.path.exists(st.session_state.configs['csv_path']):
            create_test_csv(csv_path=st.session_state.configs['csv_path'],
                            image_path=st.session_state.configs['image_folder'],
                            duplicated_label_factor=st.session_state.configs['duplicated_label_factor'])

# Set session states
if 'df' not in st.session_state:
    # Loads df in session state
    st.session_state.df = load_image_df(data_path=st.session_state.configs['csv_path'])

if 'progress' not in st.session_state:
    # Counts amount of labelled images
    st.session_state.progress = st.session_state.df.loc[~st.session_state.df['type'].isnull()].shape[0]
    st.session_state.progress_all = st.session_state.df.shape[0]

if 'image_name' not in st.session_state:
    image_name = st.session_state.df.loc[st.session_state.df['type'].isnull(), 'image']
    if image_name.shape[0] > 0:
        # Show road cover if not labelled
        st.session_state.image_name = image_name.iloc[0]
    else:
        st.session_state.image_name = 'finished_photo.jpg'

if 'select_type' not in st.session_state:
    st.session_state.select_type = None

# Webpage
# Header of webpage
st.header('Labelly - A Lightweight Labelling Interface', )

# if finished all labels
if st.session_state.progress == st.session_state.progress_all:
    st.success('Finished with all the Labels.')
    st.balloons()
    st.stop()

# Add Progress Bar to page
#with st.expander('Zeige Fortschritt als Statusbalken:'):
col1, col2 = st.columns([3, 7])
with col1:
    interrupt = st.button('Abbrechen & Speichern',
                          help='Bricht die Iteration ab und speichert die bisherigen Resultate.')
with col2:
    st.write('')
    progress_bar = st.progress(st.session_state.progress / st.session_state.progress_all)

# Interrupt functionality with save checkpoint
if interrupt:
    st.info(f'\nBisheriger Fortschritt:  {st.session_state.progress} von {st.session_state.progress_all}')
    st.warning(f'Iteration gestoppt - Daten gespeichert und ready zum weiterarbeiten.')
    st.session_state.df.to_csv(st.session_state.configs['csv_path'], index=False)

    proceed = st.button('Fortfahren')
    if proceed:
        st.experimental_rerun()
    st.stop()


# Plot Image and label form therefore create two columns
image_column, label_column = st.columns([2, 1])

# Show Images
with image_column:
    # Make function which loads next image
    if st.session_state.image_name != 'finished_photo.jpg':
        image = load_image(image_path=st.session_state.configs['image_folder'],
                           image_name=st.session_state.image_name)
    else:
        # Show Congratulation Road Cover if finished all
        image = load_image(image_path='data/_finished/',
                           image_name=st.session_state.image_name)
    st.image(image=image, width=600,
             use_column_width=True)

# Label column
with label_column:
    selected_type = st.selectbox(label='Selektiere Typ:',
                                 options=st.session_state.configs['type_labels'],
                                 index=0,
                                 help='Selektiere definierter Obertyp des Kanaldeckels')
    if selected_type:
        selected_output = st.selectbox(label='Selektiere Subtyp:',
                                       options=st.session_state.configs['ground_truth_labels'][selected_type],
                                       help='Selektiere Untertyp des definierten Obertyps des Kanaldeckels')
        if st.button('Bestätigen'):
            st.session_state.df.loc[st.session_state.df['image'] == st.session_state.image_name, 'type'] = selected_type
            st.session_state.df.loc[st.session_state.df['image'] == st.session_state.image_name, 'subtype'] = selected_output

            if st.session_state.progress > 0:
                if st.session_state.progress % st.session_state.configs['_properties']['batch_size'] == 0:
                    # Save DataFrame in batches (defined in config.yaml)
                    st.session_state.df.to_csv(st.session_state.configs['csv_path'], index=False)
                elif st.session_state.progress + 1 == st.session_state.progress_all:
                    print('Saving Dataframe')
                    st.session_state.df.to_csv(st.session_state.configs['csv_path'], index=False)

            if st.session_state.progress < st.session_state.progress_all:
                st.session_state.progress += 1

            # Delete from session state forces to reload session state
            del st.session_state.image_name

            st.experimental_rerun()

        st.write('--------------------')
        with st.expander(label='Fortschritt', expanded=True):
            st.metric(label='', value=f'{st.session_state.progress} von {st.session_state.progress_all}')


st.write(50*'-')
# Descriptions
with st.expander('Anleitung', expanded=True):
    st.markdown(body='This tool was built for the purpose to label given certain images . And so on ... '
                     '\n\nOne should proceed as follows: '
                     '\n- Label the given Image below by using the dropdown selection'
                     '\n- If the correct label was chosen then submit the label.')

with st.expander('Weitere Informationen', expanded=False):
    st.markdown(body='This tool was built for the purpose to label given certain images. This tool will automatically '
                     'save the progress from another labelling iteration.')

